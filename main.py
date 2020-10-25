from telethon import TelegramClient, events
import re
import time
import units
import sys
import random
import _thread
import config
import datetime

from collections import OrderedDict

from decimal import Decimal, getcontext

getcontext().prec = 256

api_id = config.api_id
api_hash = config.api_hash

IDLE_TOWN_ID = 271141703

client = TelegramClient('session_name', api_id, api_hash,
                        update_workers=2, spawn_read_thread=False)
client.start()

client.updates.workers = 2

city = {}
build = {}
equip = {}

MENU = -1

oper_count = 0

build_count = 0
equip_count = 0


def myPrint(*args):
    print(getDate(), *args)


def getDate():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('[%Y-%m-%d %H:%M:%S] ')
    return st


def re_init(a, b):
    global MENU
    while 1:
        t = random.randrange(120, 180)
        time.sleep(t)
        MENU = 0
        myPrint('== Acordando depois de dormir por ' + str(t) + ' segundos...')
        send_town('Menu 📜')


try:
    _thread.start_new_thread(re_init, (0, 0))
except Exception as e:
    myPrint("!! Não possível iniciar a thread : " + str(e))


def get_city(m):
    s = re.search(
        '(?s)Cidade (.*?) .*?\(Lvl ([0-9]*)\).*?Arena Rank: ([0-9]+).*?Energia: ([0-9]+)/100.*?Stamina: ([0-9]+)/5.*?Madeira: ([0-9.]+) ([A-Z]*)/hora.*?Ouro: ([0-9.]+) ([A-Z]*)/hora', m)
    l = ['name', 'lvl', 'rank', 'energy', 'stamina',
         'wood_cst', 'wood_mlt', 'gold_cst', 'gold_mlt']
    r = {}
    for i, g in enumerate(l):
        r[g] = s.group(i + 1)
        if not (g in ['name']):
            try:
                r[g] = int(r[g])
            except ValueError:
                pass
    return r


def send_town(msg):
    try:
        myPrint('>> ' + msg)
        time.sleep(random.randrange(15, 20) / 10)
        client.send_message('@IdleTownBot', msg)
    except Exception as e:
        myPrint('!! Não foi possível enviar a mensagem ' + msg + ' : ' + str(e))


def get_build(obj, m):
    s = re.search(
        '(?s)' + obj + ' \(Lvl ([0-9]+?)\).*?Custo: ([0-9.]+) ([A-Z]*).([a-z_/]+)', m)
    lvl = s.group(1)
    cst = s.group(2)
    mlt = s.group(3)
    cmd = s.group(4)
    return {'obj': obj, 'lvl': int(lvl), 'cst': int(Decimal(units.u[mlt]) / Decimal(100) * int(float(cst) * 100)), 'cst_s': cst + ' ' + mlt, 'cmd': cmd}


def get_equip(obj, m):
    s = re.search(
        '(?s)' + obj + ' \(Lvl ([0-9]+?)\).*?Custo: ([0-9.]+) ([A-Z]*).[ ]*([a-z_/]+)', m)
    lvl = s.group(1)
    cst = s.group(2)
    mlt = s.group(3)
    cmd = s.group(4)
    return {'obj': obj, 'lvl': int(lvl), 'cst': int(Decimal(units.u[mlt]) / Decimal(100) * int(float(cst) * 100)), 'cst_s': cst + ' ' + mlt, 'cmd': cmd}


def get_wood(m):
    s = re.search('(?s)Você tem \(([0-9.]+) ([A-Z]*)🌳\) de Madeira', m)
    v = s.group(1)
    t = s.group(2)
    return {'cst': int(Decimal(units.u[t]) / Decimal(100) * int(float(v) * 100)), 'cst_s': v + ' ' + t}


def get_gold(m):
    s = re.search('(?s)Você tem \(([0-9.]+) ([A-Z]*)💰\) de Ouro', m)
    v = s.group(1)
    t = s.group(2)
    return {'cst': int(Decimal(units.u[t]) / Decimal(100) * int(float(v) * 100)), 'cst_s': v + ' ' + t}


def get_enemy(m):
    s = re.search(
        '(?s)Oponente:\n(.*?) \(Lvl ([0-9]+?)\)\nArena Rank: ([0-9]+?)\nID: (.+)\nClã: (.+)$', m)
    name = s.group(1)
    lvl = s.group(2)
    rank = s.group(3)
    ID = s.group(4)
    clan = s.group(5)
    return {'name': name, 'lvl': int(lvl), 'rank': int(rank), 'ID': ID, 'clan': clan}


@client.on(events.NewMessage(incoming=True))
def my_event_handler(event):

    global city
    global build
    global equip
    global build_count
    global equip_count

    global MENU

    global IDLE_TOWN_ID

    from_id = -1

    try:
        from_id = event.message.from_id
    except:
        myPrint("!! ============================================================================ !!")
        myPrint("!! Erro ao identificar o from _id: ", sys.exc_info()[0])
        myPrint("!! ============================================================================ !!")

    try:
        if IDLE_TOWN_ID == from_id:
            msg = event.message.message
            if 'Você está enviando muitas mensagens por segundo' in msg:
                send_town('Menu 📜')

            ###
            # =============================================================================================================================
            # MENU 0 ======================================================================================================================
            # =============================================================================================================================
            ###
            elif MENU <= 0:
                city = get_city(msg)
                myPrint(city)
                if (city['name'] == ''):
                    MENU = 0
                    send_town('Menu 📜')
                else:
                    MENU = 1
                    send_town('Construções 🏢')
            ###
            # =============================================================================================================================
            # MENU 1 ======================================================================================================================
            # =============================================================================================================================
            ###
            elif MENU == 1:
                if 'melhorado com Sucesso' in msg:
                    build_count += 1

                    if build_count >= 4:
                        MENU = 2
                        build_count = 0
                        send_town('Menu 📜')
                    else:
                        send_town('Atualizar')
                else:
                    for i in ['Arsenal', 'Ferreiro', 'Serraria', 'Mina de Ouro']:
                        build[i] = get_build(i, msg)

                    wood = get_wood(msg)
                    build = OrderedDict(
                        sorted(build.items(), key=lambda x: x[1]['lvl']))
                    up_obj = next(iter(build.items()))[1]
                    cost = up_obj['cst']

                    if wood['cst'] >= cost:
                        cmd = up_obj['cmd']
                        myPrint('== Melhorando : ' + up_obj['obj'] + ' ' +
                                up_obj['cst_s'] + ' para Lvl ' + str(up_obj['lvl'] + 1))
                        send_town(cmd)
                    else:
                        myPrint('== Pouca madeira: ' +
                                up_obj['obj'] + ' ^^ ' + up_obj['cst_s'] + ' > ' + wood['cst_s'])
                        # myPrint('Cash: ' + str(wood['cst']))
                        # myPrint('Cost: ' + str(cost))
                        MENU = 2
                        send_town('Menu 📜')
            ###
            # =============================================================================================================================
            # MENU 2 ======================================================================================================================
            # =============================================================================================================================
            ###
            elif MENU == 2:
                if 'Cidade ' + city['name'] in msg:
                    send_town('Herói 💂')
                elif 'Status do Herói' in msg:
                    send_town('Equipamento')
                elif 'melhorado com Sucesso' in msg:
                    equip_count += 1

                    if equip_count >= 4:
                        MENU = 3
                        equip_count = 0
                        send_town('Menu 📜')
                    else:
                        send_town('Atualizar')
                elif 'Equipamentos' in msg:
                    for i in ['Espada', 'Escudo', 'Capacete', 'Luvas', 'Botas']:
                        equip[i] = get_equip(i, msg)

                    gold = get_gold(msg)
                    equip = OrderedDict(
                        sorted(equip.items(), key=lambda x: x[1]['lvl']))
                    up_obj = next(iter(equip.items()))[1]
                    cost = up_obj['cst']

                    if gold['cst'] >= cost:
                        cmd = up_obj['cmd']
                        myPrint('== Melhorando : ' + up_obj['obj'] + ' ' +
                                up_obj['cst_s'] + ' para Lvl ' + str(up_obj['lvl'] + 1))
                        send_town(cmd)
                    else:
                        myPrint(
                            '== Pouco ouro: ' + up_obj['obj'] + ' ^^ ' + up_obj['cst_s'] + ' > ' + gold['cst_s'])
                        MENU = 3
                        # myPrint('Cash: ' + str(gold['cst']))
                        # myPrint('Cost: ' + str(cost))
                        send_town('Menu 📜')
                else:
                    myPrint(
                        "II ============================================================================ II")
                    myPrint('II Mensagem não mapeada no menu ' + str(MENU) + ': ')
                    myPrint(msg)
                    myPrint(
                        "II ============================================================================ II")
            ###
            # =============================================================================================================================
            # MENU 3 ======================================================================================================================
            # =============================================================================================================================
            ###
            elif MENU == 3:
                # myPrint(msg)
                if 'Cidade ' + city['name'] in msg:
                    send_town('Batalhar ⚔')
                elif 'Batalhas\n/arena' in msg:
                    if city['energy'] >= 10:
                        send_town('/bosses')
                    else:
                        MENU = 4
                        myPrint('vv Pouca energia (' +
                                str(city['energy']) + '), não vou enfrentar chefão')
                        send_town('Menu 📜')
                elif 'Chefões' in msg:
                    MENU = 3
                    send_town('Atacar Max')
                elif 'Você matou o chefão' in msg:
                    myPrint('== Chefão morto :D , indo gastar seu ouro ')
                    MENU = 2
                    send_town('Menu 📜')
                elif 'Atacado' in msg:
                    myPrint('== Chefão sobreviveu, indo para confrontos ')
                    MENU = 4
                    send_town('Menu 📜')
                else:
                    myPrint(
                        "II ============================================================================ II")
                    myPrint('II Mensagem não mapeada no menu ' + str(MENU) + ': ')
                    myPrint(msg)
                    myPrint(
                        "II ============================================================================ II")
            ###
            # =============================================================================================================================
            # MENU 4 ======================================================================================================================
            # =============================================================================================================================
            ###
            elif MENU == 4:
                # myPrint(msg)
                if 'Cidade ' + city['name'] in msg:
                    send_town('Batalhar ⚔')
                elif 'Batalhas\n/arena' in msg:
                    if city['stamina'] > 0:
                        send_town('/arena')
                    else:
                        MENU = 0
                        myPrint('vv Pouca stamina (' +
                                str(city['stamina']) + '), não vou entrar na arena')
                        myPrint('== HALT')
                elif msg.startswith('Arena\n'):
                    c = random.choice(['/rMatch', '/nMatch'])
                    send_town(c)
                elif msg.startswith('Ataque Ranqueado'):
                    enemy = get_enemy(msg)
                    if enemy['lvl'] <= city['lvl'] + 1:
                        myPrint('^^ Atacando ' +
                                enemy['name'] + ' Lvl ' + str(enemy['lvl']))
                        #MENU = 4
                        send_town('Atacar ⚔')
                    else:
                        myPrint('vv Evitando o confronto com ' +
                                enemy['name'] + ' Lvl ' + str(enemy['lvl']))
                        # myPrint(event.stringify())
                        send_town('/rMatch')
                elif msg.startswith('Ataque Normal'):
                    enemy = get_enemy(msg)
                    if enemy['lvl'] <= city['lvl'] + 1:
                        myPrint('^^ Atacando ' +
                                enemy['name'] + ' Lvl ' + str(enemy['lvl']))
                        #MENU = 4
                        send_town('Atacar ⚔')
                    else:
                        myPrint('vv Evitando o confronto com ' +
                                enemy['name'] + ' Lvl ' + str(enemy['lvl']))
                        send_town('/nMatch')

                elif 'DERROTA' in msg:
                    myPrint('== Derrota :( :(')
                    #MENU = 4
                    send_town('Menu 📜')
                elif 'VITÓRIA' in msg:
                    myPrint('== Vitória :) :) ')
                    #MENU = 4
                    send_town('Menu 📜')
                elif 'Sem pontos de Stamina suficientes' in msg:
                    MENU = 0
                    myPrint('vv Sem pontos de Stamina suficientes')
                    myPrint('== HALT')
                else:
                    myPrint(
                        "II ============================================================================ II")
                    myPrint('II Mensagem não mapeada no menu ' + str(MENU) + ': ')
                    myPrint(msg)
                    myPrint(
                        "II ============================================================================ II")

        else:
            myPrint('!! Mensagem de outra origem : ' + str(from_id))
            myPrint(event.stringify())
    except:
        myPrint("!! ============================================================================ !!")
        myPrint("!! Erro genérico em my_event_handler ", sys.exc_info()[0].str())
        myPrint("!! ============================================================================ !!")
        myPrint(event.message.stringify())


send_town('Menu 📜')

client.idle()
