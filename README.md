<div align="center">

# ⚡ Videl Music & Ultra Management Bot

**Next-Generation Telegram Voice Chat Music Streamer & Complete Group Administration Suite**  
*Engineered with Dual-Engine Architecture (Pyrogram/Kurigram MTProto + Aiogram 3.x Bot API 8.x/10.x), PyTgCalls, MongoDB, Real-time DSP Equalizers, In-Bot Session Generator, and Auto-Healing Infrastructure.*

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram Bot API](https://img.shields.io/badge/Bot%20API-10.2%2B%20%7C%208.0%2B-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)
[![PyTgCalls](https://img.shields.io/badge/PyTgCalls-v2.3%2B-FF6B6B?style=for-the-badge)](https://github.com/pytgcalls/pytgcalls)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="https://files.catbox.moe/zvziwk.jpg" alt="Videl Music Banner" width="650" style="border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.5);">
</p>

[**Player UI Showcase**](#-sleek-player-ui) • [**Features**](#-highlights--capabilities) • [**Bot API 8.x/10.x Innovations**](#-modern-bot-api-innovations) • [**Commands**](#-commands) • [**Deploy Guide**](#-deployment) • [**Configuration**](#-environment-variables)

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
- 🎛 **Real-Time DSP Equalizer & Effects**: Real-time audio filters (`/bassboost`, `/superbass`, `/nightcore`, `/slowed`, `/8d`, `/vaporwave`, `/karaoke`, `/surround`, `/eq`).
- 🤖 **Smart AutoPlay / AI DJ**: Automated smart endless music recommendation fallback that keeps music playing smoothly when your queue finishes (`/autodj`).
- 🔐 **In-Bot String Session Generator (Admin Only)**: Generate Pyrogram string sessions interactively within PM with OTP, 2FA support, and `/cancel` safeguard (`/generate_session`, `/genstring`).
- 🚨 **Global Ban (GBan) System**: Cross-chat enforcement banning spammers and malicious users across all served groups with automated join-prevention (`/gban`, `/ungban`, `/gbanlist`).
- ⭐️ **Telegram Stars Invoices & Tipping**: Native Telegram Stars donations (`/stars`, `/tip`, `/donate`) powered by Bot API 8.x/10.x Star currency (`XTR`).
- ✨ **Animated Visual Message Effects**: Fire, Celebration, Heart, Lightning, and Confetti message effects (`/effect`, `/react`).
- 📱 **Telegram Mini App & WebApp**: Interactive Mini App music controller and web dashboard (`/webapp`, `/miniapp`).
- 📢 **Linked Channel Streaming**: Play music in linked broadcast channels seamlessly (`/cplay`, `/cvplay`, `/cpause`, `/cresume`, `/cstop`, `/cqueue`, `/channel`).
- 🔄 **Assistant Live Auto-Bio Sync**: Dynamically updates assistant Telegram profile bios with real-time streaming metadata (`/autobio`).
- 👤 **Assistant Profile Manager**: Update assistant profile photo, display names, and bio directly via Telegram (`/setpfp`, `/delpfp`, `/setname`, `/setbio`, `/assjoin`, `/assleave`).
- 🧹 **Automated Cache Garbage Collector**: Auto-cleans stale temporary `.mp3` and `.mp4` downloads every 30 minutes to keep disk usage near zero (`/clearcache`, `/cleanup`).
- 🛰 **Voice Chat State Watcher**: Intercepts `video_chat_started`, `video_chat_ended`, and member leave events to prevent desyncs and clean up queues.
- 📻 **24/7 Curated Live Radio**: Stream Lofi 24/7, Synthwave, Chillhop, Anime OST, EDM, Rock, Pop, and Jazz stations with `/radio`.
- 🔍 **Shazam Audio Identification**: Reply to any voice note or video with `/shazam` to identify track name, artist, album, and get 1-tap stream/download buttons.
- 🎙 **Voice Chat Recording**: Record ongoing voice chats to high-bitrate MP3 files with `/record` and `/stoprecord`.
- 💾 **Personal Playlists**: Create, manage, and batch-queue personal playlists (`/playlist`, `/addplaylist`, `/delplaylist`, `/playplaylist`).
- ⚡ **Multi-Assistant Load Balancer**: Multi-assistant clustering (`SESSION1` to `SESSION5`) with automated round-robin routing and seamless failover.
- 📥 **High-Speed Video & Song Downloader**: Download 320kbps MP3s and 1080p/720p MP4 videos directly to Telegram chats via `/song`, `/video`, and `/download`.
- 🛡 **Full Group Moderation Suite**: Fast admin commands (`/ban`, `/tban`, `/unban`, `/mute`, `/tmute`, `/unmute`, `/kick`, `/pin`, `/purge`, `/del`, `/staff`, `/id`, `/info`).
- 🔒 **Chat Permissions & Locks**: Lock stickers, media, links, voice, forwards, bots, and polls (`/lock`, `/unlock`, `/locks`).
- 🛡 **Anti-Flood & Spam Protection**: Auto-mutes users sending messages too quickly (`/antiflood`, `/setflood`).
- 📝 **Custom Filters & Notes**: Auto-responder keyword filters (`/filter`, `/filters`) and saved notes (`/save`, `/get`, `/notes`).
- 👋 **Custom Welcome & Clean Service**: Customizable welcome cards (`/setwelcome`) and auto-cleaning join/leave service messages (`/cleanservice`).
- 🗣 **Text-to-Speech (TTS)**: Synthesize high quality speech in 50+ languages with `/tts` and `/voice`.
- 🎮 **Music Trivia Quiz Game**: Interactive voice chat guess-the-song quiz with countdowns and score tracking via `/songquiz`.
- 😴 **AFK System**: Global AFK status notifier with elapsed time tracking (`/afk`).
- 📢 **Tag All / Mentions**: Batch-mention group members with customized prompts (`/tagall`, `/cancel_tagall`).
- 🏥 **Built-in HTTP Healthcheck Server**: Lightweight async web server on port 8080 (or `PORT`) for Docker, Render, Koyeb, Railway, and UptimeRobot uptime monitoring.
- 🎨 **Dynamic Glassmorphic Thumbnail Engine**: Real-time PIL-generated album art cards with song metadata, waveforms, and time indicators.
- 🌐 **13+ Languages Localization**: Built-in multi-language translation engine (English, Hindi, Spanish, French, Russian, Arabic, German, Japanese, Portuguese, Turkish, Punjabi, Burmese, Chinese).
- 🚀 **Diagnostics & Maintenance**: Network speedtest (`/speedtest`), system host diagnostics (`/sysinfo`), served chats/users exporter (`/servedchats`, `/servedusers`), config viewer with masked credentials (`/config`, `/vars`), assistant cleanup (`/leaveall`), assistant status (`/assistants`), database backup (`/dbbackup`), maintenance toggle (`/maintenance`), global broadcast (`/broadcast`), hot-reload (`/hotreload`), and developer eval (`/eval`, `/sh`).

---

## 💎 Modern Bot API Innovations

### 1. Dual-Engine Architecture
Videl utilizes a hybrid dual-engine bridge (`TelegramBridge`):
- **Kurigram / Pyrogram MTProto**: Powers low-latency voice chat streaming, high-speed file transfers, and userbot multi-assistant clusters.
- **Aiogram 3.31+ Bot API Engine**: Dispatches modern Bot API 8.x / 10.x endpoints including `message_effect_id`, `send_invoice` (Stars `XTR`), `set_message_reaction`, and HTML5 Mini App handshakes.

### 2. `ButtonStyle` Support
- **`primary`** (Accent highlighted buttons: *Play*, *Resume*, *Queue Counter*, *Copy Link*)
- **`danger`** (Red alert buttons: *Stop*, *Cancel Download*, *Close*, *Delete*)
- **`success`** (Green confirmation buttons: *Enabled Status*, *Selected Language*)
- **`disabled`** (Disabled/non-clickable buttons for status and placeholders)
- **`default`** (Neutral navigation & controls)

### 3. `RichMessage` & Structured Blocks
- **Blockquote cards**: `<blockquote expandable>` for long playlists, staff lists, and lyrics.
- **Rich Markdown Formatting**: Pull quotes, headers, code blocks, and dynamic streaming drafts.

### 4. `copy_text` 1-Tap Copy Buttons
- Quick-copy YouTube URLs, track IDs, user IDs, and chat IDs straight into clipboard with one tap.

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
| `/autodj [on/off]` | Toggles AI DJ / Smart AutoPlay endless radio fallback |

### 📢 Channel Streaming & WebApp
| Command | Description |
| :--- | :--- |
| `/channel [@username/id]` | Links a channel to the current group |
| `/cplay [query / URL]` | Streams music in the linked channel's voice chat |
| `/cvplay [query / URL]` | Streams video in the linked channel's video chat |
| `/cpause` / `/cresume` | Pauses or resumes linked channel playback |
| `/cstop` | Stops stream in linked channel |
| `/cqueue` | Displays linked channel queue |
| `/webapp` or `/miniapp` | Launches interactive Telegram Mini App player |
| `/stars [amount]` or `/tip` | Sends Telegram Stars donation invoice (`XTR`) |
| `/effect [fire/heart/..] [text]` | Sends message with animated Bot API visual effect |
| `/react [emoji]` | Reacts to message with modern emoji reaction |
| `/autobio [on/off]` | Toggles assistant real-time profile bio sync |

### 🎛 Audio Equalizer, Radio & Special Media
| Command | Description |
| :--- | :--- |
| `/eq` or `/effects` | Interactive DSP Audio Equalizer menu |
| `/bassboost` / `/superbass` | Applies heavy bass boost effect |
| `/nightcore` | Applies Nightcore pitch/tempo effect |
| `/slowed` | Applies Slowed + Reverb effect |
| `/8d` | Applies 8D surround audio panning |
| `/vaporwave` | Applies Vaporwave retro effect |
| `/karaoke` | Removes vocals (center-channel cancellation) |
| `/surround` | Applies 3D spatial surround sound |
| `/radio` or `/live` | 24/7 curated live streaming stations (Lofi, Synthwave, EDM, Rock, Pop) |
| `/shazam` or `/whatsong` | Recognizes song by replying to any audio/video |
| `/record` / `/stoprecord` | Records voice chat audio and exports MP3 |
| `/playlist` / `/myplaylist` | Views personal saved tracks |
| `/addplaylist [query / link]` | Adds song to personal playlist |
| `/delplaylist [ID]` | Deletes song from personal playlist |
| `/playplaylist` | Streams your entire personal playlist in voice chat |

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
| `/lock [type]` / `/unlock` | Locks/unlocks stickers, media, links, voice, forwards, bots |
| `/locks` | Displays active chat locks |
| `/antiflood [limit/off]` | Sets anti-flood spam limit |
| `/filter [keyword] [reply]` | Adds auto-reply keyword filter |
| `/stopfilter [keyword]` | Removes keyword filter |
| `/filters` | Lists active filters |
| `/save [name] [text]` | Saves group note (accessible via `/get [name]` or `#[name]`) |
| `/notes` / `/clear [name]` | Lists or deletes notes |
| `/setwelcome [text]` | Sets custom welcome message with placeholders |
| `/delwelcome` | Resets welcome message |
| `/cleanservice [on/off]` | Auto-deletes join/leave/pinned service events |
| `/pin` / `/unpin` / `/unpinall` | Pins or unpins messages |
| `/purge` / `/del` | Fast message deleter & purger |
| `/staff` or `/adminlist` | Displays group staff & admin roster |
| `/id` or `/info` | Displays user and chat ID card with 1-tap copy buttons |
| `/tagall [prompt]` | Mentions all group members |
| `/cancel_tagall` | Stops ongoing mention spree |
| `/tts [text]` | Converts text to voice note |
| `/songquiz` | Starts voice chat song trivia game |
| `/afk [reason]` | Sets user to AFK status |
| `/settings` or `/playmode` | Interactive button settings panel (Playmode, Cleanmode, Language) |
| `/lang` or `/language` | Opens 13-language selector |
| `/auth [reply / id]` | Authorizes a non-admin user to control playback |
| `/unauth [reply / id]` | Removes a user from authorized list |
| `/authlist` | Shows list of authorized users in current chat |
| `/reload` or `/admincache` | Refreshes administrator cache for the group |

### ⚡ Sudo, Admin & Infrastructure Commands
| Command | Description |
| :--- | :--- |
| `/generate_session` or `/genstring` | Interactive in-bot string session generator (Admin PM only) |
| `/gban [reply/id] [reason]` | Globally bans a user across all served chats |
| `/ungban [reply/id]` | Removes global ban from a user |
| `/gbanlist` | Lists all globally banned user IDs |
| `/sysinfo` or `/hostinfo` | Detailed CPU, RAM, Swap, Disk, and OS diagnostics |
| `/servedchats` | Exports `.txt` file of all served group chats |
| `/servedusers` | Exports `.txt` file of all served users |
| `/botleave [chat_id]` | Forces bot to leave a specified chat |
| `/announce [text]` | Broadcasts a pinned announcement across all active voice chats |
| `/logger [on/off]` | Toggles real-time error logging to LOGGER_ID |
| `/hotreload` or `/reloadplugins` | Hot-reloads all plugins dynamically without restarting bot |
| `/ping` or `/alive` | Checks bot latency, PyTgCalls ping, uptime, and system RAM/CPU |
| `/speedtest` or `/spt` | Runs network speedtest (download, upload, latency, ISP) |
| `/stats` | Shows served chats, total users, assistants, and system diagnostics |
| `/activevc` or `/ac` | Shows count and list of active voice chat streams |
| `/assistants` | Live health and ping status of all 5 assistants |
| `/setpfp` / `/delpfp` | Changes or deletes assistant's profile picture |
| `/setname` / `/setbio` | Updates assistant display name or bio |
| `/assjoin` / `/assleave` | Forces assistant to join or leave a specific chat |
| `/leaveall` | Instructs assistants to leave all non-active chats |
| `/clearcache` / `/cleanup` | Purges all temporary download files and caches |
| `/config` or `/vars` | Securely inspects environment variables in PM |
| `/maintenance [on/off]` | Toggles maintenance mode |
| `/dbbackup` | Dumps MongoDB database backup to JSON |
| `/broadcast [reply]` | Broadcasts message globally (`-user`, `-nochat`, `-copy`) |
| `/blacklist [chat_id / id]`| Blacklists group or user from using the bot |
| `/unblacklist [chat_id]` | Removes target from blacklist |
| `/addsudo` / `/rmsudo` | Adds or removes sudo users |
| `/sudolist` | Lists all authorized sudoers |
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
docker run -d --name videl -p 8080:8080 --env-file .env videl-music
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
| `SESSION` | **Yes** | Pyrogram / Kurigram String Session (from [@StringFatherBot](https://t.me/StringFatherBot) or in-bot `/genstring`) |
| `SESSION2` - `SESSION5` | No | Additional assistant string sessions for multi-assistant scaling |
| `BOT_NAME` | No | Display name of the bot (Default: `Videl Music`) |
| `PORT` | No | Port for HTTP healthcheck server (Default: `8080`) |
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
│   │   ├── bridge.py         # Dual-Engine Telegram Bridge (MTProto + Bot API 10.x)
│   │   ├── calls.py          # PyTgCalls Voice & Video Stream Engine with AutoPlay
│   │   ├── dir.py            # Runtime directory manager
│   │   ├── lang.py           # Multi-language localization engine (13+ languages)
│   │   ├── mongo.py          # High-speed cached MongoDB database with GBan
│   │   ├── server.py         # Async HTTP Healthcheck server (Port 8080/PORT)
│   │   ├── telegram.py       # Telegram native media downloader
│   │   ├── userbot.py        # Multi-Assistant userbot manager (1-5)
│   │   └── youtube.py        # Multi-platform audio/video resolver
│   ├── helpers/
│   │   ├── _admins.py        # VC permissions & admin validators
│   │   ├── _api.py           # Fallback stream API client
│   │   ├── _dataclass.py     # Track & Media dataclasses
│   │   ├── _exec.py          # Asynchronous eval runner
│   │   ├── _filters_dsp.py   # FFmpeg Equalizer & DSP audio effects
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
│   └── plugins/              # 59 Modular commands & feature plugins
│       ├── active.py         # Active voice chat tracker
│       ├── admin.py          # Group moderation (ban, mute, kick, purge, pin, staff)
│       ├── afk.py            # AFK status tracker
│       ├── antiflood.py      # Anti-flood spam protection
│       ├── assistant.py      # Assistant profile photo, bio, name & join/leave manager
│       ├── audio_fx.py       # Real-time DSP Equalizer & Audio FX
│       ├── auth.py           # Auth users manager
│       ├── autobio.py        # Assistant Auto-Bio real-time profile updater
│       ├── autodj.py         # Smart AutoPlay / AI DJ endless radio recommendation
│       ├── blacklist.py      # Blacklist / Whitelist manager
│       ├── broadcast.py      # Global broadcast manager
│       ├── callbacks.py      # Callback query router
│       ├── channel.py        # Channel Streaming (/cplay, /cpause, /cresume, /cstop)
│       ├── cleaner.py        # Automated cache garbage collector & disk cleaner
│       ├── downloader.py     # YouTube Video & MP3 Song Downloader
│       ├── effects.py        # Bot API 8.x/10.x visual message effects & reactions
│       ├── eval.py           # Python / Bash eval runner
│       ├── filters_notes.py  # Group custom filters & saved notes
│       ├── game.py           # Music Trivia Quiz game
│       ├── gban.py           # Cross-chat Global Ban (GBan) enforcement system
│       ├── iquery.py         # Telegram inline query search
│       ├── language.py       # Multi-language switcher
│       ├── leaveall.py       # Assistant leave inactive groups
│       ├── locks.py          # Chat permissions locks
│       ├── loop.py           # Loop stream controller
│       ├── lyrics.py         # Song lyrics scraper
│       ├── maintenance.py    # Maintenance mode, assistants status & DB backup
│       ├── misc.py           # Background timers & VC auto-leave
│       ├── pause.py          # Pause stream
│       ├── ping.py           # Health check & latency
│       ├── play.py           # Audio & Video streamer
│       ├── playlists.py      # Personal & group playlists manager
│       ├── queue.py          # Playlist queue viewer
│       ├── radio.py          # 24/7 Curated live radio stations
│       ├── record.py         # Voice chat audio recording
│       ├── replay.py         # Replay current song
│       ├── restart.py        # Clean restart & logs
│       ├── resume.py         # Resume stream
│       ├── search.py         # Interactive YouTube search
│       ├── seek.py           # Forward / Backward seek
│       ├── server_admin.py   # Host diagnostics, chat exports, announcements, reload
│       ├── session_gen.py    # In-bot interactive string session generator (Admin only)
│       ├── shazam.py         # Shazam song recognition
│       ├── shuffle.py        # Queue shuffle
│       ├── skip.py           # Skip to next song
│       ├── speed.py          # Playback speed controller
│       ├── speedtest.py      # Network speed diagnostics
│       ├── stars.py          # Telegram Stars tipping & invoices
│       ├── start.py          # Start & help menu
│       ├── stats.py          # System performance stats
│       ├── stop.py           # Stop playback
│       ├── sudoers.py        # Sudo users management
│       ├── tagall.py         # Batch mention group members
│       ├── tts.py            # Text to speech synthesizer
│       ├── variables.py      # Config & Environment variable inspector
│       ├── volume.py         # Audio volume controller
│       ├── watcher.py        # Voice chat event listener & queue cleaner
│       ├── webapp.py         # Interactive HTML5 Mini App music controller
│       └── welcome.py        # Custom welcome & clean service
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
