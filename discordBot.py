import discord
from discord.ext import commands
import datetime
import json
from dotenv import load_dotenv
import os

load_dotenv()

# users.json: 사용자 정보(가입 시점) 관리
def load_users():
    try:
        with open("users.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)

# records.json: 주별 인증 기록 관리
def load_records():
    try:
        with open("records.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_records(records):
    with open("records.json", "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

# 현재 주를 "YYYY-WW" 형식으로 반환 (월요일 시작 주)
def get_week():
    today = datetime.date.today()
    return today.strftime("%Y-%W")


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ 로그인 성공: {bot.user}")

@bot.command()
async def 승희(ctx):
    await ctx.send("엔젤 💫")

@bot.command()
async def 등록(ctx):
    users = load_users()
    user_id = str(ctx.author.id)
    current_week = get_week()
    
    # 이미 등록되어 있으면 안내 메시지 전송
    if user_id in users:
        await ctx.send(f"👤 {ctx.author.name}님은 이미 등록되어 있습니다.")
        return
    
    # 사용자 정보를 등록 (이름과 가입 주)
    users[user_id] = {
        "name": ctx.author.name,
        "joined_week": current_week
    }
    save_users(users)
    await ctx.send(f"✅ {ctx.author.mention}님이 등록되었습니다. 가입 주: {current_week}")

@bot.command()
async def 인증(ctx, *, 기록=None):
    # 사용자 정보 불러오기
    users = load_users()
    records = load_records()
    user_id = str(ctx.author.id)

    # 등록된 사용자가 아니면 등록을 요구하는 메시지 표시
    if user_id not in users:
        await ctx.send(f"❌ {ctx.author.mention}님은 아직 등록되지 않았습니다. `!등록` 명령어로 등록을 먼저 해주세요!")
        return

    # 운동 인증 사진이 없으면 에러 메시지 출력
    if not ctx.message.attachments:
        await ctx.send("❌ 운동 인증 사진을 함께 올려주세요!")
        return
    
    # 만약 기록이 제공되지 않으면 기본값으로 설정
    if 기록 is None:
        기록 = "오운완 💪🏻"

    current_week = get_week()

    # 해당 주가 records에 없으면 새로 생성
    if current_week not in records:
        records[current_week] = {}

    # 해당 주의 사용자 기록 리스트가 없으면 새로 생성
    if user_id not in records[current_week]:
        records[current_week][user_id] = []

    # 첫 번째 첨부 파일의 URL 사용 (필요시 여러 파일 처리 가능)
    image_url = ctx.message.attachments[0].url
    # 인증 기록 추가 (오늘 날짜, 입력한 메시지, 사진 URL)
    records[current_week][user_id].append({
        "date": str(datetime.date.today()),
        "word": 기록,
        "image": image_url
    })
    save_records(records)
    await ctx.send(f"✅ {ctx.author.mention}님의 운동 기록이 저장되었습니다!")

    
    # 사진 URL 저장
    image_url = ctx.message.attachments[0].url
    records[user_id][current_week].append({"date": str(datetime.date.today()), "word": 기록, "image": image_url})
    
    # 변경된 인증 데이터를 저장합니다.
    save_records(records)

    await ctx.send(f"✅ {ctx.author.mention}님의 운동 기록이 저장되었습니다!")

@bot.command()
async def 현황(ctx):
    users = load_users()  # 사용자 정보 로드
    records = load_records()  # 운동 기록 로드
    current_week = get_week()  # 현재 주
    message = "**📊 이번 주 운동 인증 현황**\n"
    
    for user_id, user_info in users.items():
        # 현재 주 기록이 있으면 해당 사용자 인증 목록, 없으면 빈 리스트로 처리
        week_records = records.get(current_week, {}).get(user_id, [])
        
        # 인증 횟수를 계산 (인증 기록이 없으면 0회로 처리)
        count = len(week_records)
        
        # 사용자 정보와 인증 횟수 추가
        message += f"\n👤 {user_info['name']} - {count}회 인증\n"
        
        # 해당 사용자의 인증 기록이 있다면 상세 내역을 추가합니다.
        if count > 0:
            for entry in week_records:
                message += f"📅 {entry['date']} - {entry['word']} | [사진 보기]({entry['image']})\n"
        else:
            # 인증 기록이 없을 경우 표시 (0회 인증)
            message += "❌ 인증 기록이 없습니다.\n"
    
    await ctx.send(message)

@bot.command()
async def 벌금(ctx):
    PENALTY_AMOUNT = 10000  # 주당 벌금 금액
    users = load_users()
    records = load_records()
    current_week = get_week()
    penalty_data = {}

    # 각 등록 사용자에 대해 벌금을 계산합니다.
    for user_id, user_info in users.items():
        joined_week = user_info["joined_week"]
        total_penalty = 0

        # records에서 현재 주 이전의 모든 주를 확인합니다.
        for week, week_data in records.items():
            # 이번 주는 벌금 계산 대상에서 제외
            if week >= current_week:
                continue
            # 사용자가 가입하기 전에 존재한 주라면 계산하지 않습니다.
            if week < joined_week:
                continue

            # 해당 주에 사용자의 인증 기록을 가져오고, 없으면 빈 리스트로 처리
            user_week_records = week_data.get(user_id, [])
            # 만약 인증 횟수가 3회 미만이면 벌금 부과
            if len(user_week_records) < 3:
                total_penalty += PENALTY_AMOUNT

        if total_penalty > 0:
            penalty_data[user_info["name"]] = total_penalty

    # 벌금 내역 메시지 생성
    if penalty_data:
        message = "**💰 운동 인증 벌금 내역**\n"
        total = 0
        for name, amount in penalty_data.items():
            message += f"{name}: {amount}원\n"
            total += amount
        message += f"\n누적 벌금: {total}원 🤑"
    else:
        message = "아직 벌금이 없습니다! 모아서 바다로 갑시다 🌊"
    
    await ctx.send(message)

@bot.command()
async def 커맨드(ctx):
    message = """
    **사용 가능한 명령어들:**
- **!등록**: 사용자를 등록합니다.📋
- **!인증**: 운동 인증을 사진과 함께 기록합니다.📸\n > `!인증 [기록 내용]` (기록 내용을 생략하면 기본값 '오운완 💪🏻'으로 저장)
- **!현황**: 이번 주 운동 인증 현황을 확인합니다.📊
- **!벌금**: 운동 인증을 3회 미만으로 한 사용자들의 벌금을 확인합니다.💸
    """
    await ctx.send(message)

@bot.event
async def on_command_error(ctx, error):
    # CommandNotFound 오류가 발생했을 때
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ 존재하지 않는 명령어입니다. `!커맨드`를 입력하여 사용 가능한 명령어를 확인하세요.")

bot.run(os.getenv("API_KEY"))
