import requests
from zerotwobot import application
from zerotwobot.modules.disable import DisableAbleCommandHandler
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext


async def paste(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message

    if message.reply_to_message:
        data = message.reply_to_message.text

    elif len(args) >= 1:
        data = await message.text.split(None, 1)[1]

    else:
        await message.reply_text("What am I supposed to do with this?")
        return

    key = (
        requests.post("https://nekobin.com/api/documents", json={"content": data})
        .json()
        .get("result")
        .get("key")
    )

    url = f"https://nekobin.com/{key}"

    reply_text = f"Nekofied to *Nekobin* : {url}"

    await message.reply_text(
        reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True,
    )


PASTE_HANDLER = DisableAbleCommandHandler("paste", paste, block=False)
application.add_handler(PASTE_HANDLER)

__command_list__ = ["paste"]
__handlers__ = [PASTE_HANDLER]
