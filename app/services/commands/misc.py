import discord

from app.bot import Carbon
from app.i18n.marker import _


class MiscService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def _avatar(
        self, interaction: discord.Interaction, user: discord.Member | None = None
    ) -> None:
        assert isinstance(interaction.user, discord.Member)
        user = user or interaction.user
        avatar = user.display_avatar

        embed = self.bot.embed_factory._build()
        embed.set_author_i18n(
            _("%(username)s's Avatar"), username=user.name, icon_url=avatar.url
        )
        embed.set_image(url=avatar.url)

        await interaction.response.send_message(embed=embed)

    async def _avatar_guild(
        self, interaction: discord.Interaction, user: discord.Member | None = None
    ) -> None:
        assert isinstance(interaction.user, discord.Member)
        user = user or interaction.user

        avatar = user.guild_avatar

        if avatar is None:
            err_embed = self.bot.embed_factory.error_embed(
                _("The user does not have a guild avatar.")
            )
            await interaction.response.send_message(embed=err_embed, ephemeral=True)
            return

        embed = self.bot.embed_factory._build()
        embed.set_author_i18n(
            _("%(username)s's Guild Avatar"), username=user.name, icon_url=avatar.url
        )
        embed.set_image(url=avatar.url)

        await interaction.response.send_message(embed=embed)

    async def _avatar_user(
        self, interaction: discord.Interaction, user: discord.Member | None = None
    ) -> None:
        assert isinstance(interaction.user, discord.Member)
        user = user or interaction.user

        avatar = user.default_avatar
        embed = self.bot.embed_factory._build()
        embed.set_author_i18n(
            _("%(username)s's Main Avatar"), username=user.name, icon_url=avatar.url
        )
        embed.set_image(url=avatar.url)

        await interaction.response.send_message(embed=embed)
