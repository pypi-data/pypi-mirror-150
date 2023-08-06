#!/usr/bin/env python3
import logging
from functools import wraps
from pathlib import Path
from os import access, R_OK

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler
from telegram.utils.helpers import escape_markdown

logging.basicConfig(
    format=" * %(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

global_users_whitelist = []


def whitelist_only(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user = update.effective_user
        logger.info(
            f"@{user.username} ({user.id}) is trying to access a privileged command"
        )
        if user.username not in global_users_whitelist:
            logger.warning(f"Unauthorized access denied for {user.username}.")
            text = (
                "🚫 *ACCESS DENIED*\n"
                "Sorry, you are *not authorized* to use this command"
            )
            update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
            return
        return func(update, context, *args, **kwargs)

    return wrapped


def parse_args(context_args):
    for arg in context_args:
        try:
            path_alias = arg
            path = Path(path_alias).expanduser()
            msg_text = f"`{path}`"
            if path.exists():
                if not access(path, R_OK):
                    raise PermissionError
                yield True, path, msg_text
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            error_text = (
                f"❌\n*{path}* does not exist.\n"
                f"Make sure  alias `{path_alias}` is pointing to an existing file"
            )
            yield False, arg, error_text
        except PermissionError:
            error_text = (
                f"❌\n*{path}*: permission denied.\n"
            )
            yield False, arg, error_text
        except AttributeError:
            # sometimes editing a previously sent chat message
            # triggers the handler with an empty update
            pass


@whitelist_only
def fetch_file(update, context):
    """Send a message or a file when the command /fetch [alias] is issued."""
    if context.args:
        for is_valid, arg, text in parse_args(context.args):
            if is_valid:
                logger.info(f"Sending {arg} to {update.effective_user.username}")
                f = open(arg, 'rb')
                update.message.reply_document(f, caption=text, parse_mode=ParseMode.MARKDOWN)
            else:
                update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

    else:
        text = (
            "⚠️\nPlease provide a configured path:\n"
            "`/fetch log_alias`\n"
            "You can add them to `paths.py`"
        )
        update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


@whitelist_only
def tail_file(update, context):
    tail_len = 10
    if context.args:
        for is_valid, arg, text in parse_args(context.args):
            if is_valid:
                logger.info(f"Tailing {arg} to {update.effective_user.username}")
                with arg.open('r') as f:
                    text = '\n'.join([escape_markdown(line) for line in list(f)[-tail_len:]])
            update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

    else:
        text = (
            "⚠️\nPlease provide a configured path:\n"
            "`/tail log_alias`\n"
        )
        update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


class Squire:
    def __init__(self, token: str, users_whitelist: list):
        self.token = token
        self.users_whitelist = users_whitelist
        global global_users_whitelist
        global_users_whitelist = list.copy(self.users_whitelist)
        self.updater = Updater(self.token, use_context=True)

        self.dp = self.updater.dispatcher
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("help", self.show_help))
        self.dp.add_handler(CommandHandler("fetch", fetch_file))
        self.dp.add_handler(CommandHandler("tail", tail_file))
        self.dp.add_error_handler(self.error)

        self.updater.start_polling()
        logger.info("BOT DEPLOYED. Ctrl+C to terminate")

        self.updater.idle()

    def start(self, update, context):
        """Send a message when the command /start is issued."""
        text = (
            "Hi!"
            "I can /fetch or /tail you some files if you are whitelisted\n"
            "/help to learn more"
        )
        update.message.reply_text(text)

    def show_help(self, update, context):
        """Send a message when the command /help is issued."""
        howto = (
            f"▪Fetch files using the `/fetch` command.\n"
            f"\tE.g., `/fetch /etc/passwd` or `/tail /etc/passwd`"
        )
        update.message.reply_text(howto, parse_mode=ParseMode.MARKDOWN)

    def error(self, update, context):
        error = context.error
        logger.warning(f"Update {update} caused error '{type(error)}': {error}")
