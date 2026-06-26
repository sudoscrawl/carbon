from app.utils.checks.purge_checks import contains_invite


def test_invite_regex():
    d1 = contains_invite("https://discord.gg/code")
    assert d1

    d2 = contains_invite("http://discord.gg/code")
    assert d2

    d3 = contains_invite("https://www.discord.gg/code")
    assert d3

    d4 = contains_invite("discord.gg/code")
    assert d4

    d5 = contains_invite("discord.com/invite/code")
    assert d5

    d6 = contains_invite("discordapp.com/invite/code")
    assert d6

    d7 = contains_invite("Here you go discord.gg/code")
    assert d7

    d8 = contains_invite("Hi lol")
    assert not d8
