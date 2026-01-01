from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
import os
from bot_instance import bot
import logging
import redis.asyncio as aioredis

r = aioredis.Redis(host=os.getenv("REDIS_HOST", "redis1226"),
                     port=int(os.getenv("REDIS_PORT", 6379)),
                   decode_responses=True)

ADMIN_ID = 6685637602


f_api = FastAPI(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
)

logger = logging.getLogger("fastapi")

@f_api.get("/")
async def root():
    return {"root": True}

@f_api.post("/test")
async def test():
    return {"ok": True}


@f_api.get("/ping")
async def ping():
    return {"pong": True}


@f_api.post("/api/receive_telegram_data")
async def receive_telegram_data(data: dict):
    print("PY Charm speak 📦 Полученные данные от Telegram:", data)
    user_id = data["user_id"]
    logger.warning(f"📦 Telegram data: {data}")
    await bot.send_message(chat_id= ADMIN_ID,
                           text = f"user_id from webapp: {user_id}")
    return {"ok": True}

@f_api.post("/api/start-test")
async def start_test(data: dict):
    print("✅ START TEST CALLED", data)
    return {
        "ok": True,
        "message": "Backend is alive",
        "user_id": data.get("user_id")
    }


@f_api.post("/api/get-user-months")
async def get_user_months(request: Request):
    data = await request.json()
    print('data = ', data)
    user_id = data["user_id"]
    # Формируем ключ по которому можно достучаться до месяцев юзера
    key_months = f"user:{user_id}:months"
    print('key_months = ', key_months)

    # получаем все месяцы из SET
    raw_months = await r.smembers(key_months)
    print('Месяцы юзера = ', raw_months)

    # приводим к формату фронта
    monaten = []
    for item in raw_months:
        year, month = item.split(":")
        monaten.append({
            "year": int(year),
            "month": month
        })


    # if user_id not in users_db:  # Не удалять !
    #     users_db[user_id] = {"monaten": []}

    return {"monaten": monaten }


@f_api.post("/api/month-select")
async def month_select(request: Request):
    data = await request.json()
    print('coming data = ', data)
    logger.warning(f"📦LOGGER 84 : {data}")
    user_id = data["user_id"]
    month = data["month"]
    year = data["year"]
    selected = data["selected"]


    key_months = f"user:{user_id}:months"
    value = f"{year}:{month}"
    if selected:
        # добавить месяц

        await r.sadd(key_months, value)
    else:
        # удалить месяц
        await r.srem(key_months, value)

        await bot.send_message(
                chat_id=user_id,
                text=f"❌ Der Monat <b> {month}  {year} </b> wurde aus Ihrer Datenbank entfernt."
            )

    # вернуть обновлённый список
    raw_months = await r.smembers(key_months)

    monaten = []
    for item in raw_months:
        y, m = item.split(":")
        monaten.append({
            "year": int(y),
            "month": m
        })

    return {
        "status": "ok",
        "monaten": monaten
    }
