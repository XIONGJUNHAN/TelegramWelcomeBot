#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.

This program is dedicated to the public domain under the CC0 license.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
#def start(bot, update):
#    """Send a message when the command /start is issued."""
#    update.message.reply_text('Hi!')

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Sorry I am just a welcome bot. 我啥也不知道。')


def joke(bot, update):
    """Tell a joke."""
    update.message.reply_text("No. No joke today. 讲不动笑话了。。")

def website(bot, update):
    """Tell the website url"""
    update.message.reply_text("https://www.dmstoken.com")

def haha(bot, update, job_queue):
    """Echo the user message."""
    block_list = job_queue.get_jobs_by_name('block')[0].context
    uid = update.message.from_user.id
    print block_list, uid
    if uid not in block_list:
        update.message.reply_text(r"I cannot help you but you can always ask @SujiYan. 有事问 @SujiYan，他全知道。")
        job_queue.get_jobs_by_name('block')[0].context.append(uid)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def welcome(bot, update, job_queue, chat_data):
    for u in update.message.new_chat_members:
        print u.username
        if u.username == None:
            job_queue.get_jobs_by_name('welcome')[0].context[0].append('%s %s' % (u.first_name, u.last_name))
        else:
            job_queue.get_jobs_by_name('welcome')[0].context[0].append(u.username)
        #can do group welcome
        job_queue.get_jobs_by_name('welcome')[0].context[1] = update.message.chat_id

def realWelcome(bot, job):
    if job.context[1] == None or job.context[0] == []:
        return
    else:
        welcomeList = list(set(job.context[0]))
        print 'welcome @%s' % (', @'.join(welcomeList))
        bot.send_message(job.context[1], 'welcome @%s' % (', @'.join(welcomeList)))
        job.context[0] = []

def block(bot, job):
    job.context = []
    return

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    welcomeList = []
    token = '507524179:AAHVM1s7VLEabaRUwTJUPOUWQKMJBBtYD-A'
    updater = Updater("%s"%token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    #dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("joke", joke))
    dp.add_handler(CommandHandler("website", website))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex('@realSujiBot'), haha, pass_job_queue = True))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome, pass_job_queue = True, pass_chat_data = True))

    # run repeatedly
    dp.job_queue.run_repeating(realWelcome, 30, context = [[], None], name = 'welcome')
    dp.job_queue.run_repeating(block, 7200, context = [], name = 'block')

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
