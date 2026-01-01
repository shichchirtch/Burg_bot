from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import StorageKey, MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.fsm.storage.base import DefaultKeyBuilder
from config import settings


key_builder = DefaultKeyBuilder(with_destiny=True)

aiogram_redis = Redis(
    host=settings.REDIS_HOST      ,#os.getenv("REDIS_HOST", "redis1226"),
    port=settings.REDIS_PORT,#int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
)

redis_storage = RedisStorage(redis=aiogram_redis, key_builder=key_builder)

BOT_TOKEN = settings.BOT_TOKEN #'8307999623:AAHLxJHj0SRFJRhhZe284VHICQTULOy6OpY'   # '<BOT_TOKEN>'

bot = Bot(token=BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

bot_storage_key = StorageKey(bot_id=bot.id, user_id=bot.id, chat_id=bot.id)

dp = Dispatcher(storage=redis_storage)




class FSM_ST(StatesGroup):
    spam = State()
    start = State()
    basic = State()
    vacancies = State()

class CREATE(StatesGroup):
    einstellen = State()
    ask_capture = State()
    enter_capture = State()
    finish = State()


class ZEIGEN(StatesGroup):
    clava = State()
    list_notes = State()
    schlist = State()

class ADMIN(StatesGroup):
    first = State()
    accept_msg = State()
    admin_send_msg = State()



server_cart = {}