import requests
from bs4 import BeautifulSoup

URL = "https://ud.floor.line.games/kr/bbs/community/community_kr/1"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}


def get_floor_posts():

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    posts = []

    rows = soup.select(
        "a.all-link.bbs-detail-link"
    )

    for row in rows:

        article_id = row.get(
            "article-id"
        )

        if not article_id:
            continue

        title_tag = row.select_one(
            ".noti-tit p"
        )

        if not title_tag:
            continue

        title = title_tag.get_text(
            strip=True
        )

        href = row.get("href")

        url = (
            "https://ud.floor.line.games"
            + href
        )

        posts.append({
            "source": "FLOOR",
            "postId": f"floor_{article_id}",
            "title": title,
            "url": url
        })

    return posts
