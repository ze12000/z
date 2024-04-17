#import asyncio
from pyrogram import Client, filters
#from datetime import datetime
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatPermissions, ChatPrivileges
from config import *

welcome_enabled = True

SUDOERS = [5881570606,5652812673]
OWNER_ID = 5881570606




def is_sudoer(_, __, message):

    return message.from_user.id in SUDOERS or message.from_user.id == OWNER_ID

def is_owner(_, __, message):

    return message.from_user.id == OWNER_ID







chat_locked = False
mention_locked = False
video_locked = False
link_locked = False
sticker_locked = False
forward_locked = False
reply_locked = False
photo_locked = False




@Client.on_chat_member_updated()
async def welcome(client, chat_member_updated):
    if not welcome_enabled:
        return
    
    if chat_member_updated.new_chat_member.status == ChatMemberStatus.BANNED:
        kicked_by = chat_member_updated.new_chat_member.restricted_by
        user = chat_member_updated.new_chat_member.user
        
        if kicked_by is not None and kicked_by.is_self:
            messagee = f"• المستخدم {user.username} ({user.first_name}) تم طرده من الدردشة بواسطة البوت"
        else:
            if kicked_by is not None:
                message = f"• المستخدم [{user.first_name}](tg://user?id={user.id}) \n• تم طرده من الدردشة بواسطة [{kicked_by.first_name}](tg://user?id={kicked_by.id})\n• ولقد طردته بسبب هذا"
                try:
                    await client.ban_chat_member(chat_member_updated.chat.id, kicked_by.id)
                except Exception as e:
                    message += f"\n\nعذرًا، لم استطع حظر الإداري بسبب: {str(e)}"
            else:
                message = f"• المستخدم {user.username} ({user.first_name}) تم طرده من الدردشة"
            
            
        
        await client.send_message(chat_member_updated.chat.id, message)





@Client.on_message(filters.command("اضف مطور", "") & filters.create(is_sudoer))
async def add_dev(client, message):
    username = message.text.split()[2]
    if username not in SUDOERS:
        SUDOERS.append(username)
        await message.reply_text("تمت إضافة المطور بنجاح.")
    else:
        await message.reply_text("المطور موجود بالفعل.")

@Client.on_message(filters.command("ازالة مطور", "") & filters.create(is_sudoer))
async def remove_dev(client, message):
    username = message.text.split()[2]
    if username in SUDOERS:
        SUDOERS.remove(username)
        await message.reply_text("تمت إزالة المطور بنجاح.")
    else:
        await message.reply_text("المطور غير موجود في القائمة.")

f = filters.command("رفع ادمن", "")
@Client.on_message(f & filters.create(is_sudoer))
async def new_and_edited(client, message):
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    await client.promote_chat_member(chat_id, user_id, ChatPrivileges(
    can_manage_chat = True,
    can_delete_messages = True,
    can_manage_video_chats = True,
    can_restrict_members = True,
    can_promote_members = True,
    can_change_info = True,
    can_post_messages = False,
    can_edit_messages = False,
    can_invite_users = True,
    can_pin_messages = True,
    is_anonymous = False
    ))
    await message.reply("تم رفع العضو ادمن بنجاح")



f = filters.create(lambda _, __, message: "رفع مشرف" in message.text)

@Client.on_message(f & filters.channel & filters.create(is_sudoer))
async def promote_by_id(client, message):
    chat_id = message.chat.id
    text = message.text.split()
    
    if len(text) == 3 and text[0] == "رفع" and text[1] == "مشرف":
        try:
            user_id = str(text[2])
            await client.promote_chat_member(
                chat_id,
                user_id,
                ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_promote_members=False,
                    can_change_info=False,
                    can_post_messages=True,
                    can_edit_messages=True,
                    can_invite_users=True,
                    can_pin_messages=False,
                    is_anonymous=False
                )
            )
            await message.reply("تم رفع العضو ادمون بنجاح")
        except ValueError:
            await message.reply("اكتب الايدي عدل يعلق")



f = filters.create(lambda _, __, message: "رفع مشرف" in message.text)

@Client.on_message(f & filters.group & filters.create(is_sudoer))
async def promote_by_id(client, message):
    chat_id = message.chat.id
    text = message.text.split()
    
    if len(text) == 3 and text[0] == "رفع" and text[1] == "مشرف":
        try:
            user_id = str(text[2])
            await client.promote_chat_member(
                chat_id,
                user_id,
                ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_promote_members=True,
                    can_change_info=True,
                    can_post_messages=False,
                    can_edit_messages=False,
                    can_invite_users=True,
                    can_pin_messages=True,
                    is_anonymous=False
                )
            )
            await message.reply("تم رفع العضو ادمون بنجاح")
        except ValueError:
            await message.reply("اكتب الايدي عدل يعلق")














@Client.on_message(filters.text & ~filters.create(is_sudoer))
async def delete_mention(client, message):
    locked_commands = ["قفل الردود", "قفل المنشن", "قفل الفيديو", "قفل الدردشة", "قفل الصور", "قفل الملصقات", "قفل التوجيه", "فتح الردود", "فتح المنشن", "فتح الفيديو", "فتح الدردشة", "فتح الصور", "فتح الملصقات", "فتح التوجيه"]
    for command in locked_commands:
        if command in message.text:
            await message.reply_text("يجب أن تكون مطورًا لاستخدام هذا الأمر.")
            break






@Client.on_message(filters.regex("قفل المنشن") & filters.create(is_sudoer))
async def lock_mention(client, message):
    global mention_locked
    mention_locked = True
    await message.reply_text("تم قفل المنشن.")
    await delete_message(client, message)


@Client.on_message(filters.regex("فتح المنشن") & filters.create(is_sudoer))
async def unlock_mention(client, message):
    global mention_locked
    mention_locked = False
    await message.reply_text("تم فتح المنشن.")
    await delete_message(client, message)


@Client.on_message(filters.text & ~filters.create(is_sudoer) & filters.create(lambda _, __, message: mention_locked))
async def delete_mention(client, message):
    if "@" in message.text:
        await message.delete()


@Client.on_message(filters.regex("قفل الفيديو") & filters.create(is_sudoer))
async def lock_video(client, message):
    global video_locked
    video_locked = True
    await message.reply_text("تم قفل الفيديو.")


@Client.on_message(filters.regex("فتح الفيديو") & filters.create(is_sudoer))
async def unlock_video(client, message):
    global video_locked
    video_locked = False
    await message.reply_text("تم فتح الفيديو.")


@Client.on_message(filters.video & ~filters.create(is_sudoer) & filters.create(lambda _, __, message: video_locked))
async def delete_video(client, message):
    await message.delete()


@Client.on_message(filters.regex("قفل الروابط") & filters.create(is_sudoer))
async def lock_links(client, message):
    global link_locked
    link_locked = True
    await message.reply_text("تم قفل الروابط.")


@Client.on_message(filters.regex("فتح الروابط") & filters.create(is_sudoer))
async def unlock_links(client, message):
    global link_locked
    link_locked = False
    await message.reply_text("تم فتح الروابط.")


@Client.on_message(filters.text & ~filters.create(is_sudoer) & filters.create(lambda _, __, message: link_locked))
async def delete_links(client, message):
    if any(entity.type == "text_link" for entity in message.entities):
        await message.delete()


@Client.on_message(filters.regex("قفل التوجيه") & filters.create(is_sudoer))
async def lock_forward(client, message):
    global forward_locked
    forward_locked = True
    await message.reply_text("تم قفل التوجيه.")


@Client.on_message(filters.regex("فتح التوجيه") & filters.create(is_sudoer))
async def unlock_forward(client, message):
    global forward_locked
    forward_locked = False
    await message.reply_text("تم فتح التوجيه.")


@Client.on_message(filters.forwarded & filters.create(lambda _, __, message: forward_locked))
async def delete_forwarded_messages(client, message):
    await message.delete()


@Client.on_message(filters.regex("قفل الملصقات") & filters.create(is_sudoer))
async def lock_stickers(client, message):
    global sticker_locked
    sticker_locked = True
    await message.reply_text("تم قفل الملصقات.")


@Client.on_message(filters.regex("فتح الملصقات") & filters.create(is_sudoer))
async def unlock_stickers(client, message):
    global sticker_locked
    sticker_locked = False
    await message.reply_text("تم فتح الملصقات.")


@Client.on_message(filters.sticker & ~filters.create(is_sudoer) & filters.create(lambda _, __, message: sticker_locked))
async def delete_sticker(client, message):
    await message.delete()


@Client.on_message(filters.regex("قفل الردود") & filters.create(is_sudoer))
async def lock_replies(client, message):
    global reply_locked
    reply_locked = True
    await message.reply_text("تم قفل الردود.")


@Client.on_message(filters.regex("فتح الردود") & filters.create(is_sudoer))
async def unlock_replies(client, message):
    global reply_locked
    reply_locked = False
    await message.reply_text("تم فتح الردود.")


@Client.on_message(filters.reply & ~filters.create(is_sudoer) & filters.create(lambda _, __, message: reply_locked))
async def delete_reply(client, message):
    await message.delete()


@Client.on_message(filters.regex("قفل الصور") & filters.create(is_sudoer))
async def lock_photos(client, message):
    global photo_locked
    photo_locked = True
    await message.reply_text("تم قفل الصور.")


@Client.on_message(filters.regex("فتح الصور") & filters.create(is_sudoer))
async def unlock_photos(client, message):
    global photo_locked
    photo_locked = False
    await message.reply_text("تم فتح الصور.")


@Client.on_message(filters.photo & ~filters.create(is_sudoer) & filters.create(lambda _, __, message: photo_locked))
async def delete_photo(client, message):
    await message.delete()


@Client.on_message(filters.regex("قفل الدردشة") & filters.create(is_sudoer))
async def lock_chat(client, message):
    global chat_locked
    chat_locked = True
    await message.reply_text("تم قفل الدردشة.")


@Client.on_message(filters.regex("فتح الدردشة") & filters.create(is_sudoer))
async def unlock_chat(client, message):
    global chat_locked
    chat_locked = False
    await message.reply_text("تم فتح الدردشة.")


@Client.on_message()
async def delete_message(client, message):
    global chat_locked
    if chat_locked and not (is_sudoer(client, None, message) or is_owner(client, None, message)):
        await message.delete()
