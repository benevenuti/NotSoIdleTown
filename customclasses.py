"""Keep needed classes for bot chat"""

import re


def building_parser(msg):
    """Parses a string message sent from Bot when asked for buildings"""
    # Cleaning
    msg = msg.replace('➖➖➖➖➖➖', '').split('\n\n')
    del msg[0]
    del msg[0]

    # Reference
    grp_l = [('🏯', 0, '/up_w'), ('🏹', 1, '/up_t'), ('📦', 2, '/up_st'),
             ('🌳', 3, '/up_lm'), ('💰', 4, '/up_gm'), ('🌾', 5, '/up_fa')]

    # Processing
    building_list = []
    for idx, obj in enumerate(msg):
        regex = "(?smx)" + "([" + grp_l[idx][0] + \
            r"]{1})(.+?)\ \(Lvl\ ([0-9]+)\).+:\ ([0-9.]+)\ (K|M)🌳\ *(" + \
            grp_l[idx][2] + ")"

        match = re.findall(regex, obj)

        price = float(match[0][3])
        if match[0][4] == 'K':
            price = price * 1000

        if match[0][4] == 'M':
            price = price * 1000 * 1000

        # print(price)
        build = Building(match[0][0], match[0][1], idx,
                         match[0][2], price, match[0][5])
        building_list.append(build)
    return building_list


class Building():
    """Keep track os buildings"""

    def __init__(self, icon, name, list_position, current_level, upgrade_price, upgrade_command):
        self._icon = icon
        self._name = name
        self._list_position = list_position
        self._current_level = current_level
        self._upgrade_price = upgrade_price
        self._upgrade_command = upgrade_command

    def get_icon(self):
        """Returns utf-8 icon char"""
        return self._icon

    def get_name(self):
        """Returns building name"""
        return self._name

    def get_listposition(self):
        """Returns position of the build in the building list"""
        return self._list_position

    def set_current_level(self, current_level):
        """Sets new current level for the building"""
        self._current_level = current_level
        return

    def get_current_level(self):
        """Returns current level of the building"""
        return self._current_level

    def set_upgrade_price(self, upgrade_price):
        """Sets new upgrade priice to upgrade the building"""
        self._upgrade_price = upgrade_price

    def get_upgrade_price(self):
        """Returns current price to upgrade the building to the next level"""
        return self._upgrade_price

    def get_upgrade_command(self):
        """Returns the upgrade command to send to the bot"""
        return self._upgrade_command
