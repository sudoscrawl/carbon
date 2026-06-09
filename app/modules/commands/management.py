import discord
from discord import app_commands
from discord.ext import commands

from app.bot import Carbon
from app.i18n.marker import _
from app.services.commands.management import ManagementService


class Management(commands.Cog):
    def __init__(self, bot: Carbon):
        self.bot = bot
        self.service = ManagementService(self.bot)

    purge = app_commands.Group(
        name="purge", description=app_commands.locale_str(_("Delete messages in bulk."))
    )

    @purge.command(
        name="any", description=app_commands.locale_str(_("Delete any message type."))
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.describe(
        count=app_commands.locale_str(_("The max number of messages to get deleted."))
    )
    async def _purge(self, interaction: discord.Interaction, count: int) -> None:
        await self.service._purge(interaction, count)

    @app_commands.command(
        name="set-modlog-channel",
        description=app_commands.locale_str(
            _("Set a channel to receive moderation logs.")
        ),
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.describe(
        channel=app_commands.locale_str(_("The channel to receive logs."))
    )
    async def set_modlog_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel | None
    ) -> None:
        assert isinstance(interaction.channel, discord.TextChannel)
        channel = channel or interaction.channel
        await self.service._set_modlog_channel(interaction, channel)


async def setup(bot: Carbon):
    await bot.add_cog(Management(bot))
