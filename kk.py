import os
import threading
import asyncio
from time import sleep
from balebot.handlers import *
from balebot.filters import *
from balebot.models.base_models import Peer
from balebot.models.messages import *
from balebot.updater import Updater
from balebot.config import Config
messageFile="ali.wav"
global_peer=list()
global_bot=None
scannerFlag=False
# A token you give from BotFather when you create your bot set below
updater = Updater(token="c7b956ff530a304140f4089825b45c2366a84fe6")
bot = updater.bot

dispatcher = updater.dispatcher

#print(os.path.getsize(messageFile))
def sendToAll(message):
    global global_bot, global_peer
    mes = TextMessage(message)
    print("FOR")
    for peer in global_peer:
        print("sending")
        try:

            bot.send_message(mes, peer, success_callback=success, failure_callback=failure)


        except:
            print("peer ERROR---------------------")

def send_voice():
    global global_bot, global_peer

    def file_upload_success(result, user_data):

        print("upload was successful : ", result)
        print(user_data)

        file_id = str(user_data.get("file_id", None))
        access_hash = str(user_data.get("user_id", None))

        print("Sending the uploaded file")
        duc=DocumentMessage(file_id=file_id, access_hash=access_hash, name="message.mp3", file_size=os.path.getsize(messageFile),
                                 mime_type="audio/mp3", caption_text=TextMessage(text="New message"))
        for user_peer in global_peer:
            bot.send_message(duc, user_peer, success_callback=success, failure_callback=failure)
            print("File sent")

    bot.upload_file(file=messageFile, file_type="file", success_callback=file_upload_success,
                    failure_callback=failure)
def success(response, user_data):
    print("success : ", response)


def failure(response, user_data):
    print("user_data : ", user_data)
    print("failure : ", response)
@dispatcher.default_handler()
def had(bot , update):
    print("jsdfjfsdjdf\njsdfjfsdjdf\njsdfjfsdjdf\njsdfjfsdjdf\njsdfjfsdjdf\njsdfjfsdjdf\njsdfjfsdjdf\njsdfjfsdjdf\njsdfjfsdjdf\njsdfjfsdjdf\njsdfjfsdjdf\njsdfjfsdjdf\n")
    user_peer = update.get_effective_user()
    mes = TextMessage("WRONG COMMAND")
    bot.send_message(mes, user_peer, success_callback=success, failure_callback=failure)
@dispatcher.command_handler("/check")
def check_command(bot , update):
    while (True):
        try:
            file = open("balecom.txt", 'r')
            com = file.read()
            file.close()
            if "mes" in com:
                file = open("balecom.txt", 'w')
                file.write("null")
                file.close()
                sendToAll("*you have a new message !*")
                print("sent\nsending voice")
                send_voice()
                print("Voice is sent")
                break


            elif "cancel" in com:
                sendToAll("*check mode canceled !*")
                break
        except:
            continue



@dispatcher.command_handler("/start")
def start_command(bot, update):
    global global_bot , global_peer
    global_bot=bot
    user_peer = update.get_effective_user()
    mes=TextMessage("*Hi nice to meet you*\nplease give me your password to continue.")
    bot.send_message(mes, user_peer, success_callback=success, failure_callback=failure)


@dispatcher.message_handler(filters=[TextFilter(keywords="I987")])
def login_command(bot, update):
    print ("REC")
    global global_bot, global_peer
    user_peer = update.get_effective_user()
    mes = TextMessage("*You are loged in*")
    global_peer.append(user_peer)
    bot.send_message(mes, user_peer, success_callback=success, failure_callback=failure)
@dispatcher.message_handler(filters=[TextFilter(keywords="O987")])
def logout_command(bot, update):
    print ("REC")
    global global_bot, global_peer
    user_peer = update.get_effective_user()
    i=-1
    for p in global_peer:
        i+=1
        if p.peer_id==user_peer.peer_id:
            del global_peer[i]
            mes = TextMessage("*You are loged out*")


    bot.send_message(mes, user_peer, success_callback=success, failure_callback=failure)
    #sendToAll("*Hello*")



updater.run()
