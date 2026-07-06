import discord
from discord import app_commands
from discord.ext import commands

from app.bot import Carbon
from app.i18n.marker import _
from app.services.commands.moderation import ModCmdService


class Moderation(commands.Cog):
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot
        self.service = ModCmdService(self.bot)

    # KICK COMMAND

    @app_commands.command(
        name="kick",
        description=app_commands.locale_str(_("Kick someone from this server.")),
    )
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(kick_members=True)
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(
        target=app_commands.locale_str(_("The user you want to kick.")),
        reason=app_commands.locale_str(_("Your reason to kick them. (Optional)")),
    )
    async def kick(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        reason: str = "No reason provided.",
    ):
        await self.service._kick(interaction, target, reason)

    # BAN COMMAND

    @app_commands.command(
        name="ban",
        description=app_commands.locale_str(_("Ban someone from this server.")),
    )
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(
        target=app_commands.locale_str(_("The user you want to ban.")),
        reason=app_commands.locale_str(_("Your reason to ban them. (Optional)")),
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        reason: str = "No reason provided.",
    ):
        await self.service._ban(interaction, target, reason)

    # UNBAN COMMAND

    @app_commands.command(
        name="unban",
        description=app_commands.locale_str(_("Unban someone from this server.")),
    )
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(
        user_id=app_commands.locale_str(
            _("Discord ID of the person you want to unban.")
        ),
        reason=app_commands.locale_str(_("Your reason to unban them. (Optional)")),
    )
    async def unban(
        self,
        interaction: discord.Interaction,
        user_id: str,
        reason: str = "No reason provided.",
    ):
        await self.service._unban(interaction, user_id, reason)

    # TIMEOUT COMMAND

    @app_commands.command(
        name="timeout",
        description=app_commands.locale_str(_("Timeout someone in this server.")),
    )
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(moderate_members=True)
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.describe(
        target=app_commands.locale_str(_("The user you want to timeout.")),
        duration=app_commands.locale_str(
            _("The duration for which you want to timeout them.")
        ),
        reason=app_commands.locale_str(_("Your reason to timeout them. (Optional)")),
    )
    async def timeout(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        duration: str,
        reason: str = "No reason provided.",
    ):
        await self.service._timeout(interaction, target, duration, reason)

    # WARN COMMAND

    @app_commands.command(
        name="warn",
        description=app_commands.locale_str(_("Warn a member of this server.")),
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(
        target=app_commands.locale_str(_("The user you want to warn.")),
        reason=app_commands.locale_str(_("Your reason to warn them. (Optional)")),
    )
    async def warn(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        reason: str = "No reason provided.",
    ):
        await self.service._warn(interaction, target, reason)


async def setup(bot: Carbon):
    await bot.add_cog(Moderation(bot))
