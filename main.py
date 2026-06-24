from crawler.dcinside import get_dc_posts
from crawler.floor import get_floor_posts
from crawler.detail import (
    get_dc_content,
    get_floor_content
)

print("===== DC =====")

dc = get_dc_posts()[3]

print(dc["title"])
print(get_dc_content(dc["url"]))

print("\n===== FLOOR =====")

floor = get_floor_posts()[0]

print(floor["title"])
print(get_floor_content(floor["url"]))

from sheets.sheet_writer import get_sheet

sheet = get_sheet()

print(sheet.title)
