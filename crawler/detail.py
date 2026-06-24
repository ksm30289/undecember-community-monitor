import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}


def clean_text(text):

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def get_dc_content(url):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    content_div = soup.select_one(
        "div.write_div"
    )

    if not content_div:
        return ""

    return clean_text(
        content_div.get_text(
            "\n",
            strip=True
        )
    )


def get_floor_content(url):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    content_div = soup.select_one(
        "div.content.ql-editor"
    )

    if not content_div:
        return {
            "content": "",
            "createdAt": ""
        }

    content = clean_text(
        content_div.get_text(
            "\n",
            strip=True
        )
    )

    created_at = ""

    info_text = soup.get_text(
        " ",
        strip=True
    )

    match = re.search(
        r"(\d{4}\.\d{2}\.\d{2})",
        info_text
    )

    if match:

        created_at = (
            match.group(1)
            .replace(".", "-")
        )

    return {
        "content": content,
        "createdAt": created_at
    }
