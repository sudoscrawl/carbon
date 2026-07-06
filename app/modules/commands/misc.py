import discord
from discord import app_commands
from discord.ext import commands

from app.bot import Carbon
from app.i18n.marker import _
from app.services.commands.misc import MiscService


class Miscellaneous(commands.Cog):
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot
        self.service = MiscService(self.bot)

    # AVATAR COMMAND

    @app_commands.command(
        name="avatar", description=app_commands.locale_str(_("Get avatar of a user."))
    )
    @app_commands.guild_only()
    @app_commands.describe(
        user=app_commands.locale_str(
            _("The user you want to view the avatar of. (Defaults to yourself)")
        )
    )
    async def _avatar(
        self, interaction: discord.Interaction, user: discord.Member | None = None
    ) -> None:
        await self.service._avatar(interaction, user)


async def setup(bot: Carbon):
    await bot.add_cog(Miscellaneous(bot))
