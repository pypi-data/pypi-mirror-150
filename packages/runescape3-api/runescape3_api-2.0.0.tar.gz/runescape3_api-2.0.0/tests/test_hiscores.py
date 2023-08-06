import os
import sys
sys.path.append(os.getcwd())
import pytest
from rs3_api.endpoints import HISCORE_API_ENDPOINTS
from rs3_api.hiscores import Hiscores
from requests.exceptions import HTTPError

@pytest.fixture(scope='module')
def hiscore():
    hiscore = Hiscores()
    return hiscore

class TestHiscores():

    """Testing parse_player_to_dict state leak"""
    def test_deep_copy(self, hiscore: Hiscores):
        hiscore_normal = hiscore.get_index_lite("normal", "Maddie May")
        normal_rank = hiscore_normal[u'skills'][u'overall'][u'rank']
        hiscore_hardcore = hiscore.get_index_lite("hardcore", "Maddie May")

        assert hiscore_normal[u'skills'][u'overall'][u'rank'] == normal_rank

    """Tests for get_ranking"""
    def test_get_ranking(self, hiscore: Hiscores):
        response = hiscore.get_ranking(0, "skill", 2)
        assert isinstance(response, dict)
        assert response['category'] == "overall"
        assert isinstance(response['rankings'], list)

    def test_get_ranking_type_exception(self, hiscore: Hiscores):
        with pytest.raises(Exception):
            hiscore.get_ranking(2, "invalid", 2)

    def test_get_ranking_type_error(self, hiscore: Hiscores):
        with pytest.raises(TypeError):
            hiscore.get_ranking("string_not_int")

    """Tests for get_index_lite"""
    def test_get_index_lite(self, hiscore: Hiscores):
        response = hiscore.get_index_lite("normal", "Phyrexz")
        assert isinstance(response, dict)

    def test_get_index_lite_invalid_mode(self, hiscore: Hiscores):
        response = hiscore.get_index_lite("invalid_mode", "Phyrexz")
        assert isinstance(response, dict)
        assert response["name"] == 'Phyrexz'

    def test_get_index_lite_type_error(self, hiscore: Hiscores):
        with pytest.raises(TypeError):
            hiscore.get_index_lite("normal", True)

    def test_get_index_lite_non_existing_username(self, hiscore: Hiscores):
        with pytest.raises(HTTPError):
            hiscore.get_index_lite("normal", "invaliduserna")

    """Tests for get_current_seasonal_ranking"""
    def test_get_season_ranking(self, hiscore: Hiscores):
        response = hiscore.get_current_seasonal_ranking("Maikeru")
        assert isinstance(response, list)

    def test_get_season_rankink_invalid_type(self, hiscore: Hiscores):
        with pytest.raises(TypeError):
            hiscore.get_current_seasonal_ranking(False)

    """Tests for get_past_seasonal_ranking"""
    def test_get_past_season_ranking(self, hiscore: Hiscores):
        response = hiscore.get_past_seasonal_ranking("Maikeru")
        assert isinstance(response, list)

    def test_get_past_season_ranking_invalid_type(self, hiscore: Hiscores):
        with pytest.raises(TypeError):
            hiscore.get_past_seasonal_ranking(False)

    """Tests for get_season_details"""
    def test_get_season_detail(self, hiscore: Hiscores):
        response = hiscore.get_season_details()

        assert isinstance(response, list)

    """Tests for get_past_season_details"""
    def test_get_past_season_detail(self, hiscore: Hiscores):
        response = hiscore.get_past_season_details()

        assert isinstance(response, list)
        assert len(response) > 0

    """Tests for get_clan_ranking"""
    def test_get_clan_ranking(self, hiscore: Hiscores):
        response = hiscore.get_clan_ranking()

        assert isinstance(response, list)
        assert len(response) == 3
