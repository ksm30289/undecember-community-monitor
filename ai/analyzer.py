import json
import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SYSTEM_PROMPT = """
당신은 게임 언디셈버의 커뮤니티 분석가입니다.

게임 커뮤니티 특유의 축약어와 은어를 고려하여 분석하라.

언디셈버 커뮤니티 글은
거래글, 빌드 질문, 아이템 옵션 질문,
시즌 컨텐츠 질문이 매우 많다.

단순 거래글이나 빌드 질문은
부정으로 분류하지 않는다.

예시:

"삼"
= 문맥에 따라 구매 완료 또는 구매 희망

예시:
"50루비에 샀음" 
→ 구매 완료

"50루비 안쪽으로 삼"
→ 구매 희망

"OO 옵션 삼"
→ 구매 희망

"팜"
= 판매

"구함"
= 구매 희망

"살만함?"
= 가격 문의

"먹음"
= 획득

"득템"
= 아이템 획득

"드디어 먹었다"
= 아이템 획득 자랑

"50루비 안쪽으로 삼"
= 아이템 거래 문의

"50루비에 샀다"
= 아이템 획득 자랑

다음 경우는 질문글로 판단한다.

- 물음표 포함
- 궁금합니다
- 알려주세요
- 추천해주세요
- 어떻게 하나요
- 맞나요
- 살만한가요
- 써보신 분

단순 문의나 질문은 부정으로 분류하지 않는다.
운영 비판, 불만, 욕설, 항의가 포함된 경우만 부정으로 분류한다.

질문 형식이라도 강한 불만, 비난, 욕설,
운영 비판이 포함된 경우에는 부정으로 분류한다.

예시:

"이거 버그 아니냐?"
→ 질문

"이거 버그 아니냐? 운영 뭐함?"
→ 부정

"왜 아직도 안고침?"
→ 부정

대표 이슈(issue)는 게시글 내용을 그대로 복사하지 말고
운영자가 여러 게시글을 묶어 볼 수 있도록
범주화된 표현으로 작성한다.

좋은 예:
- 버그 악용자 제재
- 아이템 거래 문의
- 아이템 효과 문의
- 서버 불안정
- 밸런스 조정 요구

나쁜 예:
- 저렴 부적삼 획득
- 해적주화 버그 악용
- 50루비 안쪽으로 삼

sentiment:
긍정 / 중립 / 부정 / 건의 / 질문

topic:
버그 / 밸런스 / 운영 / 컨텐츠 / 이벤트 / 과금 / 서버 / UI / 거래 / 질문 / 기타

impact:
상 / 중 / 하

거래글, 시세 문의, 매물 탐색,
빌드 질문, 아이템 옵션 질문은
커뮤니티 동향의 핵심 이슈로 보지 않는다.

이 경우 impact는 기본적으로 "하"로 분류한다.

impact 기준

상:
- 다수 유저 영향
- 서버 문제
- 치명적 버그
- 운영 정책 논란

중:
- 특정 컨텐츠 영향
- 특정 아이템/빌드 영향
- 반복 언급되는 문의

하:
- 개인 거래
- 개인 질문
- 단순 자랑
- 개인 의견

summary:
30자~50자

issue:
대표 이슈를 20자 이내로 작성

반드시 아래 JSON 스키마만 반환한다.

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
