<div align="center">

# ⚡ Videl Music Bot

**Telegram Voice Chat Music Streamer**  
Fast • Smooth • Powerful • Free to Deploy

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Telegram](https://img.shields.io/badge/Support-Beasgohan-26A5E4?style=for-the-badge&logo=telegram)](https://t.me/BeasgohanSupport)

</div>

---

## ✨ Features

- 🎵 High quality VC music streaming
- 🔍 **Search result picker** — choose from top 5 YouTube results
- 🔁 Queue + Auto-Play + **Vote-to-skip**
- 📂 **User & group playlists** (`/saveplaylist`, `/playlist`)
- ⏸ Pause / Resume / Skip / Stop / Seek
- 📊 Live progress & interactive Now Playing (Queue / Save PL / Vote)
- 🎧 Effects & audio controls
- 🛡️ **Group management** — ban / mute / kick / warn / promote / demote / purge / pin
- 🔐 **Content locks panel** + **anti-flood**
- 👋 Welcome & goodbye messages with placeholders
- ⚠️ Configurable warn system with auto-ban
- 🧹 **Auto DB cleanup** (30 days inactive) + download cleanup + idle VC leave
- 🌐 Free deploy on Render, Koyeb, Railway, Heroku, VPS
- ⚡ Kurigram (Pyrogram) + Py-TgCalls

---

## 🚀 Run

```bash
git clone https://github.com/Beasgohan-code/Videl.git
cd Videl
pip install -r requirements.txt
cp sample.env .env
# fill API_ID, API_HASH, BOT_TOKEN, STRING_SESSION, MONGO_DB_URL, OWNER_ID
python main.py
```

Or: `python -m videl`

---

## ⚙️ Required Env

| Variable | Description |
|----------|-------------|
| `API_ID` / `API_HASH` | my.telegram.org |
| `BOT_TOKEN` | @BotFather |
| `STRING_SESSION` | Assistant account string session |
| `MONGO_DB_URL` | MongoDB URI |
| `OWNER_ID` | Your Telegram user ID |

See `sample.env` for optional vars.

---

## 👤 Credits

**Developer:** [Beasgohan-code](https://github.com/Beasgohan-code)  
**Support:** [Updates](https://t.me/BeasgohanUpdates) • [Chat](https://t.me/BeasgohanSupport)

Powered by Kurigram & PyTgCalls.  
Based on open-source Telegram music bot community work.

---

## License

MIT — see [LICENSE](LICENSE)  
Fork & improve freely. Keep credits ❤️
