import asyncio
import datetime as dt
from random import choice

import pytz

import db
import stickers
import templates
import weather


async def mailing(bot, logger):
    """Ежепятнадцатиминутная рассылка"""
    while True:
        seconds_delta, next_fifteen = _get_next_fifteen_minutes()
        await asyncio.sleep(seconds_delta)

        subscribers = await db.get_subscribers_by_mailing_time(next_fifteen)
        forecast, wtype = await weather.current_weather()
        for subscriber in subscribers:
            user_id = subscriber.id
            sticker = stickers.get_by_weather(wtype)
            await bot.send_sticker(user_id, sticker)
            msg = await bot.send_message(
                user_id, f"Ваш ежедневный прогноз 🤗\n\n{forecast}")
            logger.info(f"Пользователь {user_id} получил ежедневный прогноз")

            await bot.pin_chat_message(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                disable_notification=True,
            )


def _get_next_fifteen_minutes():
    """Получаем количество секунд до слеющуюшего времени, кратного 15 минутам"""
    now = _get_current_time()
    next_fifteen = _round_time_by_fifteen_minutes(now) + dt.timedelta(minutes=15)
    seconds_delta = _get_time_difference(next_fifteen, now)
    return seconds_delta, next_fifteen.time()


def _get_current_time():
    return dt.datetime.now(pytz.timezone("Europe/Moscow"))


def _round_time_by_fifteen_minutes(time):
    return time.replace(
        minute=time.minute // 15 * 15,
        second=0,
        microsecond=0)


def _get_time_difference(time1, time2):
    return (time1 - time2).total_seconds()


async def get_user_mailing_info(user_id):
    """Получаем информацию о подписке пользователя"""
    is_subscriber = await db.is_user_in_subscription(user_id)
    if is_subscriber:
        time = await db.get_subscriber_mailing_time(user_id)
        return templates.USER_IN_MAILING.format(time.hour, time.minute)
    return templates.USER_NOT_IN_MAILING
