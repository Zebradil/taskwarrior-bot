import re
import os
import shlex
import sys
import logging

import subprocess

from telegram import ParseMode

from taskw import TaskWarrior

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TASK_DIRECTORY = 'task'
TASKRC = os.path.join(os.getcwd(), TASK_DIRECTORY, '.taskrc')
taskwarrior = None
data_location = ''


def init_taskwarrior(func):
    def wrapper(*args, **kwargs):
        # There are always (bot, update) arguments
        user_id = args[1].message.from_user.id
        data_location = os.path.join(os.getcwd(), TASK_DIRECTORY, str(user_id))
        taskwarrior = TaskWarrior(config_filename=TASKRC, config_overrides={'data': {'location': data_location}})

        return func(*args, **kwargs)

    return wrapper


def execute(command):
    proc = subprocess.Popen(
        ['task'] + shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
    return stdout.decode(), stderr.decode()


def start_bot(bot, update):
    bot.sendMessage(update.message.chat_id, text='Some helpful text')


def report(bot, update):
    pass


def add(bot, update):
    pass


def update(bot, update):
    pass


def done(bot, update):
    pass


def delete(bot, update):
    pass


def info(bot, update):
    pass


def start(bot, update):
    pass


def stop(bot, update):
    pass


def annotate(bot, update):
    pass


def denotate(bot, update):
    pass


@init_taskwarrior
def task(bot, update):
    result = taskwarrior
    bot.sendMessage(
        update.message.chat_id,
        text='<pre>{0}</pre>'.format(sys.stdout),
        parse_mode=ParseMode.HTML
    )


def parse_command(text):
    available_commands = [
        'report',
        'add',
        'update',
        'done',
        'delete',
        'info',
        'start',
        'stop',
        'annotate',
        'denotate',
    ]
    p = re.compile('^/({0}) ?(.*)'.format('|'.join(available_commands)))
    try:
        return p.match(text).groups()
    except:
        return None, None


@init_taskwarrior
def handle_command(bot, update):
    command, arguments = parse_command(update.message.text)
    globals()[command](arguments)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(sys.argv[1])

updater.dispatcher.add_handler(MessageHandler(Filters.all, lambda bot, update: print(update)), group=1)
updater.dispatcher.add_handler(MessageHandler(Filters.command, handle_command), group=1)
updater.dispatcher.add_handler(CommandHandler('start', start_bot))

updater.start_polling()
updater.idle()
