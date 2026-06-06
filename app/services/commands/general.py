from typing import Any

import discord
from discord.ext import commands

from app.bot import Carbon
from app.i18n.marker import _
from app.ui.views.help_view import HelpView
from app.ui.views.invite_view import InviteView
from app.utils.consts.branding import CARBON_LOGO, JUNGLE_GREEN


class GeneralService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def _ping(self, interaction: discord.Interaction) -> None:
        latency = round(self.bot.latency * 1000)

        embed = self.bot.embed_factory._build().add_field_i18n(
            _("Latency"), _("%(latency)s ms"), latency=latency
        )

        await interaction.response.send_message(embed=embed)

    async def _invite(self, interaction: discord.Interaction) -> None:
        embed = self.bot.embed_factory._build(
            _("Click the button below to invite the bot to your server.")
        )
        embed.set_title_i18n(_("Thank you for taking interest in Carbon"))

        view = InviteView(interaction)
        await interaction.response.send_message(embed=embed, view=view)

    async def _about(self, interaction: discord.Interaction) -> None:
        uptime = self.bot.start_time.diff_for_humans()
        server_count = len(self.bot.guilds)
        user_count = sum(guild.member_count or 0 for guild in self.bot.guilds)

        embed = self.bot.embed_factory._build(color=JUNGLE_GREEN)
        embed.set_title_i18n(_("%(emoji)s About Carbon"), emoji=CARBON_LOGO)

        embed.add_field_i18n(_("Servers"), str(server_count))
        embed.add_field_i18n(_("Users"), str(user_count))
        embed.add_field_i18n(_("Last Restart"), f"`{uptime}`")

        await interaction.response.send_message(embed=embed)
        return

    async def _help(
        self, interaction: discord.Interaction, command: str | None = None
    ) -> None:
        if command:
            # Handle specific command help
            cmd_obj: (
                commands.Command[Any, Any, Any]
                | discord.app_commands.Command[Any, ..., Any]
                | discord.app_commands.Group
                | discord.app_commands.ContextMenu
                | None
            ) = None

            # Check for regular commands first
            cmd_obj = self.bot.get_command(command)

            # If not found, check for app commands
            if not cmd_obj:
                for app_cmd in self.bot.tree.get_commands():
                    if app_cmd.name == command:
                        cmd_obj = app_cmd
                        break

            if not cmd_obj:
                await interaction.response.send_message(
                    _("Command not found."), ephemeral=True
                )
                return

            embed = self.bot.embed_factory._build(color=JUNGLE_GREEN)
            embed.set_title_i18n(_("Command Information"))

            description = ""
            if isinstance(cmd_obj, discord.app_commands.Command):
                description = cmd_obj.description
            elif isinstance(cmd_obj, commands.Command):
                description = str(cmd_obj.help)
            elif isinstance(cmd_obj, discord.app_commands.Group):
                description = cmd_obj.description
            elif isinstance(cmd_obj, discord.app_commands.ContextMenu):
                description = ""  # Context menus don't have a description property in the same way

            embed.add_field_i18n(
                _("Description"),
                _("> %(description)s"),
                description=description or _("No description."),
            )

            # Aliases (for traditional commands only)
            if isinstance(cmd_obj, commands.Command) and cmd_obj.aliases:
                aliases = [f"`!{command}`"] + [
                    f"`!{alias}`" for alias in cmd_obj.aliases
                ]
                embed.add_field_i18n(
                    _("Aliases"), _("> %(aliases)s"), aliases=", ".join(aliases)
                )

            # Usage
            usage = ""
            if isinstance(cmd_obj, discord.app_commands.Command):
                params = []
                for param in cmd_obj.parameters:
                    if param.required:
                        params.append(f"<{param.name}>")
                    else:
                        params.append(f"[{param.name}]")
                usage = f"> `/{cmd_obj.name} {' '.join(params)}`"
            elif isinstance(cmd_obj, commands.Command):
                params = []
                for name, param in cmd_obj.clean_params.items():
                    if param.default is param.empty:
                        params.append(f"<{name}>")
                    else:
                        params.append(f"[{name}]")
                usage = f"> `!{cmd_obj.name} {' '.join(params)}`"

            if usage:
                embed.add_field_i18n(_("Usage"), usage)

            await interaction.response.send_message(embed=embed)
            return

        # Handle main help menu
        embed = self.bot.embed_factory._build(
            _("Use `/help <command>` to show information about a command."),
            color=JUNGLE_GREEN,
        )
        embed.set_title_i18n(_("📚 Help Menu"))
        embed.set_footer_i18n(_("Pick a category to browse available commands"))

        view = HelpView(self.bot, interaction)
        await interaction.response.send_message(embed=embed, view=view)
        return
