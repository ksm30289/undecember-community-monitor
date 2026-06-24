from crawler.dcinside import get_dc_posts
from crawler.floor import get_floor_posts

dc_posts = get_dc_posts()
floor_posts = get_floor_posts()

print("===== DC =====")

for post in dc_posts:
    print(post)

print("===== FLOOR =====")

for post in floor_posts:
    print(post)
