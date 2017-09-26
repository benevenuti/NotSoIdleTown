# coding=utf-8
import time
import random
import re

from telethon import TelegramClient
from telethon.tl.types import UpdateShortChatMessage, UpdateShortMessage, Updates, UpdateNewMessage
#from pprint import pprint

from apiconfig import *

from botcommands import Comms

from classes import Building

LAST_COMM = Comms.MENU.value
NEXT_COMM = Comms.MENU.value

# botname
BOT_NAME = '@IdleTownBot'

CLIENT = TelegramClient('session_name', API_ID, API_HASH)

CLIENT.connect()

if not CLIENT.is_user_authorized():
    # CLIENT.sign_in(phone=phone)
    #CLIENT.sign_in(code=input('Digite o código: '))

    CLIENT.send_code_request(PHONE)
    CLIENT.sign_in(PHONE, input('Digite o código: '))

doAttack = False
doSearchOpponent = True

level = 0
myLvl = 0
qtdRecursoAlvo = 120
nivelAlvo = 38

# Prices

def valor(recurso, msg):
    """Faz o parse do valor de cada item do usuário a ser atacado"""
    m = re.search(recurso + ': ([0-9]*\.[0-9]*) ([K|M])', msg)    
    valor = 0.0
    if m != None:
        valor = float(m.group(1))
        if m.group(2) == 'M':
            valor = valor * 1000

    return valor


def sprint(string):
    """Safe Print (handle UnicodeEncodeErrors on some terminals)"""
    try:
        print(string)
    except UnicodeEncodeError:
        string = string.encode('utf-8', errors='ignore')\
                       .decode('ascii', errors='ignore')
        print(string)

# DETECÇÃO DE RECURSOS
def detect_resource(res_name, msg):
    """Detecta o recurso parametrizado"""
    m = re.findall(res_name + ":\ ([0-9.]+)\ *([KM]*)", msg)
    myResource = float(m[0][0])
    myProduction = float(m[1][0])
    if m[0][1] == 'K':
        myResource = myResource * 1000
    if m[1][1] == 'K':
        myProduction = myProduction * 1000
    sprint("Armazém - " + res_name +
           " {} - Produção {}".format(myResource, myProduction))
    return [myResource, myProduction]




def update_handler(update_object):
    """Motor de detecção de atividade"""
    global doAttack
    global doSearchOpponent
    global myLvl
    global LAST_COMM
    global NEXT_COMM
    global nivelAlvo

    global myWood
    global myGold
    global myFood
    
    if isinstance(update_object, UpdateShortMessage):
        if update_object.out:
            sprint('You sent {} to user #{}'.format(
                update_object.message, update_object.user_id))
        else:
            sprint('[User #{} sent {}]'.format(
                update_object.user_id, update_object.message))
    elif isinstance(update_object, UpdateShortChatMessage):
        if update_object.out:
            sprint('You sent {} to chat #{}'.format(
                update_object.message, update_object.chat_id))
        else:
            sprint('[Chat #{}, user #{} sent {}]'.format(
                   update_object.chat_id, update_object.from_id,
                   update_object.message))
    elif isinstance(update_object, Updates):
        if len(update_object.updates) > 0:
            if isinstance(update_object.updates[0], UpdateNewMessage):
                _from = update_object.updates[0].message.from_id
                _msg = update_object.updates[0].message.message
                sprint('User {} sent \n{}'.format(_from, _msg))
                # BATALHA
                if LAST_COMM == Comms.BATTLE.value:
                    m = re.search('\(Lvl ([0-9]*)\)', _msg)
                    if m != None:
                        if _msg.find("Inimigo Encontrado") > -1 and int(m.group(1)) < nivelAlvo:
                            if valor("Comida", _msg) > qtdRecursoAlvo or \
                                    valor("Madeira", _msg) > qtdRecursoAlvo or \
                                    valor("Ouro", _msg) > qtdRecursoAlvo:
                                if valor("Ouro", _msg) == valor("Madeira", _msg) or \
                                        valor("Madeira", _msg) == valor("Comida", _msg) or \
                                        valor("Ouro", _msg) == valor("Comida", _msg):
                                    doAttack = True

                    doSearchOpponent = True

                # MENU PRINCIPAL - level - armazem - producao
                elif LAST_COMM == Comms.MENU.value:
                    # level
                    m = re.search('\(Lvl ([0-9]*)\)', _msg)
                    myLvl = int(m.group(1))
                    nivelAlvo = myLvl + 2
                    sprint('My LEVEL = {}'.format(myLvl))
                    # armazém - produção                    
                    myWood = detect_resource("Madeira", _msg)
                    myGold = detect_resource("Ouro", _msg)
                    myFood = detect_resource("Comida", _msg)

                    NEXT_COMM = Comms.BUILD.value

                elif LAST_COMM == Comms.BUILD.value:
                    print("TO DO")

                    NEXT_COMM = ''                    


CLIENT.add_update_handler(update_handler)


# MAIN LOOP
while True:
    WAIT_TIME = random.randrange(1,10,1)
    time.sleep(WAIT_TIME)

    if NEXT_COMM != '':
        LAST_COMM = NEXT_COMM
        #print("Vai enviar {} para {}".format(NEXT_COMM, BOT_NAME))
        CLIENT.send_message(BOT_NAME, NEXT_COMM)
    else:
        print("Esperando a grama crescer - SEM COMANDO DEFINIDO")
        

    """
    if doAttack:
        doAttack=False
        tempoAttack=random.randrange(601, 620, 1) # tempo aleatório para o próximo ataque
        print("Enviando comando")
        CLIENT.send_message('@IdleTownBot', 'Atacar ⚔')
        
    if tempoAttack <= 0 and doSearchOpponent:
        if random.randrange(1, 7, 1) % 3 == 0: # simula se pesquisa um novo oponente ou aguarda mais um pouco
            doSearchOpponent=False
            CLIENT.send_message('@IdleTownBot', 'Jogador Aleatório')
    elif tempoAttack > 0:  # aguardando a próxima luta, decrementa o contador
        if tempoAttack % 30 == 0:
            print("Aguardando a próxima luta ...")
        tempoAttack=tempoAttack-1
    """
