#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) Shrimadhav U K
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Telegram Bot"""

import json
import logging
import os
from typing import List, Dict
import aiohttp
from aiogram import (
    Bot,
    Dispatcher,
    types
)
from aiogram.utils.executor import (
    start_polling,
    start_webhook
)


# -*- CONSTANTS -*-
API_TOKEN = os.environ.get("API_TOKEN", None)
SHORTEN_LINK_API_KEY = os.environ.get(
    "SHORTEN_LINK_API_KEY",
    None
)
IS_WEBHOOK = bool(os.environ.get("IS_WEBHOOK", False))
START_TEXT = os.environ.get("START_TEXT", "send a link 😡😡")
CHECKING_TEXT = os.environ.get("CHECKING_TEXT", "🤔")
NO_LINKS_PROVIDED = os.environ.get(
    "NO_LINKS_PROVIDED",
    "input links cannot be detected"
)
SHORTEN_LINK_API_URL = os.environ.get(
    "SHORTEN_LINK_API_URL",
    "https://gplinks.in/api?api={api_token}&url={long_url}&format=text"
)
# webhook settings
WEBHOOK_HOST = os.environ.get("URL", None)
WEBHOOK_PATH = f"/{API_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
# webserver settings
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", "3001"))
ALLOW_MULTIPLE_LINKS = bool(os.environ.get("ALLOW_MULTIPLE_LINKS", False))
# -*- CONSTANTS -*-


# configure logging
logging.basicConfig(level=logging.INFO)
# initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def shorten_link(long_url: str) -> str:
    """
    shortens a long link
    """
    async with aiohttp.ClientSession() as session:
        request_url = SHORTEN_LINK_API_URL.format(
            api_token=SHORTEN_LINK_API_KEY,
            long_url=long_url
        )
        response_text = await (await session.get(
            request_url
        )).text()
        return response_text


async def get_short_zon_links(message: types.Message) -> List[Dict[str, str]]:
    """
    parses the Telegram message, and does bleck megick
    """
    input_entities = message.entities or message.caption_entities
    output_url_s = []
    for a_entity in input_entities:
        entity_type = a_entity.type
        if entity_type == "text_link":
            current_url = a_entity.url
            output_url_s.append({
                current_url: (await shorten_link(current_url))
            })
        elif entity_type == "url":
            current_url = message.text[
                a_entity.offset:
                a_entity.offset + a_entity.length
            ]
            output_url_s.append({
                current_url: (await shorten_link(current_url))
            })
    return output_url_s


@dp.message_handler(commands=["start", "help"])
async def help_handler_f(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(START_TEXT)


@dp.message_handler(regexp="^(ht|f)tp*")
async def links_handler_f(message: types.Message):
    """
    This handler will be called when user sends link(s)
    """
    status_message = await message.reply(CHECKING_TEXT)
    output_url_s = await get_short_zon_links(message)
    if len(output_url_s) > 0:
        if ALLOW_MULTIPLE_LINKS:
            await status_message.edit_text(
                json.dumps(
                    output_url_s,
                    sort_keys=True,
                    indent=4
                )
            )
        else:
            await status_message.edit_text(output_url_s[0][next(iter(output_url_s[0]))])
    else:
        await status_message.edit_text(NO_LINKS_PROVIDED)


async def on_startup(_):
    """
    This callback will be called, on bot startup
    """
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(_):
    """
    This callback will be called, on bot shutdown
    """
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()


if __name__ == "__main__":
    if IS_WEBHOOK:
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            # skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        start_polling(dp, skip_updates=True)
