import os

import discord
import pendulum
import structlog
from discord import app_commands
from discord.ext import commands

from app.config import settings
from app.db.session import engine
from app.i18n.manager import I18nManager
from app.i18n.translator import Translator
from app.ui.embeds.error_embed import ErrorEmbed
from app.ui.embeds.log_embeds import LogEmbed
from app.utils.checks.not_bot import not_bot
from app.utils.consts.perm_label import PERMISSION_LABELS
from app.utils.core.custom_tree import CustomCommandTree
from app.utils.core.redis import redis_client
from app.utils.helpers.embed_factory import EmbedFactory


class Carbon(commands.Bot):
    """The main bot class for Carbon.

    Attributes:
        i18n (I18nManager): Manager for internationalization.
        embed_factory (EmbedFactory): Factory for creating localized embeds.
        tree (CustomCommandTree): Custom command tree for slash commands.
        debug (bool): Whether the bot is running in debug mode.
        logger (structlog.BoundLogger): Logger instance for the bot.
        redis (redis.Redis): Redis client instance.
    """

    def __init__(self, *, debug: bool = False, **kwargs):
        """Initializes the Carbon bot.

        Args:
            debug (bool): Whether to enable debug mode.
            **kwargs: Additional keyword arguments for commands.Bot.
        """
        self.i18n = I18nManager()
        self.embed_factory = EmbedFactory(self.i18n)
        self.error_embeds = ErrorEmbed(self.i18n)
        self.log_embeds = LogEmbed(self.i18n)
        self.tree: CustomCommandTree
        self.start_time = pendulum.now("UTC")

        self.debug = debug
        self.logger = structlog.get_logger().bind(component="bot")
        self.redis = redis_client

        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        intents.message_content = True

        discord.VoiceClient.warn_nacl = False
        discord.VoiceClient.warn_dave = False

        super().__init__(
            command_prefix="!",
            help_command=None,
            intents=intents,
            tree_cls=CustomCommandTree,
            **kwargs,
        )

    async def setup_hook(self) -> None:
        """Called by discord.py when the bot is setting up.
        Loads modules and initializes i18n.
        """
        self.logger.info("Running setup.....")
        await self.setup_modules()
        await self.init_i18n()
        self.tree.add_check(not_bot)
        self.tree.on_error = self.app_command_error
        self.logger.info("Setup completed, starting bot")

    async def init_i18n(self) -> None:
        """Initializes the i18n manager and sets the translator for the command tree."""
        await self.tree.set_translator(Translator(self.i18n))
        self.logger.info("I18n Setup completed")

    async def start(self, token: str | None = None, *, reconnect: bool = True) -> None:
        """Starts the bot with the configured token.

        Args:
            token (str | None): The bot token to use. Defaults to settings.bot_token.
            reconnect (bool): Whether to automatically reconnect on failure.
        """
        token = settings.bot_token
        self.logger.info("Launching Carbon")
        await super().start(token=token, reconnect=reconnect)

    async def close(self) -> None:
        """Closes the bot and cleans up resources (e.g., database engine)."""
        await super().close()
        await engine.dispose()

    async def setup_modules(self) -> None:
        """Recursively loads extensions from the predefined directories."""
        groups = ["app/modules/listeners", "app/modules/commands"]

        for group in groups:
            for root, _, files in os.walk(group):
                for file in files:
                    if file.endswith(".py") and file != "__init__.py":
                        path = os.path.relpath(os.path.join(root, file), group)
                        extension = f"{group.replace('/', '.')}.{path[:-3].replace(os.sep, '.')}"

                        try:
                            await self.load_extension(extension)
                            self.logger.info(f"Loaded extension: {extension}")
                        except Exception as e:
                            self.logger.error(f"Failed to load {extension}: {e}")

    async def app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        if isinstance(error, app_commands.MissingPermissions):
            perms = ", ".join(
                PERMISSION_LABELS.get(p, p.replace("_", " "))
                for p in error.missing_permissions
            )

            embed = self.error_embeds.missing_perms_embed(perms)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if isinstance(error, app_commands.BotMissingPermissions):
            perms = ", ".join(
                PERMISSION_LABELS.get(p, p.replace("_", " "))
                for p in error.missing_permissions
            )
            embed = self.error_embeds.bot_missing_perms_embed(perms)
            await interaction.response.send_message(embed=embed, ephemeral=True)
