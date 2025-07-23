import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
intents.presences = False
intents.messages = True
intents.guild_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Set your supporter roles here
PROTECTED_ROLES = [
    "Top GigaChad",
    "Clout Commander",
    "Lil Flex",
    "Exalted Premium",
    "Ol' Lady",
    "Premium Members"
]

# Name of the channel to send alerts to
LOG_CHANNEL_NAME = "mod-logs"

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_member_update(before, after):
    if before.roles == after.roles:
        return

    added_roles = [role for role in after.roles if role not in before.roles]
    removed_roles = [role for role in before.roles if role not in after.roles]

    for role in added_roles + removed_roles:
        if role.name in PROTECTED_ROLES:
            guild = after.guild
            log_channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)

            if log_channel:
                action = "added to" if role in added_roles else "removed from"

                # Find who did it using audit logs
                async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.member_role_update):
                    if entry.target.id == after.id and role in entry.changes.after:
                        actor = entry.user
                        break
                else:
                    actor = "Unknown"

                await log_channel.send(
                    f"⚠️ **{role.name}** was {action} `{after.name}` by `{actor}`."
                )

                # OPTIONAL: Revert the role change
                # if role in added_roles:
                #     await after.remove_roles(role)
                #     await log_channel.send(f"🔄 Reverted: Removed `{role.name}` from `{after.name}`.")
                # elif role in removed_roles:
                #     await after.add_roles(role)
                #     await log_channel.send(f"🔄 Reverted: Re-added `{role.name}` to `{after.name}`.")

# Run your bot
bot.run("YOUR_BOT_TOKEN")
