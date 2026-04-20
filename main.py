import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from easy_pil import Editor, load_image, Font # ใช้ load_image เฉยๆ

intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ บอทออนไลน์แล้ว: {bot.user.name}')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1495616411647737916)
    if not channel: return
    try:
        # 1. โหลดพื้นหลังและรูปโปรไฟล์
        background = Editor("background.png").resize((1100, 500))
        profile_img = load_image(member.display_avatar.url)
        profile = Editor(profile_img).resize((250, 250)).circle_image()
        
        # 2. วางรูปและข้อความ
        background.paste(profile, (425, 100))
        background.text((550, 380), "WELCOME", color="white", align="center")
        background.text((550, 440), f"{member.name}", color="white", align="center")
        
        # 3. ส่งรูป
        file = discord.File(fp=background.image_bytes, filename="welcome.png")
        await channel.send(f"ยินดีต้อนรับ {member.mention}!", file=file)
    except Exception as e:
        print(f"Error: {e}")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1495616451527315476)
    if not channel: return
    try:
        background = Editor("background.png").resize((1100, 500))
        profile_img = load_image(member.display_avatar.url)
        profile = Editor(profile_img).resize((250, 250)).circle_image()
        
        background.paste(profile, (425, 100))
        background.text((550, 380), "GOODBYE", color="red", align="center")
        background.text((550, 440), f"{member.name}", color="white", align="center")
        
        file = discord.File(fp=background.image_bytes, filename="goodbye.png")
        await channel.send(f"ลาก่อน {member.name}!", file=file)
    except Exception as e:
        print(f"Error: {e}")

keep_alive()
bot.run(os.getenv('TOKEN'))
