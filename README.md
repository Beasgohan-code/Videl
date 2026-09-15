<div align="center">

# ⚡ Videl Music Bot

**Next-Generation Telegram Group Voice Chat Music & Video Streamer**  
*Powered by Pyrogram / Kurigram, PyTgCalls, MongoDB, and modern Telegram Bot API features.*

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram Bot API](https://img.shields.io/badge/Bot%20API-10.1%2B%20%7C%208.0%2B-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)
[![PyTgCalls](https://img.shields.io/badge/PyTgCalls-v2.3%2B-FF6B6B?style=for-the-badge)](https://github.com/pytgcalls/pytgcalls)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="https://files.catbox.moe/zvziwk.jpg" alt="Videl Music Banner" width="650" style="border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.5);">
</p>

[**Features**](#-features) • [**Bot API Innovations**](#-modern-bot-api-features) • [**Commands**](#-commands) • [**Deploy Guide**](#-deployment) • [**Configuration**](#-environment-variables)

</div>

---

## 🌟 Highlights

**Videl** is a modern, high-performance Telegram music bot designed for groups and channels. Built with an asynchronous core, it provides ultra-low latency voice chat playback, high-definition video streaming, dynamic glassmorphic album art generation, multi-assistant load balancing, and modern Telegram Bot API features like **`ButtonStyle`** (colored primary/danger action buttons), **`RichMessage`** structured block formatting, and **`copy_text`** instant clipboard actions.

---

## 🚀 Features

- 🎧 **HD Audio & 1080p Video Streaming**: Crystal-clear Opus audio and fluid 60FPS video playback in Telegram Voice/Video chats.
- ⚡ **Multi-Assistant Load Balancer**: Support for up to 5 assistant accounts (`SESSION1` to `SESSION5`) with automated round-robin routing and seamless failover.
- 🎨 **Dynamic Glassmorphic Thumbnail Engine**: Real-time PIL-generated album art cards with song metadata, waveforms, and time indicators.
- 🌐 **13+ Languages Localization**: Built-in multi-language translation engine (English, Hindi, Spanish, French, Russian, Arabic, German, Japanese, Portuguese, Turkish, Punjabi, Burmese, Chinese).
- 🔄 **Audio Controls & FX**: Volume control (`1-200%`), speed adjustment (`0.75x-2.0x`), real-time loop modes, playlist shuffling, seeking forward/backward, and song replay.
- 📜 **Instant Lyrics Integration**: Scrapes and renders clean expandable lyrics cards right in chat.
- 📱 **Universal Platform Support**:
  - **YouTube & YouTube Music** (Single tracks, search queries, playlists, shorts, live streams)
  - **Spotify** (Tracks, albums, public playlists)
  - **Apple Music** & **SoundCloud**
  - **Direct URLs** (MP3, M3U8, MP4, AAC, FLAC streams)
  - **Telegram Files** (Native audio, voice notes, video files, and video notes with live download progress)
- 🔒 **Comprehensive Group & Admin Controls**:
  - Play Mode toggle (Admins-only vs Everyone)
  - Clean Mode / Command auto-deletion
  - Authorized Users system (`/auth`, `/unauth`, `/authlist`)
  - Smart Assistant auto-invite and join-request approvals
  - Auto-leave on empty voice chats (`AUTO_LEAVE`, `AUTO_END`)
  - Global broadcast engine (`/broadcast`) with pin, copy, and forward modes

---

## 💎 Modern Bot API Features

### 1. `ButtonStyle` Support
Videl leverages Telegram Bot API 8.0+ / 10.x button styling:
- **`primary`** (Accent highlighted buttons: *Play*, *Resume*, *Volume*, *Quick Actions*)
- **`danger`** (Red alert buttons: *Stop*, *Cancel Download*, *Close*, *Delete*)
- **`success`** (Green confirmation buttons: *Enabled Status*, *Selected Language*)
- **`default`** (Neutral navigation & info buttons)

### 2. `RichMessage` & Structured Blocks
- **Blockquote cards**: `<blockquote expandable>` for long playlists and lyrics.
- **Rich Markdown Formatting**: Pull quotes, headers, code blocks, and dynamic streaming drafts.
- **Rich Draft Streaming**: Real-time progress bar ticker updates without rate-limit jitter.

### 3. `copy_text` 1-Tap Copy Buttons
- Quick-copy YouTube URLs, track IDs, and join links straight into the user's clipboard with one tap.

---

## 📋 Commands

### 🎵 Music & Playback Commands
| Command | Description |
| :--- | :--- |
| `/play [query / URL / reply]` | Streams audio in voice chat from YouTube, Spotify, or Telegram |
| `/vplay [query / URL / reply]` | Streams video with HD video feed |
| `/playforce` or `/vplayforce` | Force plays track immediately, placing it at the front of queue |
| `/pause` | Pauses ongoing voice chat stream |
| `/resume` | Resumes paused voice chat stream |
| `/skip` or `/next` | Skips to the next queued track |
| `/stop` or `/end` | Stops stream and clears playback queue |
| `/replay` | Replays the currently playing track from the start |
| `/seek [seconds]` | Seeks forward by specified seconds (e.g. `/seek 30`) |
| `/seekback [seconds]` | Seeks backward by specified seconds (e.g. `/seekback 15`) |
| `/loop [1-10 / off]` | Loops currently streaming track |
| `/volume [1-200]` | Adjusts assistant voice chat playback volume |
| `/speed [0.75-2.0]` | Adjusts stream playback speed |
| `/shuffle` | Randomly shuffles the upcoming playlist queue |
| `/queue` or `/playing` | Displays currently playing track and playlist queue |
| `/lyrics [song name]` | Fetches song lyrics |

### 👑 Group Management & Settings
| Command | Description |
| :--- | :--- |
| `/settings` or `/playmode` | Interactive button settings panel (Playmode, Cleanmode, Language) |
| `/lang` or `/language` | Opens 13-language selector |
| `/auth [reply / user_id]` | Authorizes a non-admin user to control playback |
| `/unauth [reply / user_id]` | Removes a user from authorized list |
| `/authlist` | Shows list of authorized users in current chat |
| `/reload` or `/admincache` | Refreshes administrator cache for the group |

### ⚡ Sudo & Developer Commands
| Command | Description |
| :--- | :--- |
| `/ping` or `/alive` | Checks bot latency, PyTgCalls ping, uptime, and system RAM/CPU |
| `/stats` | Shows served chats, total users, assistants, and system diagnostics |
| `/activevc` or `/ac` | Shows count and list of active voice chat streams |
| `/broadcast [reply]` | Broadcasts message globally (`-user`, `-nochat`, `-copy`) |
| `/blacklist [chat_id / id]`| Blacklists group or user from using the bot |
| `/unblacklist [chat_id]` | Removes target from blacklist |
| `/addsudo` / `/rmsudo` | Adds or removes sudo users |
| `/logs` | Exports bot's runtime `log.txt` |
| `/eval` or `/exec` | Executes async Python code snippet |
| `/sh` or `/bash` | Runs shell commands on host machine |
| `/restart` | Cleans cache/temp downloads and restarts bot process |

---

## 🛠 Deployment

### Option 1: One-Click Heroku Deploy

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

1. Fork or clone this repository.
2. Click the **Deploy to Heroku** button above.
3. Fill in required environment variables (`API_ID`, `API_HASH`, `BOT_TOKEN`, `MONGO_URL`, `LOGGER_ID`, `OWNER_ID`, `SESSION`).
4. Scale the `worker` dyno inside the Heroku Dashboard.

---

### Option 2: Docker / Docker-Compose

```bash
# Clone the repository
git clone https://github.com/Beasgohan-code/Videl.git
cd Videl

# Create and populate .env
cp sample.env .env
nano .env

# Build and run container
docker build -t videl-music .
docker run -d --name videl --env-file .env videl-music
```

---

### Option 3: VPS / Ubuntu & Debian

```bash
# 1. Clone repository
git clone https://github.com/Beasgohan-code/Videl.git
cd Videl

# 2. Run automated setup wizard (Installs Python, FFmpeg, Deno, requirements & configures .env)
sudo bash setup

# 3. Start the bot
bash start
```

---

## ⚙️ Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `API_ID` | **Yes** | Telegram App API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | **Yes** | Telegram App API Hash from [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | **Yes** | Telegram Bot Token from [@BotFather](https://t.me/BotFather) |
| `MONGO_URL` | **Yes** | MongoDB Connection URI from [MongoDB Atlas](https://cloud.mongodb.com) |
| `LOGGER_ID` | **Yes** | Telegram Log Group / Channel ID (e.g. `-1001234567890`) |
| `OWNER_ID` | **Yes** | Numeric User ID of the Bot Owner |
| `SESSION` | **Yes** | Pyrogram / Kurigram String Session (from [@StringFatherBot](https://t.me/StringFatherBot)) |
| `SESSION2` - `SESSION5` | No | Additional assistant string sessions for multi-assistant scaling |
| `BOT_NAME` | No | Display name of the bot (Default: `Videl Music`) |
| `SUPPORT_CHAT` | No | Link to your Telegram support group |
| `SUPPORT_CHANNEL` | No | Link to your Telegram updates channel |
| `DURATION_LIMIT` | No | Max track duration in minutes (Default: `60`) |
| `QUEUE_LIMIT` | No | Max songs in queue per chat (Default: `30`) |
| `PLAYLIST_LIMIT` | No | Max playlist tracks to import at once (Default: `25`) |
| `AUTO_LEAVE` | No | Auto leave inactive chats after 1 hour (Default: `False`) |
| `AUTO_END` | No | Auto end stream when voice chat becomes empty (Default: `False`) |
| `THUMB_GEN` | No | Generate dynamic PIL album art thumbnails (Default: `True`) |
| `COOKIES_URL` | No | Direct Batbin/Pastebin URLs for YouTube cookie files |

---

## 📁 Project Architecture

```
Videl/
├── videl/
│   ├── __init__.py           # Bot instance initialization & loggers
│   ├── __main__.py           # Execution entrypoint & lifecycle
│   ├── core/
│   │   ├── bot.py            # Custom Telegram Bot Client
│   │   ├── calls.py          # PyTgCalls Voice & Video Stream Engine
│   │   ├── dir.py            # Runtime directory manager
│   │   ├── lang.py           # Multi-language localization engine
│   │   ├── mongo.py          # High-speed cached MongoDB database
│   │   ├── telegram.py       # Telegram native media downloader
│   │   ├── userbot.py        # Multi-Assistant userbot manager (1-5)
│   │   └── youtube.py        # Multi-platform audio/video resolver
│   ├── helpers/
│   │   ├── _admins.py        # VC permissions & admin validators
│   │   ├── _api.py           # Fallback stream API client
│   │   ├── _dataclass.py     # Track & Media dataclasses
│   │   ├── _exec.py          # Asynchronous eval runner
│   │   ├── _inline.py        # Modern Inline Keyboards
│   │   ├── _play.py          # Assistant auto-join & play middleware
│   │   ├── _queue.py         # Advanced playlist queue manager
│   │   ├── _thumbnails.py    # PIL Dynamic Glassmorphism Thumbnails
│   │   ├── _utilities.py     # Formatters, logs & lyrics scrapers
│   │   ├── button_style.py   # Bot API ButtonStyle (Primary, Danger, Success)
│   │   ├── rich_message.py   # Bot API 10.1+ RichMessage & Block builder
│   │   ├── Inter-Light.ttf   # UI Font
│   │   └── Raleway-Bold.ttf  # Header Font
│   ├── locales/              # 13 JSON Localization files
│   └── plugins/              # 27 Modular commands & feature plugins
├── config.py                 # Central configuration parser
├── sample.env                # Environment variables template
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container definition
├── heroku.yml                # Heroku container configuration
├── app.json                  # One-click Heroku template
├── setup                     # Automated Linux installer
├── start                     # Startup runner script
└── LICENSE                   # MIT License
```

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

<div align="center">
  <b>Made with ❤️ by <a href="https://github.com/Beasgohan-code">Beasgohan-code</a></b>
</div>
