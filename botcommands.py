
from enum import Enum

# main COMMS in IdleTownBot
class Comms(Enum):
    """Definições de comandos"""
    encode = 'utf-8'
    """Menus"""
    MENU = 'Menu 📜'
    BACK = 'Voltar 🔙'

    """Contruções"""
    BUILD = 'Construções 🏢'
    BUILD_UP_WOOD = '/up_w'

    """Quartel"""
    HDQ = 'Quartel 💂'
    HDQ_EQP = 'Equipamento 🆙'

    """Melhorias no Quartel"""
    HDQ_EQP_SW = '/up_tr_sw'
    HDQ_EQP_AR = '/up_tr_ar'
    HDQ_EQP_HE = '/up_tr_he'

    """Batalha"""
    BATTLE = 'Batalha ⚔️'
    BATTLE_RANDOM = '/random'
    BATTLE_ATTACK = 'Atacar ⚔'
