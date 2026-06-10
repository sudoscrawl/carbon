import discord


def is_author_bot(message: discord.Message):
    return message.author.bot
