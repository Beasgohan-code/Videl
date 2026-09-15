# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Lightweight HTTP Healthcheck Server (Koyeb, Render, Railway, Docker, UptimeRobot)

import os
import time
from aiohttp import web
from videl import app, boot, logger


async def healthcheck_handler(request):
    uptime_sec = int(time.time() - boot)
    return web.json_response({
        "status": "healthy",
        "bot": getattr(app, "name", "Videl Music"),
        "version": "3.8.0",
        "uptime_seconds": uptime_sec,
    })


async def start_server():
    port = int(os.environ.get("PORT", 8080))
    server_app = web.Application()
    server_app.router.add_get("/", healthcheck_handler)
    server_app.router.add_get("/health", healthcheck_handler)
    runner = web.AppRunner(server_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    try:
        await site.start()
        logger.info(f"Health check HTTP server started on port {port}.")
    except Exception as e:
        logger.debug(f"Health server note: {e}")
