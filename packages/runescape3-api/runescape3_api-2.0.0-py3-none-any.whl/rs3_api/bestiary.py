from .endpoints import BESTIARY_API_ENDPOINTS
from .utils.jagex import is_int, is_str
from .httpService.http_request import http_get

class Bestiary:
    #TODO Look into replacing "value" keys with Id and "label" with name

    """Bestiary Data"""
    def get_beast(self, id: int) -> dict:
        """Get specific statistics and information on a specific monsters
        :param id int: Id of the monster
        :raises TypeError: Invalid argument type
        :rtype: dict
        """
        is_int(id)
        response = http_get(BESTIARY_API_ENDPOINTS['get_beast'].format(id=id))

        return response.json()


    """Bestiary Search"""
    def get_beast_by_term(self, term: str) -> list:
        """Look up every occurence of a term in the bestiary
        :param str term: term to search for
        :rtype: list
        :raises TypeError: On Invalid argument type
        Multiple terms can be chained together with +, e.g cow+rabbit
        """
        is_str(term)

        response = http_get(BESTIARY_API_ENDPOINTS['beast_by_term'].format(term = term))
        return response.json()

    """Beastiary Names By First Letter"""
    def get_beast_by_first_letter(self, letter: str) -> list:
        """Look up every monster of which name starts with a certain Letter
        :param str letter: Letter in which to look up monsters after
        :raises TypeError: On invalid argument type
        :rtype: list
        """
        is_str(letter)
        letter = letter.upper()

        response = http_get(BESTIARY_API_ENDPOINTS['beast_by_first_letter'].format(letter = letter))
        return response.json()

    """Area Names"""
    def get_areas(self) -> list:
        """Get a list of all areas in the bestiary
        :rtype: list
        """
        response = http_get(BESTIARY_API_ENDPOINTS['get_areas'])
        return response.json()

    """Area Beasts"""
    def get_beasts_by_area(self, area: str) -> list:
        """Gets all beast in the searched areas
        :param str area: Area to search for beasts in
        :raises TypeError: On invalid argument type
        """
        is_str(area)
        area.replace(' ', '+')

        response = http_get(BESTIARY_API_ENDPOINTS['get_beasts_by_area'].format(area = area))
        return response.json()

    """Slayer Category Names"""
    def get_slayer_categories(self) -> dict:
        """Gets a dictionary of all slayer categories and their category Id's
        :rtype: dict
        """
        response = http_get(BESTIARY_API_ENDPOINTS['get_slayer_categories'])
        return response.json()

    """Slayer Beasts By Category"""
    def get_slayer_beasts_by_category_id(self, id: int) -> list:
        """Gets a list of all slayer beast by category_id

        :param int id: Category Id
        :raises TypeError: On invalid argument type
        """
        is_int(id)

        response = http_get(BESTIARY_API_ENDPOINTS['get_slayer_beasts_by_category_id'].format(id = id))
        return response.json()


    """Weakness Names"""
    def get_weakness_names(self):
        """Gets a dictionary of all weaknesses

        :rtype: dict
        """
        response = http_get(BESTIARY_API_ENDPOINTS['weakness_names'])
        return response.json()


    """Get Beasts By Weakness Id"""
    def get_beasts_by_weakness_id(self, id: int) -> list:
        """Get all beasts that have a certain weakness

        :param int id: Weakness Id
        :raises Exception: If id argument is not a positive integer
        :raises TypeError: On invalid argument type
        """
        is_int(id)
        if(id < 0):
            raise Exception("Id must be a positive integer")

        response = http_get(BESTIARY_API_ENDPOINTS['beasts_by_weakness_id'].format(id = id))
        return response.json()

    """Get Beast By Level Group"""
    def get_beasts_by_level_group(self, level_from: int, level_to: int) -> list:
        """Gets all beast between a certain level group
        :param int level_from: Lower level bound to search for(inclusive)
        :param int level_to: Upper level bound to search for(inclusive)
        :rtype TypeError: On invalid argument type
        """
        is_int(level_from, level_to)
        if(level_from < 1):
            level_from = 1

        response = http_get(BESTIARY_API_ENDPOINTS['get_beasts_by_level'].format(level_from = level_from, level_to = level_to))
        return response.json()
