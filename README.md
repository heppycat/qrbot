# Bale bot (base)

## Setup

```bash
cd /home/sleepy/bale_bot
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

```bash
export BALE_BOT_TOKEN="<your token here>"
python bot.py
```

## Notes

- Bale Bot API is Telegram-compatible. This app uses the Bale endpoints:
  - `https://tapi.bale.ai/bot<token>/METHOD`
  - `https://tapi.bale.ai/file/bot<token>/<file_path>`
- Long polling is used for simplicity.

## QR Command

```text
/qr some text here
```
