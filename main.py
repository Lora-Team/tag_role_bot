import discord
from discord.ext import commands
import os
from dotenv import load_dotenv


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_member_update(self, after: discord.Member):
        # attempt to get the respective tag role from the server
        role = discord.Guild.get_role(after.guild, 1409425360126349483)
        # if the role is not found
        if not role:
            print("role not found in server!")
            return
        # if the user updates their tag to "LAMP"
        if after.primary_guild.tag == "LAMP":
            # add the role to the user
            await after.add_roles(role, reason="User has lamp tag")
            print(f"{after.name} has lamp tag")
        else:
            # ensure the user does have the role
            if not after.get_role(1409425360126349483):
                print(f"{after.name} didn't have lamp role")
                return
            # remove the role
            await after.remove_roles(role, reason="User removed lamp tag")
            print(f"{after.name} no longer has lamp tag and the role was removed")


# Initialize your bot
# set intents
intents = discord.Intents.default()
intents.members = True
# get token
load_dotenv()
tok = os.getenv("TOKEN")
if not tok:
    os._exit(1)
# start app
client = MyClient(intents=intents)
client.run(tok)
