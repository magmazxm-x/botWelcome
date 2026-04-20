import discord
from discord.ext import commands
from keep_alive import keep_alive
from easy_pil import Editor, load_image_with_retry, Font

# ตั้งค่าบอท
intents = discord.Intents.default()
intents.members = True  # สำคัญมาก: ต้องเปิด Server Members Intent ใน Discord Developer Portal
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    # กำหนด Channel ID ที่ต้องการให้บอทส่งรูป
    channel = bot.get_channel(123456789012345678) # ใส่ ID ของห้องแชทที่นี่
    
    # สร้างรูป Welcome
    background = Editor("background.png").resize((1100, 500))
    
    # ดึงรูปโปรไฟล์ (ตัดเป็นวงกลม)
    profile_image = load_image_with_retry(member.display_avatar.url)
    profile = Editor(profile_image).resize((250, 250)).circle_image()
    
    # วางรูปโปรไฟล์ไว้ตรงกลาง (X: 425, Y: 100 โดยประมาณ)
    background.paste(profile, (425, 100))
    
    # เพิ่มชื่อผู้ใช้ด้านล่างโปรไฟล์
    font_large = Font.light(size=50)
    font_small = Font.poppins(size=30, variant="light")
    
    background.text((550, 380), f"WELCOME", color="white", font=font_large, align="center")
    background.text((550, 440), f"{member.name}", color="white", font=font_small, align="center")
    
    # ส่งรูปภาพ
    file = discord.File(fp=background.image_bytes, filename="welcome.png")
    await channel.send(f"ยินดีต้อนรับคุณ {member.mention} สู่เซิร์ฟเวอร์ของเรา!", file=file)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(123456789012345678) # ใส่ ID เดียวกับข้างบน
    
    background = Editor("background.png").resize((1100, 500))
    profile_image = load_image_with_retry(member.display_avatar.url)
    profile = Editor(profile_image).resize((250, 250)).circle_image()
    
    background.paste(profile, (425, 100))
    
    font_large = Font.poppins(size=50, variant="bold")
    background.text((550, 380), f"GOODBYE", color="red", font=font_large, align="center")
    background.text((550, 440), f"{member.name}", color="white", font=font_large, align="center")
    
    file = discord.File(fp=background.image_bytes, filename="goodbye.png")
    await channel.send(f"ลาก่อนนะคุณ {member.name} แล้วเจอกันใหม่!", file=file)
    
keep_alive() # เรียกใช้งานฟังก์ชัน keep_alive
bot.run(os.getenv('TOKEN'))
