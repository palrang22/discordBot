import discord
from discord.ext import commands
from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# 저장소 인스턴스 생성
from adapters.repositories.user_repository import UserRepository
from adapters.repositories.record_repository import RecordRepository

user_repo = UserRepository()
record_repo = RecordRepository()

# 유스케이스 임포트
from core.usecases.register_user import RegisterUserUseCase
from core.usecases.record_workout import RecordWorkoutUseCase
from core.usecases.get_status import GetStatusUseCase
from core.usecases.calculate_penalty import CalculatePenaltyUseCase

@bot.event
async def on_ready():
    print(f"✅ 로그인 성공: {bot.user}")

# 명령어
@bot.command()
async def 승희(ctx):
    await ctx.send("엔젤 💫")

@bot.command()
async def 등록(ctx):
    print(f"등록 요청: {ctx.author.id} - {ctx.author.name}")
    uc = RegisterUserUseCase(user_repo)
    try:
        success, message = uc.execute(str(ctx.author.id), ctx.author.name)
        print(f"등록 결과: {success}, 메시지: {message}")
        await ctx.send(message)
    except Exception as e:
        print(f"에러 발생: {e}")
        await ctx.send(f"등록 처리 중 오류가 발생했습니다: {e}")


@bot.command()
async def 인증(ctx, *, 기록: str = None):
    print("인증 커맨드 호출됨")
    if not ctx.message.attachments:
        await ctx.send("❌ 운동 인증 사진을 함께 올려주세요!")
        return
    image_url = ctx.message.attachments[0].url

    uc = RecordWorkoutUseCase(user_repo, record_repo)
    success, message = uc.execute(str(ctx.author.id), 기록, image_url)
    if success:
        status_uc = GetStatusUseCase(user_repo, record_repo)
        user_status = status_uc.execute(str(ctx.author.id))
        count = user_status["count"]
        print("인증 커맨드 호출됨 - 운동 기록 저장 완료")
        await ctx.send(f"✅ 운동 기록이 저장되었습니다! {ctx.author.mention}님의 이번 주 운동 횟수: {count}회")
    else:
        print("인증 커맨드 호출됨 - 운동 기록 저장 실패")
        await ctx.send(f"❌{ctx.author.mention}님은 {message}")

@bot.command()
async def 현황(ctx):
    print("현황 커맨드 호출됨")
    try:
        uc = GetStatusUseCase(user_repo, record_repo)
        print(f"현황 커맨드 호출됨 - GetstatusUseCase 호출됨: {user_repo}, {record_repo}")
        status = uc.execute()
        msg = "**📊 이번 주 운동 인증 현황**\n"
        for user_id, data in status.items():
            count = data["count"]
            msg += f"\n👤 {data["name"]} - {count}회 인증\n"
            if count > 0:
                for entry in data["records"]:
                    msg += f"📅 {entry['date']} - {entry['word']} | [사진 보기]({entry['image']})\n"
            else:
                msg += "❌ 인증 기록이 없습니다.\n"
        await ctx.send(msg)
        print("현황 메시지 전송 완료")
    except Exception as e:
        print(f"현황 커맨드 호출중 오류 발생: {e}")
        await ctx.send("🚨 현황 호출중 오류가 발생했습니다.")

@bot.command()
async def 벌금(ctx):
    print('벌금 커맨드 호출됨')
    uc = CalculatePenaltyUseCase(user_repo, record_repo)
    print(f"벌금 커맨드 호출됨 - CalculatePenaltyUseCase 호출됨: {user_repo}, {record_repo}")
    penalty_data = uc.execute()
    if penalty_data:
        msg = "**💰 운동 인증 벌금 내역**\n"
        total = 0
        for name, amount in penalty_data.items():
            msg += f"{name}: {amount}원\n"
            total += amount
        msg += f"\n누적 벌금: {total}원 🤑"
    else:
        msg = "아직 벌금이 없습니다! 모아서 바다로 갑시다 🌊"
    await ctx.send(msg)

@bot.command()
async def 커맨드(ctx):
    message = """
**사용 가능한 명령어들:**

- **!등록**: 사용자를 등록합니다. 📋  
- **!인증**: 운동 인증을 사진과 함께 기록합니다. 📸  
   > `!인증 [기록 내용]` (기록 생략 시 기본값 '오운완 💪🏻')  
- **!현황**: 이번 주 운동 인증 현황을 확인합니다. 📊  
- **!벌금**: 누적 벌금과 사용자별 벌금을 확인합니다. 💸

이스터에그가 숨겨져 있을수도...?🪺
    """
    await ctx.send(message)

@bot.event
async def on_command_error(ctx, error):
    from discord.ext.commands import CommandNotFound
    if isinstance(error, CommandNotFound):
        await ctx.send("❌ 존재하지 않는 명령어입니다. `!커맨드`를 입력하여 사용 가능한 명령어를 확인하세요.")

if __name__ == "__main__":
    bot.run(os.getenv("API_KEY"))
