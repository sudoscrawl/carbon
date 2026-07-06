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
        await interaction.response.defer()
        user = user or interaction.user
        avatar = user.display_avatar

        embed = self.bot.embed_factory._build()
        embed.set_author_i18n(
            _("%(username)s's Avatar"), username=user.name, icon_url=avatar.url
        )
        embed.set_image(url=avatar.url)

        await interaction.followup.send(embed=embed)
