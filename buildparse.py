"""Testing parser unit"""
from customclasses import building_parser

MSG = "\
Construções\n\
Aqui você pode melhorar suas Construções e aumentar o Level delas usando Madeira🌳.\n\
➖➖➖➖➖➖\n\
Você tem (107.97 K🌳) Madeira.\n\
➖➖➖➖➖➖\n\
🏯Muros (Lvl 51)\n\
➕Poder de Defesa das Tropas.\n\
Atual: 622%🛡\n\
Melhorar: 645%🛡\n\
Preço: 162.55 K🌳/up_w\n\
\n\
🏹Torres (Lvl 50)\n\
➕Poder de Ataque das tropas.\n\
Atual: 600%🗡\n\
Melhorar: 622%🗡\n\
Preço: 149.74 K🌳/up_t\n\
\n\
📦Armazém (Lvl 57)\n\
➕Capacidade de Armazenamento.\n\
Atual: 585.42 K📦\n\
Melhorar: 633.08 K📦\n\
Preço: 541.43 K🌳/up_st\n\
\n\
🌳Serraria (Lvl 56)\n\
➕Produção de Madeira/hora.\n\
Atual: 72.73 K🌳\n\
Melhorar: 77.65 K🌳\n\
Preço: 148.58 K🌳 /up_lm\n\
\n\
💰Mina de Ouro (Lvl 62)\n\
➕Produção de Ouro/hora.\n\
Atual: 75.35 K💰\n\
Melhorar: 80.31 K💰\n\
Preço: 151.85 K🌳/up_gm\n\
\n\
🌾Fazenda (Lvl 69)\n\
➕Produção de Comida/hora.\n\
Atual: 209.13 K🌾\n\
Melhorar: 222.63 K🌾\n\
Preço: 223.35 K🌳/up_fa\n\
"

build_list = building_parser(MSG)
print(build_list)