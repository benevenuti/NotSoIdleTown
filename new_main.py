import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from telethon import events
from telethon.client import TelegramClient

from config import api_id, api_hash

with TelegramClient('session_name', api_id, api_hash) as client:
    def show_img(s):
        img = mpimg.imread(s)
        imgplot = plt.imshow(img)
        plt.show()


    @client.on(events.NewMessage())
    async def handler(event):
        print(event.message.text)
        o = (await client.download_profile_photo('me'))
        show_img(o)
        await event.reply('Hey!')


    @client.on(events.MessageRead())
    async def conn(event):
        await client.send_message('me', 'Hello, myself!')


    client.run_until_disconnected()
