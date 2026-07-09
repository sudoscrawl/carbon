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

    avatar = app_commands.Group(
        name="avatar", description=app_commands.locale_str(_("Get avatar of a user."))
    )

    @avatar.command(
        name="get", description=app_commands.locale_str(_("Get avatar of a user."))
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

    @avatar.command(
        name="guild",
        description=app_commands.locale_str(_("Get the guild avatar of a user.")),
    )
    @app_commands.guild_only()
    @app_commands.describe(
        user=app_commands.locale_str(
            _("The user you want to view the avatar of. (Defaults to yourself)")
        )
    )
    async def _avatar_guild(
        self, intercation: discord.Interaction, user: discord.Member | None = None
    ) -> None:
        await self.service._avatar_guild(intercation, user)

    @avatar.command(
        name="user",
        description=app_commands.locale_str(_("Get the main avatar of a user.")),
    )
    @app_commands.guild_only()
    @app_commands.describe(
        user=app_commands.locale_str(
            _("The user you want to view the avatar of. (Defaults to yourself)")
        )
    )
    async def _avatar_user(
        self, interaction: discord.Interaction, user: discord.Member | None = None
    ) -> None:
        await self.service._avatar_user(interaction, user)

    # SERVER INFO COMMAND

    @app_commands.command(
        name="serverinfo",
        description=app_commands.locale_str(
            _("Get information about the server in which this command is executed.")
        ),
    )
    @app_commands.guild_only()
    async def _serverinfo(self, interaction: discord.Interaction):
        await self.service._serverinfo(interaction)


async def setup(bot: Carbon):
    await bot.add_cog(Miscellaneous(bot))
