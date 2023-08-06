from .endpoints import RUNEMETRICS_API_ENDPOINTS
from .models import SKILLS
from .httpService.http_request import http_get
from .utils.jagex import is_str, is_int, add_skillname_to_profile

#TODO Look into get request timeout parameter to specify timeouts

class Runemetrics:

    def get_monthly_experience(self, username: str, skill_id: str) -> dict:
        """Gets players monthly experience stats for the last 12 months in a particular skill

        :param str username: Players username
        :param str: name of requested skill
        :raises TypeError: if argument are of wrong type
        :rtype: dict
        """
        is_str(username, skill_id)
        skill_id = self.validate_skill_input(skill_id)

        response = http_get(RUNEMETRICS_API_ENDPOINTS['monthly_experience'].format(username=username, skill_id=skill_id))
        content = response.json()
        content_skill_id = content['monthlyXpGain'][0]['skillId']
        content['monthlyXpGain'][0]['skillName'] = SKILLS[content_skill_id + 1]
        return content

    def get_quests(self, username: str) -> dict:
        """Gets players quest information

        :param str username: Players username
        :rtype: dict
        :raises TypeError: Username must be a string
        """
        is_str(username)

        response = http_get(RUNEMETRICS_API_ENDPOINTS['quests'].format(username=username))
        return response.json()

    def get_profile(self, username: str, activities: int = 20) -> dict:
        """Gets players runemetrics profile
        :param int activities: number of activities in response
        :param str username: Players username
        :rtype: dict
        :raises TypeError: Arguments must be of correct type
        """
        is_str(username)
        is_int(activities)

        if(activities not in range(0, 21)):
            # Default to 20 if anything outside boundaries is given
            activities = 20

        response = http_get(RUNEMETRICS_API_ENDPOINTS['profile'].format(username=username, activities=activities))

        # Modifying response content to have skillname strings added for better usability
        content = add_skillname_to_profile(response.json())
        return content

    """Validates skill_id by checking if it is out of bounds or a valid string of a skill """
    def validate_skill_input(self, skill_id):
        if(not SKILLS.__contains__(skill_id.lower())):
            raise Exception(f"No skill named {skill_id} exists!")
        skill_id = SKILLS.index(skill_id.lower()) - 1

        return skill_id
