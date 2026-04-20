import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
# แก้บรรทัดนี้: เอา load_image_with_retry ออก แล้วใส่ load_image แทน
from easy_pil import Editor, load_image, Font 

intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Online as: {bot.user.name}')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1495616411647737916)
    if not channel: return
    try:
        background = Editor("background.png").resize((1100, 500))
        
        # แก้บรรทัดนี้: ใช้ load_image แทน
        profile_img = load_image(member.display_avatar.url) 
        profile = Editor(profile_img).resize((250, 250)).circle_image()
        
        background.paste(profile, (425, 100))
        
        background.text((550, 380), "WELCOME", color="white", align="center")
        background.text((550, 440), f"{member.name}", color="white", align="center")
        
        file = discord.File(fp=background.image_bytes, filename="welcome.png")
        await channel.send(f"ยินดีต้อนรับคุณ {member.mention} สู่เซิร์ฟเวอร์!", file=file)
    except Exception as e:
        print(f"Error Join: {e}")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1495616451527315476)
    if not channel: return
    try:
        background = Editor("background.png").resize((1100, 500))
        
        # แก้บรรทัดนี้: ใช้ load_image แทน
        profile_img = load_image(member.display_avatar.url)
        profile = Editor(profile_img).resize((250, 250)).circle_image()
        
        background.paste(profile, (425, 100))
        
        background.text((550, 380), "GOODBYE", color="red", align="center")
        background.text((550, 440), f"{member.name}", color="white", align="center")
        
        file = discord.File(fp=background.image_bytes, filename="goodbye.png")
        await channel.send(f"ลาก่อนคุณ {member.name}!", file=file)
    except Exception as e:
        print(f"Error Leave: {e}")

keep_alive()
token = os.getenv('TOKEN')
if token:
    bot.run(token)
else:
    print("❌ Token not found")
