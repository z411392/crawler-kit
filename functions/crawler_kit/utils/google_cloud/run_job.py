from crawler_kit.utils.environments import is_emulating
from subprocess import Popen, PIPE
from os import getenv
from crawler_kit.utils.google_cloud.credentials_from_env import (
    credentials_from_env,
)
from google.cloud.run_v2 import JobsClient
from google.cloud.run_v2 import RunJobRequest


def run_job(
    *args,
):
    if is_emulating():
        process = Popen(["python", "main.py", *args], stdout=PIPE, text=True)
        for line in process.stdout:
            print(line, end="")
        if process.returncode == 0:
            return
        if process.stderr is None:
            return
        raise Exception(process.stderr)

    jobs_client = JobsClient(credentials=credentials_from_env())
    job_name = "worker"
    location = "us-central1"
    container_override = RunJobRequest.Overrides.ContainerOverride()
    container_override.args.extend(args)
    overrides = RunJobRequest.Overrides()
    overrides.container_overrides = [container_override]
    name = f"projects/{getenv('PROJECT_ID')}/locations/{location}/jobs/{job_name}"
    operation = jobs_client.run_job(
        request=RunJobRequest(
            name=name,
            overrides=overrides,
        )
    )
    return operation
