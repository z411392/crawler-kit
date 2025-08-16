import asyncio
import aiohttp
import time
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import pandas as pd


@dataclass
class CrawlingJob:
    platform: str
    url: str
    job_id: Optional[str] = None
    status: str = "pending"
    response_time: Optional[float] = None
    error: Optional[str] = None


class CrawlTrigger:
    def __init__(self, base_url, timeout: int = 50):
        self.base_url = base_url
        self.timeout = timeout
        self.source = "lazada"
        self.type = "product"
        self.platform = "web"

    async def trigger(
        self, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, url: str
    ) -> CrawlingJob:
        async with semaphore:
            job = CrawlingJob(platform=self.platform, url=url)
            endpoint = f"{self.base_url}/sources/{self.source}/types/{self.type}/platforms/{self.platform}"
            payload = {"url": url}

            try:
                start_time = time.time()
                async with session.post(
                    endpoint,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                    headers={"Content-Type": "application/json"},
                ) as response:
                    job.response_time = time.time() - start_time
                    if response.status == 200:
                        result = await response.json()
                        job.status = "triggered"
                        job.job_id = result.get("data", {}).get("job_id")
                        print(
                            f"✅ {self.platform} - {url[:60]}... - 觸發成功 ({job.response_time:.2f}s)"
                        )
                    else:
                        text = await response.text()
                        job.status = "failed"
                        job.error = f"HTTP {response.status}: {text}"
                        print(
                            f"❌ {self.platform} - {url[:60]}... - 觸發失敗: {job.error}"
                        )
            except asyncio.TimeoutError:
                job.status = "timeout"
                job.error = f"請求超時 (>{self.timeout}s)"
                print(f"⏰ {self.platform} - {url[:60]}... - 請求超時")

            except Exception as e:
                job.status = "error"
                job.error = str(e)
                print(f"💥 {self.platform} - {url[:60]}... - 錯誤: {job.error}")

        return job

    def save_results(self, jobs: List[CrawlingJob], output_file: str = "results.json"):
        results = []
        for job in jobs:
            results.append(
                {
                    "platform": job.platform,
                    "url": job.url,
                    "job_id": job.job_id,
                    "status": job.status,
                    "response_time": job.response_time,
                    "error": job.error,
                    "timestamp": datetime.now().isoformat(),
                }
            )
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"📄 結果已保存至: {output_file}")


async def main(data_path, base_url, concurrency_limit):
    df = pd.read_csv(data_path)[:3]
    trigger = CrawlTrigger(base_url=base_url)

    semaphore = asyncio.Semaphore(concurrency_limit)

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(trigger.trigger(session, semaphore, row["url"]))
            for _, row in df.iterrows()
        ]
        jobs = await asyncio.gather(*tasks)
        trigger.save_results(jobs)


if __name__ == "__main__":
    data_path = "lazada_data.csv"
    base_url = "https://us-central1-crawler-kit.cloudfunctions.net/admin"
    concurrency_limit = 10
    asyncio.run(main(data_path, base_url, concurrency_limit))
