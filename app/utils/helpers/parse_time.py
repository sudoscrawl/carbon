from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pendulum

from app.i18n.marker import _

if TYPE_CHECKING:
    from app.bot import Carbon
    from app.utils.core.embed import Embed


def parse_duration_to_timedelta(
    bot: Carbon, duration: str
) -> pendulum.Duration | Embed:
    """
    Parses a duration string into a pendulum.Duration object.

    Supported formats: 5h, 2h30m, 7days, 1d2h, 45m, etc.
    """
    units = {
        "w": "weeks",
        "week": "weeks",
        "weeks": "weeks",
        "d": "days",
        "day": "days",
        "days": "days",
        "h": "hours",
        "hr": "hours",
        "hrs": "hours",
        "hour": "hours",
        "hours": "hours",
        "m": "minutes",
        "min": "minutes",
        "mins": "minutes",
        "minute": "minutes",
        "minutes": "minutes",
        "s": "seconds",
        "sec": "seconds",
        "secs": "seconds",
        "second": "seconds",
        "seconds": "seconds",
    }

    clean_duration = duration.replace(" ", "").lower()

    if not re.fullmatch(r"(\d+[a-z]+)+", clean_duration):
        return bot.embed_factory.error_embed(_("Invalid duration format"))

    matches = re.findall(r"(\d+)([a-z]+)", clean_duration)

    duration_kwargs = {}
    for value, unit in matches:
        if unit not in units:
            return bot.embed_factory.error_embed(_("Invalid duration format"))

        target_unit = units[unit]
        duration_kwargs[target_unit] = duration_kwargs.get(target_unit, 0) + int(value)

    if not duration_kwargs:
        return bot.embed_factory.error_embed(_("Invalid duration format"))

    parsed_duration = pendulum.duration(**duration_kwargs)
    if parsed_duration.total_seconds() == 0:
        return bot.embed_factory.error_embed(_("Duration must be greater than 0"))
    return parsed_duration
