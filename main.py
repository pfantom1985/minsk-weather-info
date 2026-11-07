import re
from os import getenv

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from dotenv import load_dotenv

from handlers.routes import router

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
WEBHOOK_SECRET = getenv("WEBHOOK_SECRET")
WEBHOOK_PATH = "/webhook"
_SECRET_RE = re.compile(r"^[A-Za-z0-9_-]{1,256}$")

dp = Dispatcher()
dp.include_router(router)


def webhook_url() -> str:
    domain = getenv("RAILWAY_PUBLIC_DOMAIN")
    if not domain:
        raise RuntimeError("RAILWAY_PUBLIC_DOMAIN is not set")
    return f"https://{domain}{WEBHOOK_PATH}"


async def on_startup(bot: Bot) -> None:
    url = webhook_url()
    await bot.set_webhook(
        url,
        secret_token=WEBHOOK_SECRET,
        drop_pending_updates=False,
    )
    print(f"Webhook set: {url}")


async def health(_: web.Request) -> web.Response:
    return web.Response(text="ok")


def main() -> None:
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")
    if not WEBHOOK_SECRET or not _SECRET_RE.fullmatch(WEBHOOK_SECRET):
        raise RuntimeError("WEBHOOK_SECRET must be 1-256 chars: A-Z a-z 0-9 _ -")

    bot = Bot(token=TOKEN)
    dp.startup.register(on_startup)

    app = web.Application()
    app.router.add_get("/", health)
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    ).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host="0.0.0.0", port=int(getenv("PORT", "8080")))


if __name__ == "__main__":
    main()
