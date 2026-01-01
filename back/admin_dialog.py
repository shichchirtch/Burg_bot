from aiogram_dialog import Dialog, Window, ShowMode
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Row, Next, Cancel
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from bot_instance import ADMIN, ABOUT, bot, FSM_ST
from aiogram.types import ContentType
import asyncio
from aiogram.exceptions import TelegramForbiddenError
from my_fast_api import r
from static_func import check_len_note

admin_id = 6685637602




async def accepet_admin_message(msg:Message, widget: MessageInput, dialog_manager: DialogManager, *args, **kwargs):
    dialog_manager.dialog_data['admin_msg'] = msg.text
    await dialog_manager.next()

async def get_users_for_spam():
    result = []

    user_ids = await r.smembers("users")
    for user_id in user_ids:
        key = f"user:{user_id}:profile"
        spam = await r.hget(key, "spam_opt_in")
        if spam == "2":
            result.append(int(user_id))

    return result


async def sending_msg(cb:CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
        text_from_admin = dialog_manager.dialog_data['admin_msg']
        if text_from_admin.startswith('one'):
            prefix, us_id, text_msg = text_from_admin.split('$') # one$12345678$admin_text
            user_id = int(us_id)
            try:
                await cb.bot.send_message(chat_id=user_id, text=text_msg)
                await cb.message.answer('Message is sent !')
            except Exception as e:
                await cb.message.answer(f'Msg is not sent due to {e}')
            await dialog_manager.done()
        else:
            spam_list = await get_users_for_spam()

            for taker in spam_list:
                chat_id = int(taker)
                try:
                    await cb.bot.send_message(chat_id=chat_id, text=text_from_admin)
                except TelegramForbiddenError:
                    pass
                except Exception as ex:
                    print(f'Admin sending exception happend  {ex}')
                await asyncio.sleep(0.2)  # Жду 0.2 секунды
            await cb.message.answer('Mailing done')
            await dialog_manager.done()


admin_dialog = Dialog(
    Window(
        Const('Возможные дейсвтия'),
        Next(
                    text=Const('Отправить сообщение юзерам'),
                    id='send_msg'),
        state=ADMIN.first
    ),
    Window(  # Принимает текст сообщения и записывает его в словарь data
        Const(text='введите текст сообщения'),
        Cancel(
                text=Const('◀️'),
                id='admin_out_1',
                ),
        MessageInput(
            func=accepet_admin_message,
            content_types=ContentType.TEXT,
        ),
        state=ADMIN.accept_msg
    ),
    Window(  # Отправляет сообщение юзерам
        Const('Отправить сообщуху'),
        Row(Cancel(
                text=Const('◀️'),
                id='admin_out_2',
                ),
            Button(
                text=Const('Отправить сообщение юзерам'),
                id='send_msg_fin',
                on_click=sending_msg)),
        state=ADMIN.admin_send_msg)
)



async def message_text_acc(message: Message, widget: MessageInput, dialog_manager: DialogManager) -> None:
    print('we into message_text_acc')
    name = message.from_user.first_name
    user_name = message.from_user.username
    note = check_len_note(message.text)
    note = f'{note}\n\n\n von {name}  {user_name}'
    await bot.send_message(admin_id, note)
    await asyncio.sleep(1)

    await message.answer(text=f'Die Nachricht wurde erfolgreich gesendet.')
    await asyncio.sleep(1)
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    await dialog_manager.done()


about_dialog = Dialog(
    Window(
        Const('<b>Über das Projekt</b>\n\n'
    'Dieser Bot kombiniert folgende Technologien:\n\n'
    '✅ <b>aiogram_dialog</b>\n'
    '✅ <b>FastAPI</b>\n'
    '✅ <b>React + Vite</b>\n'
    '✅ <b>Redis als Datenbank</b>\n\n'
    'Um den Entwickler zu kontaktieren, senden Sie eine Nachricht.'),
        Row(Next(Const('✉️'),
                 id="schreib_nachrichten",
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










