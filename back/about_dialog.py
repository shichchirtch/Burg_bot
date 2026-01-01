import asyncio, json
from aiogram_dialog import Dialog, StartMode, Window, DialogManager, ShowMode
from aiogram.types import Message, CallbackQuery

from back.bot_instance import FSM_ST
from bot_instance import ABOUT, bot
from aiogram.types import ContentType
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row, Cancel, Select, Group, Next
from aiogram_dialog.widgets.input import MessageInput
from my_fast_api import r
from static_func import check_len_note


async def schreiben_msg(c: CallbackQuery, button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["page"] -= 1
    await dialog_manager.show()

async def message_text_acc(message: Message, widget: MessageInput, dialog_manager: DialogManager) -> None:
    print('we into message_text_acc')
    user_id = message.from_user.id
    us_data = message.from_user
    print('us_data = ', us_data)
    user_name = message.from_user.first_name
    note = check_len_note(message.text)
    note = f'{note}\n\n\n von {user_name}'
    await bot.send_message(user_id, note)

    await asyncio.sleep(1)

    await message.answer(text=f'Die Nachricht wurde erfolgreich gesendet.')
    await asyncio.sleep(1)
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    await dialog_manager.switch_to(FSM_ST.start)



about_dialog = Dialog(
    Window(
        Const('<b>Über das Projekt</b>\n\n'
              'Dieser Bot kombiniert folgende Technologien:\n\n'
                '✅ <b>aiogram_dialog</b>\n\n'
              '✅<b>Fast API</b>\n\n'
              '✅ <b>React+Vite</b>\n\n'
              '✅ <b>Redis wie Datenbank</b>\n\n\n',
                'Um den Entwickler zu kontaktieren, senden Sie eine Nachricht.'),
        Row(Next(Const('✉️'),
            id="schreib_nachrichten",
            on_click=schreiben_msg,
        ),
            Cancel(Const("◀️ Zurück"),
               id="back")),
        state=ABOUT.one,
    ),
Window(
    Const("Senden Sie eine Nachricht an den Entwickler"),
    MessageInput(
        func=message_text_acc,
        content_types=ContentType.TEXT,
    ),
    Cancel(Const('◀️'),
           id='about_acc'),
    state=ABOUT.accepting,
))

