from crawler.dcinside import get_dc_posts
from crawler.floor import get_floor_posts
from crawler.detail import (
    get_dc_content,
    get_floor_content
)

dc_posts = get_dc_posts()

first_dc = dc_posts[0]

print(first_dc["title"])

print(
    get_dc_content(
        first_dc["url"]
    )
)
