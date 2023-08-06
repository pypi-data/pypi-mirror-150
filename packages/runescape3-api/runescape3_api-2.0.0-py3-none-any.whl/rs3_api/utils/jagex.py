from unicodedata import numeric
from ..models import PLAYER, SKILLS
import copy

def parse_player_to_dict(response: str, username: str):
    # Split the response by newline
    line_list = response.split()
    #Split each line by ',' delimeter and store in a list
    for i, item in enumerate(line_list, start=0):
        line_list[i] = item.split(',')

    # Filter the first 27 as skills category and last 30 as activities category
    skill_numbers = line_list[:29]
    activites_numbers = line_list[-30:]

    player = copy.deepcopy(PLAYER)
    player["name"] = username

    #Loop and set the skill variables in player dict
    for i, skill in enumerate(player["skills"], start=0):
        player["skills"][skill]["rank"] = skill_numbers[i][0]
        player["skills"][skill]["level"] = skill_numbers[i][1]
        player["skills"][skill]["experience"] = skill_numbers[i][2]

    #Loop and set the activities variables in player dict
    for i, activity in enumerate(player["activities"], start=0):
        player["activities"][activity]["rank"] = activites_numbers[i][0]
        player["activities"][activity]["score"] = activites_numbers[i][1]

    return player

def is_str(*arg):
    #Raises TypeError if any argument is not of type str
    if not all(isinstance(x, str) for x in arg):
        raise TypeError("Invalid argument type")

def is_int(*arg):
    #Raises TypeError if any argument is not of type int
    if not all(isinstance(x, int) for x in arg):
        raise TypeError("Invalid argument type")

def add_skillname_to_profile(profile: dict) -> dict:
    """Returns a modified profile with added skillname strings
    {
      'level': 99,
      'xp': 169867476,
      'rank': 144212,
      'id': 0,
      'skill' 'defence' <- Adding this to all skills
    }
    """
    for i, skill in enumerate(profile['skillvalues']):
        # For each skill create a new key,value pair
        # + 1 in SKILLS index is to account for no 'overall' skill therefore
        # All skills are shifted by 1 index(See models.py)
        profile['skillvalues'][i]['skillname'] = SKILLS[skill['id'] + 1]
    return profile


def is_valid_category(categoryId: int):
    # Category must be [0-41]
    if(categoryId < 0 or categoryId > 41):
        raise Exception("Cateogory must be between 0 and 41 inclusive")


def unwrap_category_dict(content):
    ret_dict = {}
    for letter in  content['alpha']:
        ret_dict[letter['letter']] = letter['items']

    return ret_dict

def abbrv_price_to_num(price: str) -> int:
    ret_val = 0
    last_letter = price[-1]
    if last_letter == 'k':
        num = int(float(price[:-1]) * 1000)
        return num
    elif last_letter == 'm':
        num = int(float(price[:-1]) * 1000000)
        return num
    elif last_letter == 'b':
        num = int(float(price[:-1]) * 1000000000)
        return num
    else:
        return int(price)
