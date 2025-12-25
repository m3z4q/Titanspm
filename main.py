import time
import random
import threading
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)
from telegram.error import RetryAfter, BadRequest

# ================= MULTI BOT TOKENS =================
BOT_TOKENS = [
    "8519181173:AAF9dPbQ5J5N_Q6iAaQBULFpaDJTX_CNmGs",
    "8510189857:AAE1FWYZcsLRM_a8vMBoytnpbkGxaQN5Tok",
    "8017630980:AAE622-he5-FFoZ9PkTpdS2nO9lLY0nCd8g"
]

OWNER_ID = 8453291493

raid_tasks = {}
gcnc_tasks = {}

EMOJIS = ["🔥","⚡","💀","👑","😈","🚀","💥","🌀","🧨","🎯","🐉","🦁","☠️"]

# ================= COMMANDS =================
async def start(update, context):
    await update.message.reply_text("🤖 Multi Bot Online\n/help")

async def help_cmd(update, context):
    await update.message.reply_text(
        "/spam <count> <text>\n"
        "/raid <count> <text>\n"
        "/stopraid\n"
        "/gcnc <count> <name>\n"
        "/stopgcnc"
    )

async def spam(update, context):
    try:
        count = int(context.args[0])
        text = " ".join(context.args[1:])
        for _ in range(count):
            await update.message.reply_text(text)
            await context.application.bot._loop.create_task(
                context.application.bot._loop.run_in_executor(None, time.sleep, 0.4)
            )
    except:
        await update.message.reply_text("Usage: /spam <count> <text>")

async def gcnc(update, context):
    parts = update.message.text.split(maxsplit=2)
    if len(parts) < 3:
        await update.message.reply_text("Usage: /gcnc <count> <name>")
        return

    chat = update.effective_chat
    base = parts[2]

    async def loop():
        i = 0
        while True:
            try:
                await chat.set_title(f"{random.choice(EMOJIS)} {base} {i+1}")
                i += 1
                await context.application.bot._loop.run_in_executor(None, time.sleep, 2)
            except RetryAfter as e:
                await context.application.bot._loop.run_in_executor(None, time.sleep, e.retry_after)
            except BadRequest:
                await context.application.bot._loop.run_in_executor(None, time.sleep, 5)

    gcnc_tasks[chat.id] = context.application.create_task(loop())
    await update.message.reply_text("✅ GC Name Change Started")

# ================= BOT THREAD =================
def start_bot(token):
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("spam", spam))
    app.add_handler(CommandHandler("gcnc", gcnc))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))

    print(f"✅ Bot running: {token[:10]}")
    app.run_polling()

# ================= MAIN =================
if __name__ == "__main__":
    for token in BOT_TOKENS:
        threading.Thread(target=start_bot, args=(token,), daemon=True).start()

    while True:
        time.sleep(10)
