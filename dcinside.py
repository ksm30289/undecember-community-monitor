import requests
from bs4 import BeautifulSoup

URL = "https://gall.dcinside.com/mgallery/board/lists/?id=undecember"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}


def get_dc_posts():

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "lxml"
    )

    posts = []

    rows = soup.select(
        "tr.ub-content.us-post"
    )

    for row in rows:

        post_no = row.get("data-no")

        if not post_no:
            continue

        title_tag = row.select_one(
            "td.gall_tit a"
        )

        if not title_tag:
            continue

        title = title_tag.get_text(
            strip=True
        )

        url = (
            "https://gall.dcinside.com"
            + title_tag["href"]
        )

        date_tag = row.select_one(
            "td.gall_date"
        )

        created_at = (
            date_tag.get_text(strip=True)
            if date_tag
            else ""
        )

        posts.append({
            "source": "DC",
            "postId": f"dc_{post_no}",
            "title": title,
            "url": url,
            "createdAt": created_at
        })

    return posts
