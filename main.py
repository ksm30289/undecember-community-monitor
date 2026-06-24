from datetime import datetime

from crawler.dcinside import get_dc_posts
from crawler.floor import get_floor_posts
from crawler.detail import (
    get_dc_content,
    get_floor_content
)

from sheets.sheet_writer import (
    append_post,
    get_existing_post_ids
)

print("수집 시작")

existing_ids = get_existing_post_ids()

posts = []

# DC
for post in get_dc_posts():

    if post["postId"] in existing_ids:
        continue

    try:

        post["content"] = get_dc_content(
            post["url"]
        )

        post["collectedAt"] = (
            datetime.now()
            .strftime("%Y-%m-%d %H:%M:%S")
        )

        posts.append(post)

    except Exception as e:

        print(
            f"DC 본문 수집 실패: {post['postId']} / {e}"
        )

# FLOOR
for post in get_floor_posts():

    if post["postId"] in existing_ids:
        continue

    try:

        post["content"] = get_floor_content(
            post["url"]
        )

        post["collectedAt"] = (
            datetime.now()
            .strftime("%Y-%m-%d %H:%M:%S")
        )

        posts.append(post)

    except Exception as e:

        print(
            f"FLOOR 본문 수집 실패: {post['postId']} / {e}"
        )

print(
    f"신규 게시글 수집: {len(posts)}건"
)

saved_count = 0

for post in posts:

    try:

        append_post(post)

        saved_count += 1

        print(
            f"저장 완료: {post['postId']}"
        )

    except Exception as e:

        print(
            f"저장 실패: {post['postId']} / {e}"
        )

print(
    f"총 저장 건수: {saved_count}"
)
