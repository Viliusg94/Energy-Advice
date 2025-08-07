"""
Unit testai WeatherAPI klasei
"""

import unittest
from unittest.mock import patch, Mock
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Pridedame weather_analysis katalogą į kelią
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'weather_analysis'))

from weather_api import WeatherAPI, CITY_CODES

class TestWeatherAPI(unittest.TestCase):
    """
    Testų klasė WeatherAPI funkcionalumui
    """
    
    def setUp(self):
        """
        Nustatome testų aplinką
        """
        self.api = WeatherAPI("vilnius")
        self.mock_response_data = {
            'observations': [
                {
                    'observationTimeUtc': '2024-01-01T12:00:00Z',
                    'airTemperature': 5.5,
                    'relativeHumidity': 80,
                    'windSpeed': 3.2,
                    'seaLevelPressure': 1013.2
                },
                {
                    'observationTimeUtc': '2024-01-01T13:00:00Z',
                    'airTemperature': 6.0,
                    'relativeHumidity': 78,
                    'windSpeed': 3.5,
                    'seaLevelPressure': 1013.5
                }
            ]
        }
        
        self.mock_forecast_data = {
            'forecastTimestamps': [
                {
                    'forecastTimeUtc': '2024-01-02T12:00:00Z',
                    'airTemperature': 7.0,
                    'totalPrecipitation': 0.0
                },
                {
                    'forecastTimeUtc': '2024-01-02T13:00:00Z',
                    'airTemperature': 7.5,
                    'totalPrecipitation': 0.5
                }
            ]
        }
    
    def test_init_valid_location(self):
        """
        Testuojame teisingą inicializaciją su galiojančiu miesto kodu
        """
        api = WeatherAPI("kaunas")
        self.assertEqual(api.location_code, "kaunas")
        self.assertEqual(api.base_url, "https://api.meteo.lt/")
        self.assertIsNotNone(api.timezone)
    
    def test_init_invalid_location(self):
        """
        Testuojame inicializaciją su negaliojančiu miesto kodu
        """
        api = WeatherAPI("neteisinga_vieta")
        self.assertEqual(api.location_code, "vilnius")  # Turėtų grįžti į default
    
    @patch('weather_api.requests.get')
    def test_make_request_success(self, mock_get):
        """
        Testuojame sėkmingą API užklausą
        """
        # Nustatome mock atsakymą
        mock_response = Mock()
        mock_response.json.return_value = self.mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.api._make_request("test_endpoint")
        
        self.assertEqual(result, self.mock_response_data)
        mock_get.assert_called_once()
    
    @patch('weather_api.requests.get')
    def test_make_request_failure(self, mock_get):
        """
        Testuojame nesėkmingą API užklausą
        """
        # Nustatome mock klaidą
        mock_get.side_effect = Exception("API klaida")
        
        result = self.api._make_request("test_endpoint")
        
        self.assertIsNone(result)
    
    @patch.object(WeatherAPI, '_make_request')
    def test_get_historical_data_success(self, mock_request):
        """
        Testuojame sėkmingą istorinių duomenų gavimą
        """
        mock_request.return_value = self.mock_response_data
        
        start_date = "2024-01-01"
        end_date = "2024-01-02"
        
        result = self.api.get_historical_data(start_date, end_date)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)
        self.assertEqual(len(result), 2)
        mock_request.assert_called_once()
    
    @patch.object(WeatherAPI, '_make_request')
    def test_get_historical_data_no_data(self, mock_request):
        """
        Testuojame istorinių duomenų gavimą kai nėra duomenų
        """
        mock_request.return_value = {'observations': []}
        
        result = self.api.get_historical_data("2024-01-01", "2024-01-02")
        
        self.assertIsNone(result)
    
    def test_get_historical_data_invalid_dates(self):
        """
        Testuojame neteisingų datų apdorojimą
        """
        # Pradžios data vėlesnė už pabaigos datą
        result = self.api.get_historical_data("2024-01-02", "2024-01-01")
        self.assertIsNone(result)
        
        # Neteisingas datos formatas
        result = self.api.get_historical_data("neteisingadata", "2024-01-02")
        self.assertIsNone(result)
    
    @patch.object(WeatherAPI, '_make_request')
    def test_get_forecast_data_success(self, mock_request):
        """
        Testuojame sėkmingą prognozės duomenų gavimą
        """
        mock_request.return_value = self.mock_forecast_data
        
        result = self.api.get_forecast_data()
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)
        self.assertEqual(len(result), 2)
    
    @patch.object(WeatherAPI, '_make_request')
    def test_get_forecast_data_no_data(self, mock_request):
        """
        Testuojame prognozės duomenų gavimą kai nėra duomenų
        """
        mock_request.return_value = {'forecastTimestamps': []}
        
        result = self.api.get_forecast_data()
        
        self.assertIsNone(result)
    
    @patch.object(WeatherAPI, '_make_request')
    def test_get_current_conditions_success(self, mock_request):
        """
        Testuojame dabartinių oro sąlygų gavimą
        """
        mock_current_data = {
            'airTemperature': 10.5,
            'relativeHumidity': 75,
            'observationTimeUtc': '2024-01-01T15:00:00Z'
        }
        mock_request.return_value = mock_current_data
        
        result = self.api.get_current_conditions()
        
        self.assertEqual(result, mock_current_data)
    
    @patch.object(WeatherAPI, '_make_request')
    def test_get_current_conditions_failure(self, mock_request):
        """
        Testuojame dabartinių oro sąlygų gavimo klaidą
        """
        mock_request.return_value = None
        
        result = self.api.get_current_conditions()
        
        self.assertIsNone(result)
    
    def test_city_codes_constant(self):
        """
        Testuojame miestų kodų konstantą
        """
        self.assertIn("vilnius", CITY_CODES)
        self.assertIn("kaunas", CITY_CODES)
        self.assertIn("klaipeda", CITY_CODES)
        self.assertIsInstance(CITY_CODES, dict)

class TestWeatherAPIIntegration(unittest.TestCase):
    """
    Integracijos testai (reikalauja interneto ryšio)
    """
    
    def setUp(self):
        """
        Nustatome integracijos testų aplinką
        """
        self.api = WeatherAPI("vilnius")
    
    @unittest.skip("Integracijos testas - reikalauja interneto ryšio")
    def test_real_api_call(self):
        """
        Testuojame realų API iškvietimą (praleidžiamas default)
        """
        # Šis testas veiks tik su realiu interneto ryšiu
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        result = self.api.get_historical_data(start_date, end_date)
        
        # Jei API veikia, turėtume gauti DataFrame arba None
        self.assertTrue(result is None or isinstance(result, pd.DataFrame))

if __name__ == '__main__':
    # Paleisdami testus
    unittest.main(verbosity=2)
