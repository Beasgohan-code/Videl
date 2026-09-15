# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl High-Performance MongoDB Database Engine

from time import time
from typing import List, Dict, Any, Optional

try:
    from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
except ImportError:
    from pymongo import AsyncMongoClient as MongoClient

from videl import config, logger


class MongoDB:
    def __init__(self):
        self.mongo: Optional[MongoClient] = None
        self.db = None
        if config.MONGO_URL:
            try:
                self.mongo = MongoClient(config.MONGO_URL, serverSelectionTimeoutMS=12500)
                self.db = self.mongo.Videl
            except Exception:
                pass

        # In-memory fast cache
        self.admin_list: Dict[int, List[int]] = {}
        self.active_calls: Dict[int, Dict[str, Any]] = {}
        self.admin_play: List[int] = []
        self.blacklisted: List[int] = []
        self.cmd_delete: List[int] = []
        self.loop: Dict[int, int] = {}
        self.volume: Dict[int, int] = {}
        self.speed: Dict[int, float] = {}
        self.notified: List[int] = []
        self.logger_enabled: bool = False

        self.assistant: Dict[int, int] = {}
        self.auth: Dict[int, List[int]] = {}
        self.chats: List[int] = []
        self.lang: Dict[int, str] = {}
        self.users: List[int] = []

    @property
    def assistantdb(self):
        return self.db.assistant if self.db is not None else None

    @property
    def authdb(self):
        return self.db.auth if self.db is not None else None

    @property
    def chatsdb(self):
        return self.db.chats if self.db is not None else None

    @property
    def langdb(self):
        return self.db.lang if self.db is not None else None

    @property
    def usersdb(self):
        return self.db.users if self.db is not None else None

    @property
    def sudodb(self):
        return self.db.sudoers if self.db is not None else None

    @property
    def bldb(self):
        return self.db.blacklist if self.db is not None else None

    @property
    def settingsdb(self):
        return self.db.settings if self.db is not None else None

    async def connect(self) -> None:
        """Ping MongoDB and load cache."""
        try:
            if not self.mongo:
                if not config.MONGO_URL:
                    raise SystemExit("Missing MONGO_URL environment variable.")
                self.mongo = MongoClient(config.MONGO_URL, serverSelectionTimeoutMS=12500)
                self.db = self.mongo.Videl

            start = time()
            await self.mongo.admin.command("ping")
            logger.info(f"Connected to MongoDB successfully in {time() - start:.2f}s")
            await self.load_cache()
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise SystemExit(f"Database connection failed: {e}")

    async def load_cache(self) -> None:
        """Pre-populate memory cache from MongoDB collections."""
        if self.db is None:
            return
        try:
            async for doc in self.chatsdb.find():
                self.chats.append(doc["chat_id"])
            async for doc in self.usersdb.find():
                self.users.append(doc["user_id"])
            async for doc in self.bldb.find():
                self.blacklisted.append(doc["chat_id"])
            async for doc in self.langdb.find():
                self.lang[doc["chat_id"]] = doc["lang"]
            async for doc in self.authdb.find():
                self.auth[doc["chat_id"]] = doc.get("users", [])
            async for doc in self.assistantdb.find():
                self.assistant[doc["chat_id"]] = doc["assistant_id"]
            async for doc in self.settingsdb.find():
                cid = doc["chat_id"]
                if doc.get("admin_play"):
                    self.admin_play.append(cid)
                if doc.get("cmd_delete"):
                    self.cmd_delete.append(cid)
            logger.info(f"Database cache loaded: {len(self.chats)} chats, {len(self.users)} users.")
        except Exception as ex:
            logger.warning(f"Warning during cache loading: {ex}")

    async def close(self) -> None:
        if self.mongo is not None:
            self.mongo.close()

    # Chat management
    async def is_chat(self, chat_id: int) -> bool:
        return chat_id in self.chats

    async def add_chat(self, chat_id: int) -> None:
        if chat_id not in self.chats:
            self.chats.append(chat_id)
            if self.chatsdb is not None:
                await self.chatsdb.update_one({"chat_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True)

    async def get_chats(self) -> List[int]:
        return list(self.chats)

    # User management
    async def is_user(self, user_id: int) -> bool:
        return user_id in self.users

    async def add_user(self, user_id: int) -> None:
        if user_id not in self.users:
            self.users.append(user_id)
            if self.usersdb is not None:
                await self.usersdb.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

    async def get_users(self) -> List[int]:
        return list(self.users)

    # Sudo management
    async def get_sudoers(self) -> List[int]:
        sudoers = [config.OWNER_ID]
        if self.sudodb is not None:
            async for doc in self.sudodb.find():
                sudoers.append(doc["user_id"])
        return list(set(sudoers))

    async def add_sudo(self, user_id: int) -> None:
        if self.sudodb is not None:
            await self.sudodb.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

    async def del_sudo(self, user_id: int) -> None:
        if self.sudodb is not None:
            await self.sudodb.delete_one({"user_id": user_id})

    # Blacklist management
    async def get_blacklisted(self) -> List[int]:
        return list(self.blacklisted)

    async def add_blacklist(self, chat_id: int) -> None:
        if chat_id not in self.blacklisted:
            self.blacklisted.append(chat_id)
            if self.bldb is not None:
                await self.bldb.update_one({"chat_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True)

    async def del_blacklist(self, chat_id: int) -> None:
        if chat_id in self.blacklisted:
            self.blacklisted.remove(chat_id)
            if self.bldb is not None:
                await self.bldb.delete_one({"chat_id": chat_id})

    # Admin list caching
    async def get_admins(self, chat_id: int, reload: bool = False) -> List[int]:
        from videl.helpers._admins import reload_admins
        if reload or chat_id not in self.admin_list:
            admins = await reload_admins(chat_id)
            self.admin_list[chat_id] = admins
            return admins
        return self.admin_list[chat_id]

    # Authorized users
    async def is_auth(self, chat_id: int, user_id: int) -> bool:
        return user_id in self.auth.get(chat_id, [])

    async def add_auth(self, chat_id: int, user_id: int) -> None:
        users = self.auth.get(chat_id, [])
        if user_id not in users:
            users.append(user_id)
            self.auth[chat_id] = users
            if self.authdb is not None:
                await self.authdb.update_one({"chat_id": chat_id}, {"$set": {"users": users}}, upsert=True)

    async def rm_auth(self, chat_id: int, user_id: int) -> None:
        users = self.auth.get(chat_id, [])
        if user_id in users:
            users.remove(user_id)
            self.auth[chat_id] = users
            if self.authdb is not None:
                await self.authdb.update_one({"chat_id": chat_id}, {"$set": {"users": users}}, upsert=True)

    async def _get_auth(self, chat_id: int) -> List[int]:
        return self.auth.get(chat_id, [])

    # Language
    async def get_lang(self, chat_id: int) -> str:
        return self.lang.get(chat_id, config.LANG_CODE)

    async def set_lang(self, chat_id: int, lang_code: str) -> None:
        self.lang[chat_id] = lang_code
        if self.langdb is not None:
            await self.langdb.update_one({"chat_id": chat_id}, {"$set": {"lang": lang_code}}, upsert=True)

    # Play mode (Admin only vs Everyone)
    async def get_play_mode(self, chat_id: int) -> bool:
        return chat_id in self.admin_play

    async def set_play_mode(self, chat_id: int, enable: bool) -> None:
        if enable and chat_id not in self.admin_play:
            self.admin_play.append(chat_id)
        elif not enable and chat_id in self.admin_play:
            self.admin_play.remove(chat_id)
        if self.settingsdb is not None:
            await self.settingsdb.update_one({"chat_id": chat_id}, {"$set": {"admin_play": enable}}, upsert=True)

    # Cleanmode / Command delete
    async def get_cmd_delete(self, chat_id: int) -> bool:
        return chat_id in self.cmd_delete

    async def set_cmd_delete(self, chat_id: int, enable: bool) -> None:
        if enable and chat_id not in self.cmd_delete:
            self.cmd_delete.append(chat_id)
        elif not enable and chat_id in self.cmd_delete:
            self.cmd_delete.remove(chat_id)
        if self.settingsdb is not None:
            await self.settingsdb.update_one({"chat_id": chat_id}, {"$set": {"cmd_delete": enable}}, upsert=True)

    # Active calls and playback status
    async def add_call(self, chat_id: int) -> None:
        self.active_calls[chat_id] = {"paused": False}

    async def remove_call(self, chat_id: int) -> None:
        self.active_calls.pop(chat_id, None)

    async def get_call(self, chat_id: int) -> bool:
        return chat_id in self.active_calls

    async def playing(self, chat_id: int, paused: Optional[bool] = None) -> bool:
        if chat_id not in self.active_calls:
            return False
        if paused is not None:
            self.active_calls[chat_id]["paused"] = paused
        return not self.active_calls[chat_id].get("paused", False)

    # Loop count
    async def get_loop(self, chat_id: int) -> int:
        return self.loop.get(chat_id, 0)

    async def set_loop(self, chat_id: int, count: int) -> None:
        self.loop[chat_id] = count

    # Volume & Speed
    async def get_volume(self, chat_id: int) -> int:
        return self.volume.get(chat_id, 100)

    async def set_volume(self, chat_id: int, vol: int) -> None:
        self.volume[chat_id] = vol

    async def get_speed(self, chat_id: int) -> float:
        return self.speed.get(chat_id, 1.0)

    async def set_speed(self, chat_id: int, spd: float) -> None:
        self.speed[chat_id] = spd

    # Assistant assignment
    async def get_assistant(self, chat_id: int):
        from videl import anon, userbot
        if not userbot.clients:
            raise RuntimeError("No userbot assistants available.")
        asst_id = self.assistant.get(chat_id)
        if asst_id:
            for idx, ub in enumerate(userbot.clients):
                if ub.id == asst_id:
                    return anon.clients[idx]
        chosen_idx = len(self.active_calls) % len(userbot.clients)
        chosen_ub = userbot.clients[chosen_idx]
        self.assistant[chat_id] = chosen_ub.id
        if self.assistantdb is not None:
            await self.assistantdb.update_one({"chat_id": chat_id}, {"$set": {"assistant_id": chosen_ub.id}}, upsert=True)
        return anon.clients[chosen_idx]

    async def get_client(self, chat_id: int):
        from videl import userbot
        if not userbot.clients:
            raise RuntimeError("No userbot assistants available.")
        asst_id = self.assistant.get(chat_id)
        if asst_id:
            for ub in userbot.clients:
                if ub.id == asst_id:
                    return ub
        chosen_idx = len(self.active_calls) % len(userbot.clients)
        return userbot.clients[chosen_idx]

    # Logger
    async def is_logger(self) -> bool:
        return self.logger_enabled

    async def set_logger(self, enable: bool) -> None:
        self.logger_enabled = enable
