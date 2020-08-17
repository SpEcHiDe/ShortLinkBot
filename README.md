# GPLinksBot

~~(yet)~~ another link shortner inside Telegram.

- can be found on [Telegram](https://telegram.dog/gplinksbot)

## installing

#### The Easy Way

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)


#### The Legacy Way

- clone the repository, locally.
```sh
git clone https://GitLab.com/SpEcHiDe/ShortLinkBot.git -b aiogram
```

- change the directory.
```sh
cd ShortLinkBot
```

- create a virtual environment.
```sh
python3 -m venv venv
```

- activate the virtual environment.
```sh
. ./venv/bin/activate
```

- install the requirements.
```sh
pip install -r requirements.txt
```

- set the required ENVironment variables

- run the bot
```sh
python3 bot.py
```

## [@SpEcHlDe](https://telegram.dog/SpEcHlDe)

- Mandatory Environment Variables
  - `API_TOKEN`: get Telegram Bot Token from [@BotFather](https://telegram.dog/BotFather)
  - `SHORTEN_LINK_API_KEY`: get API key from your short link provider. The default provider is [GPLinks](https://gplinks.in/ref/avsojwoq)

- Optional Environment Variables
  - `SHORTEN_LINK_API_URL`: Get your shortened API URL in the same format as in Line Number 51 of bot.py. If you want to use GPLinks, leave this empty, and unset the variable.
  - `START_TEXT`: 
  - `CHECKING_TEXT`: 
  - `NO_LINKS_PROVIDED`:
  - `IS_WEBHOOK`: setting this to `ANYTHING` will enable WEBHOOK mode, else will use long-polling mode.
  - `URL`: The webhook URL that the bot should use.
  - `PORT`: The port to listen at.

- The Telegram RoBot should work without setting the optional variables.
- Please report any issues to the support group: [@SpEcHlDe](https://telegram.dog/SpEcHlDe)


## LICENSE
[AGPLv3](./LICENSE)

## credits

- Libraries Used:
  - [aiogram](https://docs.aiogram.dev)
  - [aiohttp](https://docs.aiohttp.org)
