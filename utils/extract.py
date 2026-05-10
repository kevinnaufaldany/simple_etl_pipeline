from datetime import datetime
import time
import re

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}


def fetching_content(url):
    """Mengambil konten HTML dari URL yang diberikan."""
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None


def extract_fashion_data(card, timestamp=None):
    """Mengambil data fashion dari elemen div.collection-card."""
    try:
        if timestamp is None:
            timestamp = datetime.now()

        title_element = card.find('h3', class_='product-title')
        if not title_element:
            return None
        title = title_element.get_text(strip=True)
        if title == "Unknown Product":
            return None

        price_element = card.find('span', class_='price')
        if not price_element:
            return None
        price = price_element.get_text(strip=True)

        rating = "Invalid Rating"
        rating_element = card.find('p', string=re.compile(r"Rating\s*:", re.IGNORECASE))
        if rating_element:
            text = rating_element.get_text(strip=True)
            match = re.search(r"(\d+(?:\.\d+)?)", text)
            if match:
                rating = match.group(1)

        colors = "Colors not found"
        colors_element = card.find('p', string=re.compile(r"Colors", re.IGNORECASE))
        if colors_element:
            text = colors_element.get_text(strip=True)
            match = re.search(r"(\d+)", text)
            if match:
                colors = match.group(1)

        size = "Size not found"
        size_element = card.find('p', string=re.compile(r"Size\s*:", re.IGNORECASE))
        if size_element:
            text = size_element.get_text(strip=True)
            match = re.search(r"Size\s*:\s*(.+)", text, flags=re.IGNORECASE)
            if match:
                size = match.group(1).strip()

        gender = "Gender not found"
        gender_element = card.find('p', string=re.compile(r"Gender\s*:", re.IGNORECASE))
        if gender_element:
            text = gender_element.get_text(strip=True)
            match = re.search(r"Gender\s*:\s*(.+)", text, flags=re.IGNORECASE)
            if match:
                gender = match.group(1).strip()

        return {
            "title": title,
            "price": price,
            "rating": rating,
            "colors": colors,
            "size": size,
            "gender": gender,
            "timestamp": timestamp,
        }
    except Exception as e:
        print(f"ERROR saat extract data fashion: {e}")
        return None


def scrape_fashion_data(base_url, start_page=1, delay=2):
    """Mengambil seluruh data produk fashion dari halaman web."""
    data = []
    page_number = start_page
    timestamp = datetime.now()

    while True:
        if page_number == 1:
            url = base_url.replace('/page{}.html', '')
        else:
            url = base_url.format(page_number)

        print(f"Scraping halaman: {url}")
        content = fetching_content(url)
        if not content:
            break

        soup = BeautifulSoup(content, "html.parser")
        product_cards = soup.find_all('div', class_='collection-card')
        print(f"  -> Menemukan {len(product_cards)} produk di halaman ini")

        for i, card in enumerate(product_cards):
            fashion = extract_fashion_data(card, timestamp)
            if fashion:
                data.append(fashion)
            else:
                print(f"  -> Produk {i + 1} tidak bisa diextract")

        next_button = soup.find('li', class_='next')
        if next_button:
            page_number += 1
            if delay:
                time.sleep(delay)
            if page_number > 50:
                break
        else:
            break

    print(f"\nTotal data yang berhasil diambil: {len(data)}")
    return data
