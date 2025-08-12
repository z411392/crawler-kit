import logging
from typing import Dict, Optional, List
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)


class AmazonParser:
    def __init__(self):
        pass

    def parse_product_page(self, content: str, url: str) -> Optional[Dict]:
        try:
            soup = BeautifulSoup(content, "html.parser")

            title = self._extract_title(soup)
            price = self._extract_price(soup)
            image = self._extract_image(soup)
            description = self._extract_description(soup)
            seller = self._extract_seller(soup)

            return {
                "url": url,
                "title": title,
                "price": price,
                "image": image,
                "description": description,
                "seller": seller,
            }
        except Exception as e:
            logger.error(f"Error parsing product page: {e}")
            return None

    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        title_strategies = [
            lambda: soup.find("span", attrs={"id": "productTitle"}).text.strip(),
            lambda: soup.find("img", attrs={"id": "landingImage"}).get("alt").strip(),
            lambda: soup.find("span", attrs={"id": "btAsinTitle"}).text.strip(),
            lambda: soup.find("h1", attrs={"data-automation-id": "title"}).text.strip(),
            lambda: soup.title.text.strip() if soup.title else None,
        ]

        for strategy in title_strategies:
            try:
                result = strategy()
                if result and result.strip():
                    return result
            except Exception:
                continue

        return "N/A"

    def _extract_price(self, soup: BeautifulSoup) -> Optional[str]:
        price_strategies = [
            lambda: soup.find("span", attrs={"class": "a-text-price"})
            .find("span")
            .text,
            lambda: soup.find("span", attrs={"id": "price"}).text,
            lambda: soup.select(
                'span[class="_p13n-desktop-sims-fbt_price_p13n-sc-price__bCZQt"]'
            )[0]
            .contents[0]
            .strip(),
            lambda: (
                soup.select('span[class="a-price-whole"]')[0].contents[0].strip()
                + soup.select('span[class="a-price-fraction"]')[0].contents[0].strip()
                + soup.select('span[class="a-price-symbol"]')[0].contents[0].strip()
            ),
            lambda: (
                soup.select('span[class="a-price-whole"]')[0].contents[0].strip()
                + soup.select('span[class="a-price-symbol"]')[0].contents[0].strip()
            ),
            lambda: soup.select_one(".x-price-primary .ux-textspans").text.strip()
            if soup.select_one(".x-price-primary .ux-textspans")
            else None,
        ]

        for strategy in price_strategies:
            try:
                result = strategy()
                if result and result.strip():
                    return result
            except Exception:
                continue

        return "N/A"

    def _extract_image(self, soup: BeautifulSoup) -> Optional[str]:
        image_strategies = [
            lambda: soup.find("img", attrs={"id": "landingImage"}).get("src"),
            lambda: soup.find("img", attrs={"id": "main-image"}).get("src"),
            lambda: soup.find("img", attrs={"id": "js-masrw-main-image"}).get("src"),
            lambda: soup.find("div", attrs={"id": "img-canvas"}).find("img").get("src")
            if soup.find("div", attrs={"id": "img-canvas"})
            else None,
            lambda: soup.find("img", attrs={"id": "atf-full"}).get("src"),
            lambda: soup.find("meta", property="og:image").get("content")
            if soup.find("meta", property="og:image")
            else None,
        ]

        for strategy in image_strategies:
            try:
                result = strategy()
                if result and result.strip():
                    return result
            except Exception:
                continue

        return "N/A"

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        description_strategies = [
            lambda: soup.find("div", attrs={"id": "productDescription"}).text.strip(),
            lambda: soup.find(
                "div", attrs={"id": "mas-product-description"}
            ).text.strip(),
            lambda: soup.find(
                "div", attrs={"data-automation-id": "atfSynopsisExpander"}
            ).text.strip(),
            lambda: soup.find("meta", property="og:description").get("content")
            if soup.find("meta", property="og:description")
            else None,
            lambda: self._extract_title(soup)
            if self._extract_title(soup) != "N/A"
            else None,
        ]

        for strategy in description_strategies:
            try:
                result = strategy()
                if result and result.strip():
                    return result
            except Exception:
                continue

        return "N/A"

    def _extract_seller(self, soup: BeautifulSoup) -> Optional[str]:
        seller_strategies = [
            lambda: soup.select(
                'div[id="tabular_feature_div"] div[class="tabular-buybox-text a-spacing-none"] span a'
            )[0]
            .contents[0]
            .strip(),
            lambda: soup.select('div[id="merchant-info"] a span')[0]
            .contents[0]
            .strip(),
            lambda: soup.select(
                "#productDetails_techSpec_section_1 > tbody:nth-child(1) > tr:nth-child(11) > td:nth-child(2)"
            )[0]
            .contents[0]
            .strip(),
            lambda: soup.select("a[id='sellerProfileTriggerId']")[0].text.strip(),
            lambda: soup.select_one(
                ".x-sellercard-atf__info__about-seller"
            ).text.strip()
            if soup.select_one(".x-sellercard-atf__info__about-seller")
            else None,
        ]

        for strategy in seller_strategies:
            try:
                result = strategy()
                if result and result.strip() and result != "":
                    return result
            except Exception:
                continue

        return "N/A"
