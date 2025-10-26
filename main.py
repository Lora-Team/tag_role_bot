import discord
from discord.ext import commands
import os
import sys
import csv
from datetime import datetime, timezone
from dotenv import load_dotenv


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        _ = before  # not used
        # attempt to get the respective tag role from the server
        role = discord.Guild.get_role(after.guild, 1409425360126349483)
        # if the role is not found, panic
        if not role:
            sys.exit("Role not found in server!")
        has_role = after.get_role(1409425360126349483)
        has_tag = after.primary_guild.tag == "LAMP"
        action = None
        if has_tag and not has_role:
            await after.add_roles(role, reason="User has LAMP tag")
            print(f"{after.name} has LAMP tag, added role")
            action = "added"
        elif has_role and not has_tag:
            await after.remove_roles(role, reason="User removed LAMP tag")
            print(f"{after.name} no longer has LAMP tag, removed role")
            action = "removed"

        if action:
            self.record_event(after, action)

    def record_event(self, member: discord.Member, action: str):
        """Record a single event (role added/removed) to a CSV file."""
        filename = "stats.csv"
        file_exists = os.path.isfile(filename)

        with open(filename, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            # write header if file is new
            if not file_exists:
                writer.writerow(["timestamp", "user_id", "user_name", "action"])
            writer.writerow(
                [datetime.now(timezone.utc).isoformat(), member.id, member.name, action]
            )
        print(f"Logged {action} event for {member.name}")


# Initialize your bot
# set intents
intents = discord.Intents.default()
intents.members = True
# get token
_ = load_dotenv()
tok = os.getenv("TOKEN")
if not tok:
    sys.exit("No env token found")
# start app
client = MyClient(intents=intents)
client.run(tok)
