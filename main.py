import discord
from discord.ext import commands
import os
import sys
from dotenv import load_dotenv


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        # attempt to get the respective tag role from the server
        role = discord.Guild.get_role(after.guild, 1409425360126349483)
        # if the role is not found, panic
        if not role:
            sys.exit("Role not found in server!")
        # if the user updates their tag to "LAMP" then add the role
        if after.primary_guild.tag == "LAMP":
            await after.add_roles(role, reason="User has lamp tag")
            print(f"{after.name} has lamp tag, added role")
        elif after.get_role(1409425360126349483):
            # if the user has the role and their tag is not lamp then remove the role
            await after.remove_roles(role, reason="User removed lamp tag")
            print(f"{after.name} no longer has lamp tag, removed role")


# Initialize your bot
# set intents
intents = discord.Intents.default()
intents.members = True
# get token
load_dotenv()
tok = os.getenv("TOKEN")
if not tok:
    sys.exit("No env token found")
# start app
client = MyClient(intents=intents)
client.run(tok)
