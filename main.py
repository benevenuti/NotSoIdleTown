from telethon import TelegramClient, events
from telethon.tl.types import UpdateShortChatMessage, UpdateShortMessage, Updates, UpdateNewMessage
import re
import time
import units
import sys
import random
import _thread

from decimal import Decimal
from collections import OrderedDict

api_id = 999999
api_hash = 'abcdef0123456789abcdef0123456789'
phone_number = '+55 54 9 9999 9999'

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


def re_init(a, b):
    global MENU
    while 1:
        t = random.randrange(120, 180)
        time.sleep(t)
        MENU = 0
        print('== Acordando depois de dormir por ' + str(t) + ' segundos...')
        send_town('Menu 📜')


try:
    _thread.start_new_thread(re_init, (0, 0))
except Exception as e:
    print("!! Não possível iniciar a thread : " + str(e))


def get_city(m):
    s = re.search(
        '(?s)Cidade (.*?) .*?\(Lvl ([0-9]*)\).*?Arena Rank: ([0-9]+).*?Energia: ([0-9]+)/100.*?Stamina: ([0-9]+)/5.*?Madeira: ([0-9.]+) ([A-Z]*)/hora.*?Ouro: ([0-9.]+) ([A-Z]*)/hora', m)
    l = ['name', 'lvl', 'rank', 'energy', 'stamina',
         'wood_cst', 'wood_mlt', 'gold_cst', 'gold_mlt']
    r = {}
    for i, g in enumerate(l):
        r[g] = s.group(i+1)
        if not (g in ['name']):
            try:
                r[g] = int(r[g])
            except ValueError:
                pass
    return r


def send_town(msg):
    try:
        print('>> ' + msg)
        time.sleep(random.randrange(1, 2))
        client.send_message('@IdleTownBot', msg)
    except Exception as e:
        print('!! Não foi possível enviar a mensagem ' + msg + ' : ' + str(e))


def get_build(obj, m):
    s = re.search(
        '(?s)' + obj + ' \(Lvl ([0-9]+?)\).*?Custo: ([0-9.]+) ([A-Z]*).([a-z_/]+)', m)
    lvl = s.group(1)
    cst = s.group(2)
    mlt = s.group(3)
    cmd = s.group(4)
    return {'obj': obj, 'lvl': int(lvl), 'cst': Decimal(cst) * Decimal(units.u[mlt]), 'cst_s': cst + ' ' + mlt, 'cmd': cmd}


def get_equip(obj, m):
    s = re.search(
        '(?s)' + obj + ' \(Lvl ([0-9]+?)\).*?Custo: ([0-9.]+) ([A-Z]*).[ ]*([a-z_/]+)', m)
    lvl = s.group(1)
    cst = s.group(2)
    mlt = s.group(3)
    cmd = s.group(4)
    return {'obj': obj, 'lvl': int(lvl), 'cst': Decimal(cst) * Decimal(units.u[mlt]), 'cst_s': cst + ' ' + mlt, 'cmd': cmd}


def get_wood(m):
    s = re.search('(?s)Você tem \(([0-9.]+) ([A-Z]*)🌳\) de Madeira', m)
    v = s.group(1)
    t = s.group(2)
    return {'cst': Decimal(float(v) * units.u[t]), 'cst_s': v + ' ' + t}


def get_gold(m):
    s = re.search('(?s)Você tem \(([0-9.]+) ([A-Z]*)💰\) de Ouro', m)
    v = s.group(1)
    t = s.group(2)
    return {'cst': Decimal(float(v) * units.u[t]), 'cst_s': v + ' ' + t}


def get_enemy(m):
    s = re.search(
        '(?s)Oponente:\n(.*?) \(Lvl ([0-9]+?)\)\nArena Rank: ([0-9]+?)\nID: (.+)\nClã: (.+)$', m)
    name = s.group(1)
    lvl = s.group(2)
    rank = s.group(3)
    ID = s.group(4)
    clan = s.group(5)
    return {'name': name, 'lvl': int(lvl), 'rank': int(rank), 'ID': ID, 'clan': clan}


@client.on(events.NewMessage())
def my_all_handler(event):
    global MENU
    global IDLE_TOWN_ID

    from_id = -1

    if MENU == 9:
        try:
            from_id = event.message.from_id
        except Exception as e:
            print('!! Erro ao identificar from_id: ' + str(e))
            return

        if IDLE_TOWN_ID == from_id:
            msg = event.message.message
            print(msg)


@client.on(events.NewMessage(incoming=True, chats=('Idle Town')))
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
    except Exception as e:
        print('!! Erro ao identificar from_id: ' + str(e))

    try:
        if IDLE_TOWN_ID == from_id:

            msg = event.message.message
            # print(event.stringify())

            if MENU <= 0:

                city = get_city(msg)

                print(city)

                if (city['name'] == ''):
                    send_town('Menu 📜')
                    MENU = 0
                else:
                    send_town('Construções 🏢')
                    MENU = 1
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

                    if wood['cst'].compare(cost) == Decimal('1'):
                        cmd = up_obj['cmd']
                        print('== Melhorando : ' + up_obj['obj'] + ' ' +
                              up_obj['cst_s'] + ' para Lvl ' + str(up_obj['lvl']+1))
                        send_town(cmd)
                    else:
                        print('== Pouca madeira: ' +
                              up_obj['obj'] + ' ^^ ' + up_obj['cst_s'] + ' > ' + wood['cst_s'])
                        MENU = 2
                        send_town('Menu 📜')

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

                    if gold['cst'].compare(cost) == Decimal('1'):
                        cmd = up_obj['cmd']
                        print('== Melhorando : ' + up_obj['obj'] + ' ' +
                              up_obj['cst_s'] + ' para Lvl ' + str(up_obj['lvl']+1))
                        send_town(cmd)
                    else:
                        print(
                            '== Pouco ouro: ' + up_obj['obj'] + ' ^^ ' + up_obj['cst_s'] + ' > ' + gold['cst_s'])
                        MENU = 3
                        send_town('Menu 📜')
            elif MENU == 3:
                # print(msg)
                if 'Cidade ' + city['name'] in msg:
                    send_town('Batalhar ⚔')
                elif 'Batalhas\n/arena' in msg:
                    if city['energy'] >= 90:
                        send_town('/bosses')
                    else:
                        MENU = 4
                        print('vv Pouca energia (' +
                              str(city['energy']) + '), não vou enfrentar chefão')
                        send_town('Batalhar ⚔')
                elif 'Chefões' in msg:
                    MENU = 9
                    send_town('Atacar Max')
                elif 'Você matou o chefão' in msg:
                    MENU = 4
                    send_town('Batalhar ⚔')

            elif MENU == 4:
                # print(msg)
                if 'Cidade ' + city['name'] in msg:
                    send_town('Batalhar ⚔')
                elif 'Batalhas\n/arena' in msg:
                    if city['stamina'] > 0:
                        send_town('/arena')
                    else:
                        MENU = 0
                        print('vv Pouca stamina (' +
                              str(city['energy']) + '), não vou entrar na arena')
                        print('== HALT')
                elif msg.startswith('Arena\n'):
                    c = random.choice(['/rMatch', '/nMatch'])
                    send_town(c)
                elif msg.startswith('Ataque Ranqueado'):
                    enemy = get_enemy(msg)
                    if enemy['lvl'] <= city['lvl']:
                        print('^^ Atacando ' +
                              enemy['name'] + ' Lvl ' + str(enemy['lvl']))
                        MENU = 9
                        send_town('Atacar ⚔')
                    else:
                        print('vv Evitando o confronto com ' +
                              enemy['name'] + ' Lvl ' + str(enemy['lvl']))
                        # print(event.stringify())
                        send_town('/rMatch')
                elif msg.startswith('Ataque Normal'):
                    enemy = get_enemy(msg)
                    if enemy['lvl'] <= city['lvl']:
                        print('^^ Atacando ' +
                              enemy['name'] + ' Lvl ' + str(enemy['lvl']))
                        MENU = 9
                        send_town('Atacar ⚔')
                    else:
                        print('vv Evitando o confronto com ' +
                              enemy['name'] + ' Lvl ' + str(enemy['lvl']))
                    # print(event.stringify())
                        send_town('/nMatch')
                elif ['DERROTA', 'VITÓRIA'] in msg:
                    print(msg)
                    MENU = 4
                else:
                    print(event.stringify())

        else:
            print('!! Mensagem de outra origem : ' + str(from_id))
            print(event.stringify())
    except Exception as e:
        print('!! ============================================================================ !!')
        print('!! Erro genérico no handler: ' + str(e))
        print('!! ============================================================================ !!')


send_town('Menu 📜')

client.idle()
