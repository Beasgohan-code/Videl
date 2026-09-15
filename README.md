<div align="center">

# ⚡ Videl Music & Management Bot

**Next-Generation Telegram Voice Chat Music Streamer & Group Management Suite**  
*Engineered with Pyrogram / Kurigram, PyTgCalls, MongoDB, and modern Telegram Bot API features.*

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram Bot API](https://img.shields.io/badge/Bot%20API-10.1%2B%20%7C%208.0%2B-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)
[![PyTgCalls](https://img.shields.io/badge/PyTgCalls-v2.3%2B-FF6B6B?style=for-the-badge)](https://github.com/pytgcalls/pytgcalls)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="https://files.catbox.moe/zvziwk.jpg" alt="Videl Music Banner" width="650" style="border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.5);">
</p>

[**Player UI Showcase**](#-sleek-player-ui) • [**Features**](#-features) • [**Bot API Innovations**](#-modern-bot-api-features) • [**Commands**](#-commands) • [**Deploy Guide**](#-deployment) • [**Configuration**](#-environment-variables)

</div>

---

## 📸 Sleek Player UI

```
Britney Spears - Criminal (Lyrics)
7clouds
AUDIO • 3:44
Requested by Rahul 🤍

2:32 ─────🔘──────── 3:44

[ ↶ Replay ]   [ II Pause ]   [ » Skip ]
        [ ≡ Queue • 3 ]
[ 🔊 Volume ]  [ 🔀 Shuffle ]  [ 📜 Lyrics ]  [ ⚡ Speed ]
     [ ❐ Copy Link ]   [ 🗑 Close ]
```

---

## 🌟 Highlights & Capabilities

- 🎧 **HD Audio & 1080p Video Streaming**: Crystal-clear Opus audio and fluid 60FPS video playback in Telegram Voice/Video chats with dynamic progress bars.
- ⚡ **Multi-Assistant Load Balancer**: Multi-assistant clustering (`SESSION1` to `SESSION5`) with automated round-robin routing and seamless failover.
- 📥 **High-Speed Video & Song Downloader**: Download 320kbps MP3s and 1080p/720p MP4 videos directly to Telegram chats via `/song`, `/video`, and `/download`.
- 🛡 **Full Group Moderation Suite**: Fast admin commands (`/ban`, `/tban`, `/unban`, `/mute`, `/tmute`, `/unmute`, `/kick`, `/pin`, `/purge`, `/del`, `/staff`, `/id`, `/info`).
- 🎨 **Dynamic Glassmorphic Thumbnail Engine**: Real-time PIL-generated album art cards with song metadata, waveforms, and time indicators.
- 🌐 **13+ Languages Localization**: Built-in multi-language translation engine (English, Hindi, Spanish, French, Russian, Arabic, German, Japanese, Portuguese, Turkish, Punjabi, Burmese, Chinese).
- 🔄 **Audio Controls & FX**: Volume control (`1-200%`), speed adjustment (`0.75x-2.0x`), real-time loop modes, playlist shuffling, seeking forward/backward, and song replay.
- 📜 **Instant Lyrics Scraper**: Real-time expandable lyrics cards in chat.
- 📱 **Universal Platform Support**:
  - **YouTube & YouTube Music** (Single tracks, search queries, playlists, shorts, live streams)
  - **Spotify** (Tracks, albums, public playlists)
  - **Apple Music** & **SoundCloud**
  - **Direct URLs** (MP3, M3U8, MP4, AAC, FLAC streams)
  - **Telegram Files** (Native audio, voice notes, video files with live download progress)
- 🚀 **Diagnostics & Maintenance**: Network speedtest (`/speedtest`), assistant cleanup (`/leaveall`), interactive search (`/search`), global broadcast (`/broadcast`), and developer eval (`/eval`, `/sh`).

---

## 💎 Modern Bot API Features

### 1. `ButtonStyle` Support
- **`primary`** (Accent highlighted buttons: *Play*, *Resume*, *Queue Counter*, *Copy Link*)
- **`danger`** (Red alert buttons: *Stop*, *Cancel Download*, *Close*, *Delete*)
- **`success`** (Green confirmation buttons: *Enabled Status*, *Selected Language*)
- **`disabled`** (Disabled/non-clickable buttons for status and placeholders)
- **`default`** (Neutral navigation & controls)

### 2. `RichMessage` & Structured Blocks
- **Blockquote cards**: `<blockquote expandable>` for long playlists, staff lists, and lyrics.
- **Rich Markdown Formatting**: Pull quotes, headers, code blocks, and dynamic streaming drafts.
- **Rich Draft Streaming**: Real-time progress bar ticker updates without rate-limit jitter.

### 3. `copy_text` 1-Tap Copy Buttons
- Quick-copy YouTube URLs, track IDs, user IDs, and chat IDs straight into the clipboard with one tap.

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
| `/search [query]` | Interactive YouTube search with 1-tap play/download buttons |

### 📥 Video & Audio Downloader
| Command | Description |
| :--- | :--- |
| `/song [name / URL]` | Downloads high quality 320kbps MP3 audio file to chat |
| `/video [name / URL]` | Downloads HD 720p/1080p MP4 video file to chat |
| `/download [name / URL]`| Fast multi-format media downloader |

### 🛡 Group Management & Moderation
| Command | Description |
| :--- | :--- |
| `/ban [reply / id] [time/reason]` | Bans user from group (supports temp bans e.g. `10m`, `1d`) |
| `/tban [reply / id] [time]` | Temporarily bans a user |
| `/unban [reply / id]` | Unbans a user |
| `/mute [reply / id] [time]` | Mutes a user (supports temp mutes) |
| `/unmute [reply / id]` | Unmutes a user |
| `/kick [reply / id]` | Kicks a user from the group |
| `/pin` / `/unpin` / `/unpinall` | Pins or unpins messages |
| `/purge` / `/del` | Fast message deleter & purger |
| `/staff` or `/adminlist` | Displays group staff & admin roster |
| `/id` or `/info` | Displays user and chat ID card with 1-tap copy buttons |
| `/settings` or `/playmode` | Interactive button settings panel (Playmode, Cleanmode, Language) |
| `/lang` or `/language` | Opens 13-language selector |
| `/auth [reply / id]` | Authorizes a non-admin user to control playback |
| `/unauth [reply / id]` | Removes a user from authorized list |
| `/authlist` | Shows list of authorized users in current chat |
| `/reload` or `/admincache` | Refreshes administrator cache for the group |

### ⚡ Sudo & Developer Commands
| Command | Description |
| :--- | :--- |
| `/ping` or `/alive` | Checks bot latency, PyTgCalls ping, uptime, and system RAM/CPU |
| `/speedtest` or `/spt` | Runs network speedtest (download, upload, latency, ISP) |
| `/stats` | Shows served chats, total users, assistants, and system diagnostics |
| `/activevc` or `/ac` | Shows count and list of active voice chat streams |
| `/leaveall` | Instructs assistants to leave all non-active chats |
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
│   │   ├── _inline.py        # Modern Inline Keyboards with ButtonStyle
│   │   ├── _play.py          # Assistant auto-join & play middleware
│   │   ├── _queue.py         # Advanced playlist queue manager
│   │   ├── _thumbnails.py    # PIL Dynamic Glassmorphism Thumbnails
│   │   ├── _utilities.py     # Formatters, logs & lyrics scrapers
│   │   ├── button_style.py   # Bot API ButtonStyle (Primary, Danger, Success, Disabled)
│   │   ├── rich_message.py   # Bot API 10.1+ RichMessage & Block builder
│   │   ├── Inter-Light.ttf   # UI Font
│   │   └── Raleway-Bold.ttf  # Header Font
│   ├── locales/              # 13 JSON Localization files
│   └── plugins/              # 32 Modular commands & feature plugins
│       ├── active.py         # Active voice chat tracker
│       ├── admin.py          # Group moderation (ban, mute, kick, purge, pin, staff)
│       ├── auth.py           # Auth users manager
│       ├── blacklist.py      # Blacklist / Whitelist manager
│       ├── broadcast.py      # Global broadcast manager
│       ├── callbacks.py      # Callback query router
│       ├── downloader.py     # YouTube Video & MP3 Song Downloader
│       ├── eval.py           # Python / Bash eval runner
│       ├── iquery.py         # Telegram inline query search
│       ├── language.py       # Multi-language switcher
│       ├── leaveall.py       # Assistant leave inactive groups
│       ├── loop.py           # Loop stream controller
│       ├── lyrics.py         # Song lyrics scraper
│       ├── misc.py           # Background timers & VC auto-leave
│       ├── pause.py          # Pause stream
│       ├── ping.py           # Health check & latency
│       ├── play.py           # Audio & Video streamer
│       ├── queue.py          # Playlist queue viewer
│       ├── replay.py         # Replay current song
│       ├── restart.py        # Clean restart & logs
│       ├── resume.py         # Resume stream
│       ├── search.py         # Interactive YouTube search
│       ├── seek.py           # Forward / Backward seek
│       ├── shuffle.py        # Queue shuffle
│       ├── skip.py           # Skip to next song
│       ├── speed.py          # Playback speed controller
│       ├── speedtest.py      # Network speed diagnostics
│       ├── start.py          # Start & help menu
│       ├── stats.py          # System performance stats
│       ├── stop.py           # Stop playback
│       ├── sudoers.py        # Sudo users management
│       └── volume.py         # Audio volume controller
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
