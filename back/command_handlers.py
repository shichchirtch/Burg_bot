from aiogram import Router, html
import asyncio
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from filters import  IS_ADMIN, PRE_START
from aiogram.fsm.context import FSMContext
from bot_instance import FSM_ST
from aiogram_dialog import  DialogManager, StartMode
from  external_functions import get_user_count, get_total_months_count
from my_fast_api import r
from keyboards import pre_start_clava
from admin_dialog import ADMIN
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ch_router = Router()

@ch_router.message(CommandStart())
async def command_start_process(message:Message, dialog_manager: DialogManager, state:FSMContext):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    logger.warning("🔥 BOT HANDLER CALLED")
    # инициализировать профиль в Redis (если ещё нет)
    key_profile = f"user:{user_id}:profile"
    exists = await r.exists(key_profile)
    logging.getLogger().warning("Heir !!!")

    logger.warning(f"exists = {exists}")

    if not exists:
        await r.hset(key_profile, mapping={
            "first_name": user_name,
            "spam_opt_in": "0"
        })
        await r.sadd("users", user_id)  #  Добавляю в сэт tg_us_id

    users_started_bot_allready = await get_user_count()  #  Считаю юзеров

    await message.answer(text=f'Hallo, {html.bold(html.quote(user_name))}!\nIch bin MINI APP Bot'
                              f'Ich wurde bereits von <b>{users_started_bot_allready}</b> Nutzern, wie Ihnen, gestartet. 🎲', reply_markup=ReplyKeyboardRemove())
    await message.answer("Bitte klicken Sie auf den <b>Burg</b>, um die Web-App zu öffnen. ↙️")
    await dialog_manager.start(state=FSM_ST.spam, mode=StartMode.RESET_STACK)
    logger.warning('\n\n\nWe are hier !😀😀😀')



@ch_router.message(PRE_START())
async def before_start(message: Message):
    prestart_ant = await message.answer(text='Klicken auf <b>start</b> !',
                                        reply_markup=pre_start_clava)
    await message.delete()
    await asyncio.sleep(3)
    await prestart_ant.delete()


@ch_router.message(Command('admin'), IS_ADMIN())
async def basic_menu_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ADMIN.first)
    await asyncio.sleep(1)
    await message.delete()


@ch_router.message(Command('basic_menu'))
async def basic_menu_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=FSM_ST.start, mode=StartMode.RESET_STACK)


@ch_router.message(Command('help'))
async def command_help(message: Message, dialog_manager: DialogManager):
    await message.answer(text='help text')
    await dialog_manager.start(state=FSM_ST.basic, mode=StartMode.RESET_STACK)

@ch_router.message(Command('wieviel'))
async def command_wieviel(message: Message, dialog_manager: DialogManager):
    print('\n\nwork function comand_wieviel')
    wieviel = await get_user_count()
    zusammen_eintrag = await get_total_months_count()
    await message.answer(text=f'Bot wurde bereits von <b>{wieviel}</b> Nutzern, wie Ihnen, gestartet. 🎲\n\n'
                              f'Insgesamt wurden <b>{zusammen_eintrag}</b> Beiträge geleistet.')
    await dialog_manager.start(state=FSM_ST.basic, mode=StartMode.RESET_STACK)

@ch_router.message(Command('admin'), IS_ADMIN())
async def admin_enter(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ADMIN.first)
    await asyncio.sleep(1)
    await message.delete()