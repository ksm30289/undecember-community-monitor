from crawler.dcinside import get_dc_posts
from crawler.floor import get_floor_posts
from crawler.detail import (
    get_dc_content,
    get_floor_content
)
from sheets.sheet_writer import get_sheet

print("===== DC =====")

dc = get_dc_posts()[3]

print(dc["title"])
print(get_dc_content(dc["url"]))

print("\n===== FLOOR =====")

floor = get_floor_posts()[0]

print(floor["title"])
print(get_floor_content(floor["url"]))

sheet = get_sheet()

print(f"시트 연결 성공: {sheet.title}")

sheet.append_row([
    "테스트",
    "2026-06-24",
    "TEST",
    "저장 테스트",
    "본문 테스트",
    "https://test.com",
    "",
    "",
    "",
    "",
    "",
    "test_001"
])

print("시트 저장 성공")
