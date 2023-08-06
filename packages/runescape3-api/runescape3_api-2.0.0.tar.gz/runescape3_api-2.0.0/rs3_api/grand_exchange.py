from datetime import datetime, timezone
from rs3_api.httpService.http_request import http_get
from .endpoints import GRAND_EXCHANGE_API_ENDPOINTS
from .utils.jagex import abbrv_price_to_num, is_int, is_str, is_valid_category, unwrap_category_dict

class GrandExchange:
    """ Grand Exchange """

    def get_catalogue(self, categoryId: int) -> dict:
        """ Gets the number of items determined by the first letter in category. 
        
        :param int categoryId: id of the category
        :rtype dict
        :raises Exception: if category is an invalid integer.
        :raises TypeError: if category argument is not an integer.
        """

        # Argument type validation
        is_int(categoryId)
        is_valid_category(categoryId)

        response = http_get(GRAND_EXCHANGE_API_ENDPOINTS['catalogue'].format(categoryId = categoryId))
        content = unwrap_category_dict(response.json())
        return content


    def get_runedate(self) -> dict:
        """ Return the runedate of when the grand exchange was last updated 
        rtype: dict
        """
        response = http_get(GRAND_EXCHANGE_API_ENDPOINTS['runedate'])
        return response.json()

    def get_items(self, categoryId: int, searchString: str, page: int = 1) -> dict:
        """ Gets twelve items determined by category and first letters of search string
        :param int categoryId
        :param str searchString: search for items that start with this string
        :page int: which page of twelve to fetch, default = 1
        :raises TypeError: if parameters are of the wrong type
        :raises Exception: if categoryId is an invalid integer
        """

        # Argument validation
        is_int(categoryId, page)
        is_str(searchString)
        is_valid_category(categoryId)

        response = http_get(GRAND_EXCHANGE_API_ENDPOINTS['items']
            .format(categoryId = categoryId, searchString = searchString.lower(), page = page))

        return response.json()

    def get_item_detail(self, itemId: int) -> dict:
        """ Returns current price and price trends information on tradeable items in the Grand Exchange,
        the category, item image and examine for the given item
        :param int itemId
        :raises TypeError: if itemId is of the wrong type
        """

        # Argument validation
        is_int(itemId)

        response = http_get(GRAND_EXCHANGE_API_ENDPOINTS['item_detail'].format(itemId=itemId))
        content = response.json()['item']

        # Get unabbreviated prices.
        current_price = abbrv_price_to_num(str(content['current']['price']))
        today_price = abbrv_price_to_num(str(content['today']['price']))

        # Create new key with int value of the price.
        content['current']['price_num'] = current_price
        content['today']['price_num'] = today_price

        return content

    
    def get_item_graph(self, itemId: int) -> dict:
        """ Graph shows the prices each day of a given item for the previous 180 days.
        When no price information is available, then a value of zero is returned.
        :param int itemId
        :raises TypeError: if itemId is of the wrong type
        """
        
        is_int(itemId)

        response = http_get(GRAND_EXCHANGE_API_ENDPOINTS['graph'].format(itemId=itemId))
        content = response.json()
        # Daily is the item trade history over the past day
        # Average is the item trade history for today
        ret_dict = {'daily': [], 'average': []}

        for key, value in content['daily'].items():
            temp_dict = {}
            seconds = int(key) / 1000.0
            temp_dict['epoch'] = datetime.fromtimestamp(seconds, timezone.utc)
            temp_dict['price'] = value
            ret_dict['daily'].append(temp_dict)
        
        for key, value in content['average'].items():
            temp_dict = {}
            seconds = int(key) / 1000.0
            temp_dict['epoch'] = datetime.fromtimestamp(seconds, timezone.utc)
            temp_dict['price'] = value
            ret_dict['average'].append(temp_dict)

        return ret_dict