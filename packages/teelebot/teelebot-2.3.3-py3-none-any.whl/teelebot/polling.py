# -*- coding:utf-8 -*-
'''
@creation date: 2020-06-23
@last modification: 2023-05-14
'''
import os
import signal


def _runUpdates(bot):

    signal.signal(signal.SIGINT, __exit)
    while True:
        results = bot.getUpdates(
            offset=bot._offset,
            limit=100,
            timeout=bot._timeout,
            allowed_updates=bot._allowed_updates
        ) # Get the message queue 'messages'
        messages = bot._washUpdates(results)
        if messages is None or not messages:
            continue
        for message in messages:  # Retrieve a single message 'message'
            bot._pluginRun(bot, message)


def __exit(signum, frame):
    print("Bot Exit.")
    os._exit(0)


