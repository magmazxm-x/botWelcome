import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from easy_pil import Editor, load_image_with_retry, Font

# 1. ตั้งค่า Intents ให้มองเห็นสมาชิก
intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'--- บอทออนไลน์แล้วในชื่อ: {bot.user.name} ---')

@bot.event
async def on_member_join(member):
    # เลขห้องที่คุณส่งมา (Welcome)
    channel_id = 1495616411647737916 
    channel = bot.get_channel(channel_id)
    if not channel:
        return

    try:
        # โหลดพื้นหลัง (ขนาดควรสัมพันธ์กับ 1100x500 เพื่อความสวยงาม)
        background = Editor("background.png").resize((1100, 500))
        
        # โหลดรูปโปรไฟล์และตัดวงกลม
        profile_image = load_image_with_retry(member.display_avatar.url)
        profile = Editor(profile_image).resize((250, 250)).circle_image()
        
        # วางรูปโปรไฟล์ไว้ตรงกลาง
        background.paste(profile, (425, 100))
        
        # ใส่ข้อความ (ใช้ Font.light เพื่อความปลอดภัยบน Linux)
        font_large = Font.light(size=50)
        font_small = Font.light(size=30)
        
        background.text((550, 380), "WELCOME", color="white", font=font_large, align="center")
        background.text((550, 440), f"{member.name}", color="white", font=font_small, align="center")
        
        # ส่งรูป
        file = discord.File(fp=background.image_bytes, filename="welcome.png")
        await channel.send(f"ยินดีต้อนรับคุณ {member.mention} เข้าสู่เซิร์ฟเวอร์ครับ!", file=file)
    except Exception as e:
        print(f"เกิดข้อผิดพลาดตอนคนเข้า: {e}")

@bot.event
async def on_member_remove(member):
    # เลขห้องที่คุณส่งมา (Goodbye)
    channel_id = 1495616451527315476 
    channel = bot.get_channel(channel_id)
    if not channel:
        return

    try:
        background = Editor("background.png").resize((1100, 500))
        profile_image = load_image_with_retry(member.display_avatar.url)
        profile = Editor(profile_image).resize((250, 250)).circle_image()
        
        background.paste(profile, (425, 100))
        
        font_large = Font.light(size=50)
        background.text((550, 380), "GOODBYE", color="red", font=font_large, align="center")
        background.text((550, 440), f"{member.name}", color="white", font=font_large, align="center")
        
        file = discord.File(fp=background.image_bytes, filename="goodbye.png")
        await channel.send(f"ลาก่อนนะคุณ {member.name} แล้วพบกันใหม่!", file=file)
    except Exception as e:
        print(f"เกิดข้อผิดพลาดตอนคนออก: {e}")

# เริ่มระบบ Keep Alive เพื่อไม่ให้บอทหลับ
keep_alive()

# ดึง Token จาก Environment Variables ของ Render
token = os.getenv('TOKEN')
if token:
    bot.run(token)
else:
    print("Error: ไม่พบตัวแปร TOKEN ในหน้า Settings ของ Render")
