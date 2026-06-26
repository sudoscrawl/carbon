import discord

import app.utils.checks.purge_checks as purge_checks
from app.bot import Carbon
from app.db.services.modsettings_service import ModSettingsService
from app.db.session import session_maker
from app.i18n.marker import _


class ManagementService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    # PURGE COMMAND GROUP
    async def _purge(self, interaction: discord.Interaction, count: int) -> None:
        assert isinstance(interaction.channel, discord.TextChannel)
        await interaction.response.defer(ephemeral=True)
        if count <= 0 or count > 100:
            embed = self.bot.embed_factory.error_embed(
                _("The message count must be between 1 and 100.")
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        deleted = await interaction.channel.purge(limit=count)

        embed = self.bot.embed_factory.success_embed(
            _("Deleted %(count)s messages."), count=len(deleted)
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def _purge_bots(self, interaction: discord.Interaction, count: int) -> None:
        assert isinstance(interaction.channel, discord.TextChannel)
        await interaction.response.defer(ephemeral=True)
        if count <= 0 or count > 100:
            embed = self.bot.embed_factory.error_embed(
                _("The message count must be between 1 and 100.")
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        deleted = 0

        async for message in interaction.channel.history(limit=500):
            if purge_checks.is_author_bot(message):
                await message.delete()
                deleted += 1

                if deleted >= count:
                    break

        embed = self.bot.embed_factory.success_embed(
            _("Deleted %(count)s messages."), count=deleted
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def _purge_humans(self, interaction: discord.Interaction, count: int) -> None:
        assert isinstance(interaction.channel, discord.TextChannel)
        await interaction.response.defer(ephemeral=True)
        if count <= 0 or count > 100:
            embed = self.bot.embed_factory.error_embed(
                _("The message count must be between 1 and 100.")
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        deleted = 0

        async for message in interaction.channel.history(limit=500):
            if purge_checks.is_author_human(message):
                await message.delete()
                deleted += 1

                if deleted >= count:
                    break

        embed = self.bot.embed_factory.success_embed(
            _("Deleted %(count)s messages."), count=deleted
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def _purge_embeds(self, interaction: discord.Interaction, count: int) -> None:
        assert isinstance(interaction.channel, discord.TextChannel)
        await interaction.response.defer(ephemeral=True)
        if count <= 0 or count > 100:
            embed = self.bot.embed_factory.error_embed(
                _("The message count must be between 1 and 100.")
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        deleted = 0

        async for message in interaction.channel.history(limit=500):
            if purge_checks.does_message_contain_embed(message):
                await message.delete()
                deleted += 1

                if deleted >= count:
                    break

        embed = self.bot.embed_factory.success_embed(
            _("Deleted %(count)s messages."), count=deleted
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def _purge_images(self, interaction: discord.Interaction, count: int) -> None:
        assert isinstance(interaction.channel, discord.TextChannel)
        await interaction.response.defer(ephemeral=True)
        if count <= 0 or count > 100:
            embed = self.bot.embed_factory.error_embed(
                _("The message count must be between 1 and 100.")
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        deleted = 0
        async for message in interaction.channel.history(limit=500):
            if purge_checks.is_image_attached(message):
                await message.delete()
                deleted += 1

                if deleted >= count:
                    break

        embed = self.bot.embed_factory.success_embed(
            _("Deleted %(count)s messages."), count=deleted
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def _purge_invites(
        self, interaction: discord.Interaction, count: int
    ) -> None:
        assert isinstance(interaction.channel, discord.TextChannel)
        await interaction.response.defer(ephemeral=True)
        if count <= 0 or count > 100:
            embed = self.bot.embed_factory.error_embed(
                _("The message count must be between 1 and 100.")
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        deleted = 0
        async for message in interaction.channel.history(limit=500):
            if purge_checks.is_invite_included(message):
                await message.delete()
                deleted += 1

                if deleted >= count:
                    break

        embed = self.bot.embed_factory.success_embed(
            _("Deleted %(count)s messages."), count=deleted
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def _set_modlog_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ) -> None:
        await interaction.response.defer(ephemeral=True)
        async with session_maker() as session, session.begin():
            assert interaction.guild is not None
            await ModSettingsService.set_log_channel_id(
                session, interaction.guild.id, channel.id
            )
        try:
            embed = self.bot.embed_factory.success_embed(
                _("Succesfully set %(channel_mention)s to receive moderation logs."),
                channel_mention=channel.mention,
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            print(e)
