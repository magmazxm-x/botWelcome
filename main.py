import discord
from discord.ext import commands
import os  # เพิ่มบรรทัดนี้
from keep_alive import keep_alive
from easy_pil import Editor, load_image_with_retry, Font

# ตั้งค่าบอท
intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    # เปลี่ยนตัวเลขข้างล่างนี้ให้เป็น ID ห้องของคุณจริงๆ
    channel = bot.get_channel(1495616411647737916) 
    if channel is None:
        return

    try:
        background = Editor("background.png").resize((1100, 500))
        profile_image = load_image_with_retry(member.display_avatar.url)
        profile = Editor(profile_image).resize((250, 250)).circle_image()
        
        background.paste(profile, (425, 100))
        
        # ใช้ฟอนต์แบบ Standard เพื่อลดโอกาส Error บน Render
        font_large = Font.light(size=50)
        font_small = Font.light(size=30)
        
        background.text((550, 380), "WELCOME", color="white", font=font_large, align="center")
        background.text((550, 440), f"{member.name}", color="white", font=font_small, align="center")
        
        file = discord.File(fp=background.image_bytes, filename="welcome.png")
        await channel.send(f"ยินดีต้อนรับคุณ {member.mention} สู่เซิร์ฟเวอร์!", file=file)
    except Exception as e:
        print(f"Error: {e}")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1495616451527315476) # เปลี่ยน ID ให้ตรงกัน
    if channel is None:
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
        await channel.send(f"ลาก่อนนะคุณ {member.name}!", file=file)
    except Exception as e:
        print(f"Error: {e}")

keep_alive()
# ตรวจสอบว่าใน Render ตั้งค่า Environment Variable ชื่อ TOKEN ไว้แล้ว
token = os.getenv('TOKEN')
if token:
    bot.run(token)
else:
    print("Error: ไม่พบ TOKEN ใน Environment Variables")
