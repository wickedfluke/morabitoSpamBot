#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
API_ID = 25165796#api id
API_HASH = "6fd1434e34ab932d2d94ccae2f856394"#api hash
groups = []
spamEnabled = False
Time = 1
Message = None

client = TelegramClient('opentelegramfiles',API_ID,API_HASH)
async def doSpam(client, msg):
    try:
        for group in groups:
            try:
                await client.send_message(group, msg[0], file=msg[1], link_preview=msg[2])
                await asyncio.sleep(0.2)
            except:
                pass
    except:
        pass
@client.on(events.NewMessage( outgoing=True))
async def miei_msg(event):
    global groups, Message, spamEnabled, Time
    if event.text == ".start":
        if not spamEnabled:
            await event.edit("spam avviato!")
            spamEnabled = True
            if Message != None:
                while spamEnabled:
                    await asyncio.wait([asyncio.create_task(doSpam(event.client, Message))])
                    for i in range(Time * 60):
                        if spamEnabled:
                            await asyncio.sleep(1)
                        else:
                            break

    elif event.text == ".stop":
        await event.edit("spam stoppato!")
        spamEnabled = False
    elif event.text == ".addgroup":
        if isinstance(event.peer_id, PeerUser):
            await event.edit("stai parlando con un utente! non è un gruppo!")
        else:
            if isinstance(event.peer_id, PeerChat):
                groups.append(event.peer_id.chat_id)
                await event.edit("gruppo aggiunto per lo spam correttamente!")
            elif isinstance(event.peer_id, PeerChannel):
                groups.append(event.peer_id.channel_id)
                await event.edit("gruppo aggiunto per lo spam correttamente!")
            else:
                event.edit("errore nell'aggiunta.(controllare il log.)")
    elif event.text == ".addchannelforspam":
        if isinstance(event.peer_id, PeerChannel):
            groups.append(event.peer_id.channel_id)
            await event.edit("canale aggiunto per lo spam correttamente!")
    elif event.text == ".remove_this_forspam":
        await event.edit("!rimosso per lo spam correttamente!")
    elif event.text == ".mex":
        if event.is_reply:
            new = await event.get_reply_message()
            if new.media != None and type(new.media).__name__ != "MessageMediaWebPage" and type(
                    new.media).__name__ != "MessageMediaUnsupported":
                media = new.media
            else:
                media = None
            if new.web_preview != None:
                lp = True
            else:
                lp = False
            Message = [new.text, media, lp]
            await event.edit("messaggio fissato per lo spam")
        else:
            await event.edit("!nessun messaggio fissato per lo spam!\n(rispondi ad un messaggio per usare questo comando!)")
    elif event.text == ".time":
        if event.is_reply:
            new = await event.get_reply_message()
            if int(new.text) in range(1, 60):
                Time = int(new.text)
                await event.edit("tempo VALIDO selezionato!")
            else:
                await event.edit("tempo non VALIDO(rimane il precedente impostato):\ndefault- 15 minuti")

client.start()
client.run_until_disconnected()
