# Telegram Assistant (starter)

A minimal Telegram bot in Python using polling mode. No public URL or webhook needed.

## 1. Create the bot
1. In Telegram, open a chat with **@BotFather** and send `/newbot`.
2. Follow the prompts and copy the token it gives you.

## 2. Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # then paste your token into .env
python bot.py
```
Message your bot on Telegram. Send `/start` to see your user ID, put it in
`ALLOWED_USER_IDS` in `.env`, and restart so only you can use it.

## 3. Deploy to the cloud
The project includes a `Dockerfile`, so any container host works. Set the
`TELEGRAM_BOT_TOKEN` (and `ALLOWED_USER_IDS`) as environment variables on the
host rather than uploading `.env`. Run **one instance only**: two instances
polling with the same token will conflict.

## Structure
- `bot.py`: Telegram messaging layer
- `assistant.py`: assistant logic (currently an echo; this is where tasks go)
