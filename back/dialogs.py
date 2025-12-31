from aiogram_dialog import Dialog, StartMode, Window, DialogManager, ShowMode
from aiogram.types import Message, CallbackQuery
from bot_instance import FSM_ST, CREATE, ZEIGEN, dp, bot_storage_key
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import (Button, Row, Cancel, Select, Radio,
                                        Next, Start, Group, Back, SwitchTo)
from aiogram_dialog.widgets.input import TextInput, MessageInput, ManagedTextInput
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram.types import ContentType
import json
import operator, asyncio, datetime
from external_functions import radio_spam_button_clicked
from static_func import *
from my_fast_api import r
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_spam(dialog_manager: DialogManager, **kwargs):
    spam = [('🤢', '1'), ('😃', '2')]
    check_info = dialog_manager.dialog_data.get('spam_wahl', '')
    print('Print works !\n\n')
    logger.info('Loger works !\n\n')
    return {"spam_data": spam, 'spam_wahl': check_info}


async def message_text_handler(message: Message, widget: MessageInput, dialog_manager: DialogManager) -> None:
    print('we into message_text_handler')
    user_id = str(message.from_user.id)
    note = check_len_note(message.text)
    heute = datetime.datetime.now().strftime('%d.%m.%Y')
    note = f'{note}\n\n {heute}'
    dialog_manager.dialog_data['note'] = note
    dialog_manager.dialog_data['foto_id'] = ''
    notiz_key = form_key_note(note)

    await r.hset(
        f"user:{user_id}:notes",
        notiz_key,
        json.dumps({
            "text": note,
            "foto_id": ''
        })
    )

    await asyncio.sleep(1)

    await message.answer(text=f'Gut, Diese Note wurde in deine Noten beifügen')
    await asyncio.sleep(1)
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    await message.delete()
    await dialog_manager.switch_to(CREATE.finish)


async def accepting_foto(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    foto_id = message.photo[-1].file_id
    dialog_manager.dialog_data['foto_id'] = foto_id
    heute = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
    capture = f'Foto {heute}'
    dialog_manager.dialog_data['capture'] = capture
    # bot_dict = await dp.storage.get_data(key=bot_storage_key)  # Получаю словарь бота
    # print('FOTO = ', bot_dict)
    user_id = str(message.from_user.id)
    # user_dict = bot_dict[user_id]
    # user_dict['notes'][capture] = foto_id
    # await dp.storage.update_data(key=bot_storage_key, data=bot_dict)

    await r.hset(
        f"user:{user_id}:notes",
        capture,
        json.dumps({
            "text": capture,
            "foto_id": foto_id
        })
    )

    dialog_manager.show_mode = ShowMode.SEND
    await dialog_manager.next()


async def message_not_foto_handler(message: Message, widget: MessageInput,
                                   dialog_manager: DialogManager) -> None:
    dialog_manager.show_mode = ShowMode.NO_UPDATE
    await message.answer('Senden Sie mir den Text oder das Foto')


async def set_foto_notiz_ohne_capture(cb: CallbackQuery, widget: Button, dialog_manager: DialogManager) -> None:
    """Хэндлер формирует словарь с фото без подписи"""
    await cb.message.answer(text='eingegeben')
    dialog_manager.show_mode = ShowMode.SEND
    await dialog_manager.done()


async def message_capture_handler(message: Message, widget: MessageInput, dialog_manager: DialogManager) -> None:
    """Хэндлер устанавливает capture"""
    user_id = str(message.from_user.id)
    capture = form_capture(message.text)
    foto_id = dialog_manager.dialog_data['foto_id']
    old_capture = dialog_manager.dialog_data['capture']
    redis_key = f"user:{user_id}:notes"
    notes_keys = await r.hkeys(f"user:{user_id}:notes")
    print("1 notes_keys =", notes_keys)
    await r.hdel(redis_key, old_capture)

    heute = datetime.datetime.now().strftime('%d.%m.%Y')
    capture = f'{capture}\n\n {heute}'
    notiz_key = form_capture(capture)
    print('nitiz_key =', notiz_key)
    await r.hset(
        f"user:{user_id}:notes",
        notiz_key,
        json.dumps({
            "text": notiz_key,
            "foto_id": foto_id
        })
    )
    notes_keys = await r.hkeys(f"user:{user_id}:notes")
    print("2 notes_keys =", notes_keys)

    await message.answer(text='Capture wurde in deine  Foto')
    dialog_manager.show_mode = ShowMode.SEND
    await message.delete()
    await dialog_manager.next()


async def message_not_text_handler_in_capture(message: Message, widget: MessageInput,
                                              dialog_manager: DialogManager) -> None:
    dialog_manager.show_mode = ShowMode.NO_UPDATE
    await message.answer('schick mir Text')


async def reset_funk(callback: CallbackQuery, widget: Button,
                     dialog_manager: DialogManager, *args, **kwargs):
    print('reset funk works')
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    dialog_manager.dialog_data.clear()



async def peredumal_func(callback: CallbackQuery, widget: Button,
                            dialog_manager: DialogManager, *args, **kwargs):
    print('peredumal_funk works')
    user_id = str(callback.from_user.id)
    capture = dialog_manager.dialog_data['capture']
    redis_key = f"user:{user_id}:notes"
    await r.hdel(redis_key, capture)
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    dialog_manager.dialog_data.clear()
    await dialog_manager.done()




start_dialog = Dialog(
    Window(
        Const('Möchten Sie Nachrichten vom Bot erhalten ?'),
        Row(
            Radio(
                checked_text=Format('🔘 {item[0]}'),
                unchecked_text=Format('⚪️ {item[0]}'),
                id='spam_window',
                item_id_getter=operator.itemgetter(1),
                items="spam_data",
                on_state_changed=radio_spam_button_clicked,
            ),
        ),
        state=FSM_ST.spam,
        getter=get_spam
    ),

    Window(
        Const('eine Notiz erstellen 👇'),
        Row(
            Start(
                text=Const('Neue Notiz erstellen'),
                id='kuck_start',
                state=CREATE.einstellen),
            Start(
                text=Const('Kuck meine Notizen'),
                id='save_bd',
                state=ZEIGEN.clava),
        ),
        state=FSM_ST.start))

create_dialog = Dialog(
    Window(
        Const('Typen hier oder schick mir eine Foto'),
        MessageInput(
            func=message_text_handler,
            content_types=ContentType.TEXT,
        ),
        MessageInput(
            func=accepting_foto,
            content_types=ContentType.PHOTO,
        ),
        MessageInput(
            func=message_not_foto_handler,
            content_types=ContentType.ANY,
        ),
        Cancel(Const('◀️'),
               id='Cancel_for_uniq_day'),
        state=CREATE.einstellen,
    ),
    Window(  # Окно предлагающее ввести capture
        Const('Eingeben Captura'),  # Хотите сделать подпись по фотографией ?
        Button(Const('◀️'),
               id='return_to_basic',
               on_click=peredumal_func),
        Row(Next(Const('😃'),
                 id='yes_capture'),
            Button(Const('❌'),
                   id='no_capture',
                   on_click=set_foto_notiz_ohne_capture)),

        state=CREATE.ask_capture,
    ),

    Window(  # Окно принимающее capture
        Format(text='Schiken mir Capture !'),  # Отправьте capture
        MessageInput(
            func=message_capture_handler,
            content_types=ContentType.TEXT,
        ),
        MessageInput(
            func=message_not_text_handler_in_capture,
            content_types=ContentType.ANY,
        ),
        Cancel(Const('◀️'),
               id='Cancel_for_accepting_capture'),
        state=CREATE.enter_capture,
    ),
    Window(  # окно возвращаюшее в предыдущий диалог
        Const(text='Notiz akzeptiert !'),  # Напоминание принято
        Cancel(text=Format(text='▶️'),  #
               id='see_stelle_button',
               on_click=reset_funk),
        state=CREATE.finish))

