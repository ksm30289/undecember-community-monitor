import json
import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SYSTEM_PROMPT = """
당신은 게임 언디셈버의 커뮤니티 분석가입니다.

반드시 JSON만 반환하세요.

sentiment:
긍정 / 중립 / 부정 / 건의

topic:
버그 / 밸런스 / 운영 / 컨텐츠 / 이벤트 / 과금 / 서버 / UI / 기타

impact:
상 / 중 / 하

summary:
30자~50자

issue:
대표 이슈를 20자 이내로 작성

예시:

{
  "sentiment":"부정",
  "topic":"운영",
  "issue":"버그 악용자 제재",
  "impact":"중",
  "summary":"버그 악용자 제재가 미흡하다는 의견 제기"
}
"""


def analyze_post(post):

    text = f"""
제목:
{post['title']}

본문:
{post['content']}
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    content = (
        response.choices[0]
        .message.content
        .strip()
    )

    try:
        return json.loads(content)

    except Exception:

        return {
            "sentiment": "중립",
            "topic": "기타",
            "issue": "",
            "impact": "하",
            "summary": ""
        }
