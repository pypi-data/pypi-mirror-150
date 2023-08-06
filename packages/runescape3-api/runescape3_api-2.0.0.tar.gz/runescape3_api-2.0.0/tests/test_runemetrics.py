import os
import sys
sys.path.append(os.getcwd())
import pytest
from rs3_api.endpoints import RUNEMETRICS_API_ENDPOINTS
from rs3_api.runemetrics import Runemetrics

@pytest.fixture(scope='module')
def runemetrics():
    runemetrics = Runemetrics()
    return runemetrics

class TestRuneMetric():
    """Tests for get_monthly_experience"""
    def test_get_monthly_experience(self, runemetrics: Runemetrics):
        # Test for a successful call
        response = runemetrics.get_monthly_experience('Phyrexz', 'defence')

        # Assert that response if of type dict and
        # that the correct skill is returned
        assert isinstance(response, dict)
        assert response['monthlyXpGain'][0]['skillId'] == 1
        assert response['monthlyXpGain'][0]['skillName'] == 'defence'

    def test_get_monthly_experience_id_out_of_bounds(self, runemetrics: Runemetrics):
        # Test if exception is thrown if skill index is out of bounds
        with pytest.raises(Exception):
            runemetrics.get_monthly_experience('Phyrexz', 28)

    def test_get_monthly_experience_invalid_skill_string(self, runemetrics: Runemetrics):
        # Test if Exception is thrown when invalid string for skill name is supplied
        with pytest.raises(Exception):
            runemetrics.get_monthly_experience('Phyrexz', 'notaskillname')

    def test_get_monthly_experience_argument_type_error(self, runemetrics: Runemetrics):
        # Test if TypeError is thrown when invalid type is supplied as argument
        with pytest.raises(TypeError):
            response = runemetrics.get_monthly_experience(12, 12)


    """Tests for get_quests"""
    def test_get_quests(self, runemetrics: Runemetrics):
        response = runemetrics.get_quests('Phyrexz')

        assert isinstance(response, dict)
        assert isinstance(response['quests'], list)

    def test_get_quests_non_str_username(self, runemetrics: Runemetrics):
        with pytest.raises(TypeError):
            response = runemetrics.get_quests(12)


    """Tests for get_profile"""
    def test_get_profile(self, runemetrics: Runemetrics):
        response = runemetrics.get_profile('Phyrexz')

        assert isinstance(response, dict)

    def test_get_profile_non_int_parameter(self, runemetrics: Runemetrics):
        with pytest.raises(TypeError):
            response = runemetrics.get_profile('Phyrexz', "12")
