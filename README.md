# 🏋️ WorkoutCheck Bot

운동 인증 모임을 위한 Discord 봇입니다. 사진 인증 등록부터 주간 현황 집계, 미달 시 벌금 계산까지 모임 운영을 자동화합니다.

수기로 사진을 일일이 확인하고 벌금을 계산하던 번거로움을 해결하기 위해 직접 개발했고, **PostgreSQL 기반으로 Heroku에 배포해 24시간 운영**했습니다.

<br>

## 주요 기능

명령어 한 번으로 운동 모임 운영에 필요한 흐름이 모두 처리됩니다.

| 명령어 | 설명 |
|--------|------|
| `!등록` | 사용자를 등록하고 가입 주차를 기록합니다 |
| `!인증 [기록]` | 사진을 첨부해 운동을 인증합니다 (기록 생략 시 기본값 `오운완 💪🏻`) |
| `!현황` | 이번 주 멤버별 인증 횟수와 기록을 집계해 보여줍니다 |
| `!벌금` | 주 3회 미달 주차를 기준으로 누적 벌금을 계산합니다 |
| `!커맨드` | 사용 가능한 명령어 목록을 안내합니다 |

인증 시 사진 첨부를 강제하고 하루 1회만 인정하도록 검증하며, 현황 메시지가 Discord 2000자 제한을 넘으면 자동으로 분할 전송합니다.

<br>

## 화면

<table>
  <tr>
    <td align="center"><b>운동 인증</b></td>
    <td align="center"><b>운동 인증 실패 (중복)</b></td>
  </tr>
  <tr>
    <td><img width="100%" src="https://github.com/user-attachments/assets/cb541c3a-92bd-45c0-8c9a-d57cc86f1db3" alt="운동 인증" /></td>
    <td><img width="100%" src="https://github.com/user-attachments/assets/da60d6d9-b158-428c-9cb1-f4c7076e767f" alt="운동 인증 실패 (중복)" /></td>
  </tr>
  <tr>
    <td align="center"><b>주간 현황</b></td>
    <td align="center"><b>벌금 내역</b></td>
  </tr>
  <tr>
    <td><img width="100%" src="https://github.com/user-attachments/assets/94e7a90b-7976-431e-b921-2c62dbd47135" alt="주간 현황" /></td>
    <td><img width="100%" src="https://github.com/user-attachments/assets/e61fa7b0-2e53-4719-888b-880d5768c394" alt="벌금 내역" /></td>
  </tr>
</table>


<br>

## 기술 스택

- **Language** Python 3.12
- **Library** discord.py 2.4.0
- **Database** PostgreSQL (psycopg2)
- **Infra** Heroku

<br>

## 아키텍처

Clean Architecture를 적용해 도메인 로직과 외부 의존성을 분리했습니다. 인증·현황·벌금 같은 핵심 규칙은 `core`에 두고, Discord·DB 같은 외부 요소는 `frameworks`·`adapters`에서만 다루도록 의존성 방향을 안쪽으로 고정했습니다.

```
bot/
├── core/                    # 도메인 계층 (외부 의존성 없음)
│   ├── entities/            # User, Record
│   └── usecases/            # 등록 · 인증 · 현황 · 벌금 계산
├── adapters/
│   └── repositories/        # PostgreSQL 연결 및 데이터 접근
├── frameworks/
│   └── discord_bot.py       # Discord 명령어 핸들러 (진입점)
└── utils/                   # 주차 계산, KST 시간 처리
```

- **usecase**는 repository를 주입받아 동작하므로 데이터 저장 방식이 바뀌어도 도메인 로직은 그대로 유지됩니다.
- 모임 규칙(주 단위 집계, 가입 주차 이후부터 벌금 부과, 주 3회 기준 등)이 모두 usecase에 모여 있어 정책 변경 지점이 명확합니다.
- 주차는 KST 기준으로 계산해 시간대 오차 없이 인증을 집계합니다.

<br>

## 실행 방법

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 환경 변수 설정 (.env)
API_KEY=<your-discord-bot-token>
DATABASE_URL=<your-postgresql-url>

# 3. 실행
python bot/frameworks/discord_bot.py
```

PostgreSQL에 `users`, `records` 테이블이 필요합니다.

```sql
CREATE TABLE users (
    user_id     TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    joined_week TEXT NOT NULL
);

CREATE TABLE records (
    id      SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    week    TEXT NOT NULL,
    date    TEXT NOT NULL,
    word    TEXT,
    image   TEXT
);
```
