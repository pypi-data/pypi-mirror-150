from curses import has_key
from gzip import READ
import os
import re
import sys
sys.path.append(os.getcwd())
import pytest
from datetime import datetime
from rs3_api.endpoints import GRAND_EXCHANGE_API_ENDPOINTS
from rs3_api.grand_exchange import GrandExchange
from rs3_api.models import GECategories
from rs3_api.utils.jagex import abbrv_price_to_num, unwrap_category_dict
from requests.exceptions import HTTPError

@pytest.fixture(scope='module')
def grand_exchange():
    grand_exchange = GrandExchange()
    return grand_exchange

class TestGrandExchange():
    """Test Get Catalogue """
    def test_get_catalogue(self, grand_exchange : GrandExchange):
        response = grand_exchange.get_catalogue(GECategories.FAMILIARS)
        assert isinstance(response, dict)
        #TODO Should this be exhaustive and check for all keys .. ?
        assert '#' in response
        assert 'z' in response
        assert isinstance(response['#'], int)

    def test_get_catalogue_invalid_argument_type(self, grand_exchange : GrandExchange):
        with pytest.raises(TypeError):
            grand_exchange.get_catalogue("not an int")

    def test_get_catalogue_invalid_argument(self, grand_exchange : GrandExchange):
        with pytest.raises(Exception):
            grand_exchange.get_catalogue(50)


    """ Test Get Twelve Items """
    def test_get_items(self, grand_exchange: GrandExchange):
        response = grand_exchange.get_items(GECategories.FAMILIARS, 'c')

        assert isinstance(response, dict)
        assert isinstance(response['items'], list)

    """ Test Get Item Detail """
    def test_get_item_detail_success(self, grand_exchange: GrandExchange):
        response = grand_exchange.get_item_detail(21787) # Steadfast Boots
        assert isinstance(response, dict)
        assert 'current' in response
        assert 'icon' in response
        assert 'icon_large' in response
        assert 'id' in response
        assert 'type' in response
        assert 'typeIcon' in response
        assert 'name' in response
        assert 'description' in response
        assert 'current' in response
        assert 'today' in response
        assert 'members' in response
        assert 'day30' in response
        assert 'day90' in response
        assert 'day180' in response
        assert 'price_num' in response['current']
        assert 'price_num' in response['today']
        assert isinstance(response['current']['price_num'], int)


    def test_get_graph_sucess(self, grand_exchange: GrandExchange):
        response = grand_exchange.get_item_graph(21787) # Steadfast boots
        assert isinstance(response, dict)
        assert isinstance(response['daily'], list)
        assert isinstance(response['average'], list)
        assert isinstance(response['daily'][0]['epoch'], datetime)
        assert isinstance(response['daily'][0]['price'], int)


    #TODO : These belong in their own test file.
    """ Helper Function Tests """
    def test_unwrap_category_dict(self):
        category_dict = {"types":[],"alpha":[{"letter":"#","items":0},{"letter":"a","items":6},{"letter":"b","items":8},{"letter":"c","items":1},{"letter":"d","items":3},{"letter":"e","items":2},{"letter":"f","items":3},{"letter":"g","items":5},{"letter":"h","items":2},{"letter":"i","items":5},{"letter":"j","items":0},{"letter":"k","items":1},{"letter":"l","items":2},{"letter":"m","items":5},{"letter":"n","items":1},{"letter":"o","items":1},{"letter":"p","items":4},{"letter":"q","items":0},{"letter":"r","items":3},{"letter":"s","items":27},{"letter":"t","items":2},{"letter":"u","items":1},{"letter":"v","items":5},{"letter":"w","items":2},{"letter":"x","items":0},{"letter":"y","items":0},{"letter":"z","items":0}]}
        unwrapped_dict = unwrap_category_dict(category_dict)

        assert isinstance(unwrapped_dict, dict)
        assert unwrapped_dict['#'] == 0
        assert unwrapped_dict['a'] == 6

    def test_abbrv_price_to_num(self):
        abbrv_price_k = "41.2k"
        abbrv_price_m = "-41.2m"
        abbrv_price_b = "-1.9b"
        abbrv_price = "1200"
        result_k = abbrv_price_to_num(abbrv_price_k)
        result_m = abbrv_price_to_num(abbrv_price_m)
        result_b = abbrv_price_to_num(abbrv_price_b)
        result = abbrv_price_to_num(abbrv_price)

        assert isinstance(result, int)
        assert result_k == 41200
        assert isinstance(result, int)
        assert result_m == -41200000
        assert isinstance(result, int)
        assert result_b == -1900000000
        assert isinstance(result, int)
        assert result == 1200