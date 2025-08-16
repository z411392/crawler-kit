import logging
from typing import Dict, Optional
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class LazadaParser:
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
        # 優先使用更具體的產品標題選擇器
        title_selectors = [
            "#module_product_title_1 h1.pdp-mod-product-badge-title",
            ".pdp-mod-product-badge-title-v2",
            ".pdp-mod-product-badge-title",
            "h1.pdp-mod-product-badge-title",
        ]

        for selector in title_selectors:
            try:
                title_element = soup.select_one(selector)
                if title_element:
                    title = title_element.text.strip()
                    if title:
                        return title
            except Exception as e:
                logger.debug(f"Error with title selector {selector}: {e}")
                continue

        # 備用：使用頁面標題
        try:
            if soup.title:
                title = soup.title.text.strip()
                if title:
                    return title
        except Exception as e:
            logger.error(f"Error extracting title: {e}")

        return None

    def _extract_price(self, soup: BeautifulSoup) -> Optional[str]:
        price_selectors = [
            ".pdp-product-price .pdp-price_type_normal",
            ".pdp-v2-product-price-content-salePrice",
            ".pdp-price_color_orange",
            ".redmart-product-current-price-container",
            ".x-price-primary .ux-textspans",  # 原有的選擇器
        ]

        for selector in price_selectors:
            try:
                price_element = soup.select_one(selector)
                if price_element:
                    price = price_element.text.strip()
                    if price:
                        return price
            except Exception as e:
                logger.debug(f"Error with price selector {selector}: {e}")
                continue

        logger.warning("Unable to find product price")
        return None

    def _extract_image(self, soup: BeautifulSoup) -> Optional[str]:
        # 優先使用縮略圖選擇器
        image_selectors = [
            ".gallery-preview-panel__content img.gallery-preview-panel__image",
            ".gallery-preview-panel-v2__content img.gallery-preview-panel-v2__image",
            ".pdp-mod-common-image.gallery-preview-panel-v2__image",
        ]

        for selector in image_selectors:
            try:
                image_element = soup.select_one(selector)
                if image_element:
                    image_url = image_element.get("src")
                    if image_url:
                        return image_url
            except Exception as e:
                logger.debug(f"Error with image selector {selector}: {e}")
                continue

        # 備用：使用 og:image
        try:
            image_element = soup.find("meta", property="og:image")
            if image_element:
                image_url = image_element.get("content")
                if image_url:
                    return image_url
        except Exception as e:
            logger.debug(f"Error extracting og:image: {e}")

        logger.warning("Unable to find product image")
        return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        description_selectors = [
            "ul li[data-spm-anchor-id*='product_detail']",  # 新版面
            ".pdp-product-desc",  # 舊版面
            ".pdp-mod-specification",
        ]

        for selector in description_selectors:
            try:
                desc_element = soup.select_one(selector)
                if desc_element:
                    description = desc_element.text.strip()
                    if description:
                        return description
            except Exception as e:
                logger.debug(f"Error with description selector {selector}: {e}")
                continue

        # 備用：使用 og:description
        try:
            description_element = soup.find("meta", property="og:description")
            if description_element:
                description_text = description_element.get("content")
                if description_text:
                    return description_text
        except Exception as e:
            logger.debug(f"Error extracting og:description: {e}")

        # 最後備用：使用產品標題作為描述
        title = self._extract_title(soup)
        if title:
            return title

        return None

    def _extract_seller(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            img_elements = soup.find_all("img")
            for img in img_elements:
                img_src = img.get("src", "")
                if (
                    "https://img.lazcdn.com/g/shop/39d341a70b428b10bd2de1fb5c74c3e2.jpeg"
                    in img_src
                ):
                    return "Lazada global"
        except Exception as e:
            logger.debug(f"Error checking for Lazada global image: {e}")

        seller_selectors = [
            ".seller-name__detail .seller-name__detail-name",
            ".seller-name-v2__detail-name",
            ".pdp-link_theme_black.seller-name-v2__detail-name",
            ".redmart-seller__name-text",
            ".x-sellercard-atf__info__about-seller",
        ]

        for selector in seller_selectors:
            try:
                seller_element = soup.select_one(selector)
                if seller_element:
                    seller_name = seller_element.text.strip()
                    if seller_name:
                        return seller_name
            except Exception as e:
                logger.debug(f"Error with seller selector {selector}: {e}")
                continue

        logger.warning("Unable to find seller information")
        return "N/A"
