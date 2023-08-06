import os
import sys
sys.path.append(os.getcwd())
import pytest
from rs3_api.endpoints import BESTIARY_API_ENDPOINTS
from rs3_api.bestiary import Bestiary
from requests.exceptions import HTTPError

@pytest.fixture(scope='module')
def bestiary():
    bestiary = Bestiary()
    return bestiary

class TestBestiary():
    """Test Get Bestiary Data"""
    def test_get_bestiary_data(self, bestiary: Bestiary):
        response = bestiary.get_beast(89) # Unicorn

        assert isinstance(response, dict)
        assert response['name'] == 'Unicorn'

    def test_get_bestiary_data_argument_type_error(self, bestiary: Bestiary):
        with pytest.raises(TypeError):
            response = bestiary.get_beast("Unicorn") # Wrong argument type

    """Test Bestiary Search"""
    def test_get_beast_by_term(self, bestiary: Bestiary):
        response = bestiary.get_beast_by_term("cow")

        assert isinstance(response, list)
        assert 'label' in response[0]
        assert 'value' in response[0]

    def test_get_beast_by_two_terms(self, bestiary: Bestiary):
        response = bestiary.get_beast_by_term("cow+rabbit")

        assert isinstance(response, list)
        assert 'label' in response[0]
        assert 'value' in response[0]

    def test_get_beast_by_ter_beast_does_not_exist(self, bestiary: Bestiary):
        response = bestiary.get_beast_by_term("nobeasthasthisname")

        assert isinstance(response, list)
        assert response[0] == "none"

    def test_get_beast_by_term_argument_type_error(self, bestiary: Bestiary):
        with pytest.raises(TypeError):
            response = bestiary.get_beast_by_term(12)

    """Test Beast Names By First Letter"""
    def test_get_beast_by_first_letter(self, bestiary: Bestiary):
        response = bestiary.get_beast_by_first_letter('q')

        assert isinstance(response, list)
        assert 'label' in response[0]
        assert 'value' in response[0]

    def test_get_areas(self, bestiary):
        response = bestiary.get_areas()

        assert isinstance(response, list)
        assert response

    """Get Beasts By In Area"""
    def test_get_beasts_by_area(self, bestiary):
        response = bestiary.get_beasts_by_area("The Abyss")

        assert isinstance(response, list)
        assert 'label' in response[0]
        assert 'value' in response[0]

    def test_get_beasts_by_invalid_area(self, bestiary):
        response = bestiary.get_beasts_by_area("Not An Area")

        assert isinstance(response, list)
        assert response[0] == "none"

    """Get Slayer Categories"""
    def test_get_slayer_categories(self, bestiary):
        response = bestiary.get_slayer_categories()

        assert isinstance(response, dict)

    """Get Slayer Beasts By Category"""
    def test_get_slayer_beast_by_category_id(self, bestiary):
        response = bestiary.get_slayer_beasts_by_category_id(41) # Aberrant Spectres

        assert isinstance(response, list)
        assert 'label' in response[0]
        assert 'value' in response[0]

    def test_get_slayer_beast_by_category_invalid_id(self, bestiary):
        response = bestiary.get_slayer_beasts_by_category_id(1000)

        assert isinstance(response, list)
        assert response[0] == "none"

    """Weakness Names"""
    def test_get_weakness_names(self, bestiary):
        response = bestiary.get_weakness_names()

        assert isinstance(response, dict)
        assert 'Air' in response

    """Beasts by weakness Id"""
    def test_beast_by_weakness_id(self, bestiary):
        response = bestiary.get_beasts_by_weakness_id(1)

        assert isinstance(response, list)
        assert isinstance(response[0], dict)
        assert 'label' in response[0]
        assert 'value' in response[0]

    """Test for get_beasts_by_level_group"""
    def test_get_beasts_by_level_group(self, bestiary):
        response = bestiary.get_beasts_by_level_group(140, 150)

        assert isinstance(response, list)
        assert isinstance(response[0], dict)
        assert 'label' in response[0]
        assert 'value' in response[0]

    def test_get_beasts_by_level_group_invalid_order(self, bestiary):
        response = bestiary.get_beasts_by_level_group(150, 140)

        assert isinstance(response, list)
        assert response[0] == "none"
