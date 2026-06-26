import re

import discord


def is_author_bot(message: discord.Message) -> bool:
    return message.author.bot


def is_author_human(message: discord.Message) -> bool:
    return not message.author.bot


def does_message_contain_embed(message: discord.Message) -> bool:
    return len(message.embeds) != 0


def is_image_attached(message: discord.Message) -> bool:
    if message.attachments:
        for i in message.attachments:
            if i.content_type and i.content_type.startswith("image/"):
                return True
    return False


def contains_invite(content: str) -> bool:
    invite_pattern = re.compile(
        r"(?:https?://)?(?:www\.)?discord(?:app)?\.(?:com|gg)/(?:invite/)?[a-zA-Z0-9_-]+"
    )
    return bool(invite_pattern.search(content))


def is_invite_included(message: discord.Message) -> bool:
    return contains_invite(message.content)
