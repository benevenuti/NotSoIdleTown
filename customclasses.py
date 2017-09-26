"""Keep needed classes for bot chat"""


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
