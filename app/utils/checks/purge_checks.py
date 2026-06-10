import discord


def is_author_bot(message: discord.Message):
    return message.author.bot


def is_author_human(message: discord.Message):
    return not message.author.bot


def does_message_contain_embed(message: discord.Message):
    return len(message.embeds) != 0
