import discord
from discord import Interaction, app_commands
from discord.app_commands import locale_str
from discord.ext import commands

from app.bot import Carbon
from app.i18n.marker import _
from app.services.commands.general import GeneralService


class General(commands.Cog):
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot
        self.service = GeneralService(self.bot)

    # -- ping command --
    @app_commands.command(
        name="ping", description=locale_str(_("Check the bot latency."))
    )
    @app_commands.guild_only()
    async def ping(self, interaction: Interaction) -> None:
        await self.service._ping(interaction)

    # -- invite command --
    @app_commands.command(
        name="invite", description=locale_str(_("Get an invite link for Carbon."))
    )
    @app_commands.guild_only()
    async def invite(self, interaction: discord.Interaction) -> None:
        await self.service._invite(interaction)

    # -- about command --
    @app_commands.command(
        name="about", description=locale_str(_("Get information about Carbon."))
    )
    @app_commands.guild_only()
    async def about(self, interaction: discord.Interaction) -> None:
        await self.service._about(interaction)

    # -- help autocomplete --
    async def help_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list:
        commands = [cmd.qualified_name for cmd in self.bot.tree.walk_commands()]

        return [
            app_commands.Choice(name=cmd, value=cmd)
            for cmd in commands
            if current.lower() in cmd.lower()
        ][:25]

    # -- help command --
    @app_commands.command(
        name="help", description=locale_str(_("Get a list of all my commands."))
    )
    @app_commands.guild_only()
    @app_commands.autocomplete(command=help_autocomplete)
    @app_commands.describe(command="The command to get help for.")
    async def help(
        self, interaction: discord.Interaction, command: str | None = None
    ) -> None:
        await self.service._help(interaction, command)


async def setup(bot: Carbon):
    await bot.add_cog(General(bot))
