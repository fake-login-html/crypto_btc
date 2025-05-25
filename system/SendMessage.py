from pyrogram import Client, utils
import asyncio

api_id = ''
api_hash = ''

# def get_peer_type_new(peer_id: int) -> str:
#     peer_id_str = str(peer_id)
#     if not peer_id_str.startswith("-"):
#         return "user"
#     elif peer_id_str.startswith("-100"):
#         return "channel"
#     else:
#         return "chat"

# utils.get_peer_type = get_peer_type_new


async def run(sms):

    # отправляем сообщение в чат
    client = Client(name="system/my_session", api_id=api_id, api_hash=api_hash)
    async with client:
        await client.send_message(chat_id=-1002398344294, text=sms)

def Send(sms):
    asyncio.run(run(sms=sms))


async def ref(sms):
    # редактируем закрепленное сообщение в чате
    client = Client(name="system/my_session", api_id=api_id, api_hash=api_hash)
    async with client:
        await client.edit_message_text(chat_id=-1002398344294, message_id=117, text=sms)

def Refactor(sms):
    asyncio.run(ref(sms=sms))


