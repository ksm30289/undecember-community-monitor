from crawler.dcinside import get_dc_posts
from crawler.floor import get_floor_posts


print("===== DC =====")

dc_posts = get_dc_posts()

for post in dc_posts[:5]:
    print(post)

print()
print("===== FLOOR =====")

floor_posts = get_floor_posts()

for post in floor_posts[:5]:
    print(post)
