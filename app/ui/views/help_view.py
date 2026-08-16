import contextlib
from typing import TYPE_CHECKING

import discord
from discord import ui

from app.i18n.marker import _
from app.utils.consts.branding import INVITE_LINK, JUNGLE_GREEN, SUPPORT_SERVER

if TYPE_CHECKING:
    from app.bot import Carbon

EMOJIS = {
    "Moderation": "🛡️",
    "Miscellaneous": "📦",
    "General": "⭐",
    "Management": "🔨",
}

DESCRIPTIONS = {
    "Moderation": _("Commands for managing members and server behavior."),
    "General": _("Commands for basic utility."),
    "Management": _("Commands for managing carbon configurations for this server."),
    "Miscellaneous": _("Miscellaneous set of commands."),
}


class HelpView(ui.View):
    def __init__(self, bot: "Carbon", interaction: discord.Interaction):
        super().__init__(timeout=120)
        self.bot = bot
        self.interaction = interaction
        self.add_item(HelpSelect(bot))
        self.add_item(
            ui.Button(
                label=_("Invite"),
                style=discord.ButtonStyle.link,
                url=INVITE_LINK,
            )
        )
        self.add_item(
            ui.Button(
                label=_("Support Server"),
                style=discord.ButtonStyle.link,
                url=SUPPORT_SERVER,
            )
        )

    async def on_timeout(self) -> None:
        for item in self.children:
            if isinstance(item, (ui.Button, ui.Select)):
                item.disabled = True

        with contextlib.suppress(Exception):
            await self.interaction.edit_original_response(view=self)


class HelpSelect(ui.Select):
    def __init__(self, bot: "Carbon"):
        self.bot = bot
        options = [
            discord.SelectOption(
                label=_("Home"),
                description=_("Return to the main help menu."),
                emoji="🏠",
            )
        ]

        ignored_cogs = [
            "guildeventcog",
            "connectioncog",
        ]

        for cog_name, _cog in bot.cogs.items():
            if cog_name.lower() in ignored_cogs:
                continue

            options.append(
                discord.SelectOption(
                    label=cog_name,
                    emoji=EMOJIS.get(cog_name, "📁"),
                    description=self.bot.i18n.gettext(
                        DESCRIPTIONS.get(cog_name, _("Commands for %(cog_name)s.")),
                        cog_name=cog_name,
                    ),
                )
            )

        super().__init__(
            placeholder=_("Select a category"),
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        selection = self.values[0]

        if selection == "Home":
            embed = self.bot.embed_factory._build(
                _("Use `/help <command>` to show information about a command."),
                color=JUNGLE_GREEN,
            )
            embed.set_title_i18n(_("📚 Help Menu"))
            embed.set_footer_i18n(_("Pick a category to browse available commands"))

            return await interaction.response.edit_message(
                embed=embed, view=HelpView(self.bot, interaction)
            )

        cog = self.bot.get_cog(selection)
        if not cog:
            return await interaction.response.send_message(
                _("Cog not found."), ephemeral=True
            )

        embed = self.bot.embed_factory._build(color=JUNGLE_GREEN)
        embed.set_title_i18n(
            _("%(emoji)s %(selection)s Commands"),
            emoji=EMOJIS.get(selection, "📁"),
            selection=selection,
        )

        description = self.bot.i18n.gettext(
            DESCRIPTIONS.get(selection, _("Commands for %(cog_name)s.")),
            cog_name=selection,
        )
        embed.description = f"-# {description}"

        found_any = False
        # Slash commands
        for cmd in cog.get_app_commands():
            embed.add_field(
                name=f"`/{cmd.name}`",
                value=cmd.description or _("No description provided."),
                inline=False,
            )
            found_any = True

        if not found_any:
            embed.description += _("\n\nNo commands available in this category.")

        await interaction.response.edit_message(
            embed=embed, view=HelpView(self.bot, interaction)
        )
        return None
