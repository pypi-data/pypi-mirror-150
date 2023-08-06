from .endpoints import HISCORE_API_ENDPOINTS
from .models import SKILLS, ACTIVITIES
from .utils.jagex import parse_player_to_dict, is_str, is_int
from .httpService.http_request import http_get

class Hiscores:

    """Player Hiscores"""
    def get_ranking(self, index: int = 0, category: str = "skill", size: int = 25) -> dict:
        """Gets hiscore ranks in a particular skill or activity

        :param int index: index of the skill or activity to fetch
        :param str category: 'skill' or 'activity'
        :param int size: How many results you want back, default = 25
        :rtype: dict
        :raises Exception: If there is invalid category argument
        """
        # Argument type validation
        is_int(index)
        # Category must be either 'skill' or 'activity'
        if(category != "activity" and category != "skill"):
            raise Exception("Invalid category must be: skill | activity")

        category_id = 0 if category == "skill" else 1
        response = http_get(HISCORE_API_ENDPOINTS['ranking'].format(index = index, category = category_id, size = size))
        content = response.json()

        skill_or_activity = SKILLS[index] if category_id == 0 else ACTIVITIES[index]
        return_dict = {
            "category": skill_or_activity,
            "rankings": content
        }
        return return_dict

    def get_index_lite(self, game_mode: str, username: str) -> dict:
        """Gets a players hiscore profile

        :param str game_mode: Name of players game mode
        :param str username: Players username
        :rtype: dict
        :raises Exception: if api returns a 404 error
        """
        # Argument type validation
        is_str(game_mode, username)

        game_mode = game_mode.lower()
        # Check if game mode string is valid
        if(not self.__game_mode_validation(game_mode)):
            game_mode = "normal"
        #Call the requests service
        response = http_get(HISCORE_API_ENDPOINTS[game_mode].format(username = username))
        #TODO Look into this, probably removable
        # If username does not exist it return a html that include an error404 string
        if("error404" in response.text):
            raise Exception("Runescape API throws error404, most likely username does not exist on hiscore")
        # Parse the content from the api into a usable dictionary
        content = parse_player_to_dict(response.text, username)

        return content

    """Player Season Rankings"""
    def get_current_seasonal_ranking(self, username: str) -> list:
        """Gets a players current seasonal stats

        :param str username: Players username
        :rtype: list
        """
        # Argument type checking
        is_str(username)

        response = http_get(HISCORE_API_ENDPOINTS["season_ranking"].format(username = username))
        return response.json()

    def get_past_seasonal_ranking(self, username: str) -> list:
        """Gets a players past season stats(archived)

        :param str username: Players username
        :rtype: list
        """
        # Argument type checking
        is_str(username)

        response = http_get(HISCORE_API_ENDPOINTS["past_season_ranking"].format(username = username))
        return response.json()

    """Season Details"""
    def get_season_details(self) -> list:
        """Gets details about the current season
        rtype: list
        """
        response = http_get(HISCORE_API_ENDPOINTS["season_detail"])
        return response.json()

    def get_past_season_details(self) -> list:
        """Gets details past seasons
        rtype: list
        """
        response = http_get(HISCORE_API_ENDPOINTS["past_season_detail"])
        return response.json()

    """Clans"""
    def get_clan_ranking(self) -> list:
        """Returns details about the top 3 clans
        rtype: list
        """
        response = http_get(HISCORE_API_ENDPOINTS["clan_ranking"])
        return response.json()


    """Helper functions"""

    def __game_mode_validation(self, game_mode):
        if(game_mode == "normal" or game_mode == "ironman" or game_mode == "hardcore"):
            return True
        else:
            return False
