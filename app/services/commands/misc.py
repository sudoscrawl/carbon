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

    async def _serverinfo(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        assert guild is not None

        ts = int(guild.created_at.timestamp())

        created = f"<t:{ts}:R>"

        embed = self.bot.embed_factory._build()

        if guild.icon:
            embed.set_author(name=guild.name, icon_url=guild.icon.url)
            embed.set_thumbnail(url=guild.icon.url)
        else:
            embed.set_author(name=guild.name)

        owner_id = guild.owner_id
        assert owner_id is not None
        owner = await guild.fetch_member(owner_id)

        embed.add_field_i18n(_("Owned By"), str(owner.mention))
        embed.add_field_i18n(_("Member Count"), str(guild.member_count))
        embed.add_field_i18n(
            _("Created At"),
            f"{guild.created_at.strftime('%a, %b %d, %Y %I:%M %p')} ({created})",
        )
        embed.add_field_i18n(
            _("Channels"),
            f"Text: **{len(guild.text_channels)}** \nVoice: **{len(guild.voice_channels)}**",
        )
        embed.add_field_i18n(_("Roles"), str(len(guild.roles)))
        embed.set_footer(text=f"ID: {guild.id}")

        await interaction.response.send_message(embed=embed)
