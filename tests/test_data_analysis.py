"""
Unit testai WeatherAnalyzer klasei
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Pridedame weather_analysis katalogą į kelią
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'weather_analysis'))

from data_analysis import WeatherAnalyzer

class TestWeatherAnalyzer(unittest.TestCase):
    """
    Testų klasė WeatherAnalyzer funkcionalumui
    """
    
    def setUp(self):
        """
        Nustatome testų aplinką
        """
        # Sukuriame mock istorinių duomenų DataFrame
        dates = pd.date_range('2024-01-01', periods=168, freq='H')  # 7 dienos kas valandą
        self.historical_data = pd.DataFrame({
            'airTemperature': np.random.normal(5, 10, 168),  # Temperatūra apie 5°C
            'relativeHumidity': np.random.normal(75, 15, 168),  # Drėgmė apie 75%
            'windSpeed': np.random.exponential(3, 168),  # Vėjo greitis
            'seaLevelPressure': np.random.normal(1013, 20, 168)  # Slėgis
        }, index=dates)
        
        # Sukuriame mock prognozės duomenų DataFrame
        forecast_dates = pd.date_range('2024-01-08', periods=48, freq='H')  # 2 dienos
        self.forecast_data = pd.DataFrame({
            'airTemperature': np.random.normal(7, 8, 48),
            'totalPrecipitation': np.random.exponential(0.5, 48)  # Krituliai
        }, index=forecast_dates)
        
        self.analyzer = WeatherAnalyzer(self.historical_data, self.forecast_data)
    
    def test_init_with_data(self):
        """
        Testuojame inicializaciją su duomenimis
        """
        analyzer = WeatherAnalyzer(self.historical_data, self.forecast_data)
        
        self.assertIsNotNone(analyzer.historical_data)
        self.assertIsNotNone(analyzer.forecast_data)
        self.assertIsNotNone(analyzer.combined_data)
    
    def test_init_without_data(self):
        """
        Testuojame inicializaciją be duomenų
        """
        analyzer = WeatherAnalyzer()
        
        self.assertIsNone(analyzer.historical_data)
        self.assertIsNone(analyzer.forecast_data)
        self.assertIsNone(analyzer.combined_data)
    
    def test_combine_data(self):
        """
        Testuojame duomenų sujungimą
        """
        result = self.analyzer.combine_data()
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)
        # Turėtume turėti istorinius + prognozės duomenis
        expected_length = len(self.historical_data) + len(self.forecast_data)
        self.assertGreater(len(result), 0)
    
    def test_combine_data_no_common_columns(self):
        """
        Testuojame duomenų sujungimą kai nėra bendrų stulpelių
        """
        # Sukuriame duomenis be bendrų stulpelių
        different_forecast = pd.DataFrame({
            'differentColumn': [1, 2, 3]
        }, index=pd.date_range('2024-01-08', periods=3, freq='H'))
        
        analyzer = WeatherAnalyzer(self.historical_data, different_forecast)
        result = analyzer.combine_data()
        
        self.assertTrue(result.empty)
    
    def test_calculate_annual_averages(self):
        """
        Testuojame metinių vidurkių skaičiavimą
        """
        result = self.analyzer.calculate_annual_averages()
        
        self.assertIsInstance(result, dict)
        self.assertIn('average_temperature', result)
        self.assertIn('average_humidity', result)
        self.assertIn('average_wind_speed', result)
        self.assertIn('average_pressure', result)
        
        # Patikrinome ar vidurkiai yra realistiniai
        self.assertIsInstance(result['average_temperature'], (int, float))
        self.assertIsInstance(result['average_humidity'], (int, float))
    
    def test_calculate_annual_averages_empty_data(self):
        """
        Testuojame metinių vidurkių skaičiavimą su tuščiais duomenimis
        """
        empty_analyzer = WeatherAnalyzer()
        result = empty_analyzer.calculate_annual_averages()
        
        self.assertEqual(result, {})
    
    def test_analyze_day_night_temperature(self):
        """
        Testuojame dienos/nakties temperatūros analizę
        """
        result = self.analyzer.analyze_day_night_temperature()
        
        self.assertIsInstance(result, dict)
        self.assertIn('average_day_temperature', result)
        self.assertIn('average_night_temperature', result)
        self.assertIn('day_night_difference', result)
        
        # Patikrinome ar rezultatai yra skaičiai
        for key, value in result.items():
            self.assertIsInstance(value, (int, float))
    
    def test_analyze_day_night_temperature_no_temp_data(self):
        """
        Testuojame dienos/nakties analizę be temperatūros duomenų
        """
        data_without_temp = self.historical_data.drop('airTemperature', axis=1)
        analyzer = WeatherAnalyzer(data_without_temp)
        
        result = analyzer.analyze_day_night_temperature()
        
        self.assertEqual(result, {})
    
    def test_analyze_weekend_rain_forecast(self):
        """
        Testuojame savaitgalių lietaus prognozės analizę
        """
        # Pridedame savaitgalius į prognozės duomenis
        weekend_dates = pd.date_range('2024-01-06', periods=48, freq='H')  # Prasideda šeštadienį
        weekend_forecast = pd.DataFrame({
            'totalPrecipitation': np.random.exponential(0.5, 48)
        }, index=weekend_dates)
        
        analyzer = WeatherAnalyzer(self.historical_data, weekend_forecast)
        result = analyzer.analyze_weekend_rain_forecast()
        
        self.assertIsInstance(result, dict)
        self.assertIn('weekend_rain_days', result)
        self.assertIn('total_weekend_days', result)
        self.assertIn('rain_probability', result)
    
    def test_analyze_weekend_rain_forecast_empty_data(self):
        """
        Testuojame savaitgalių lietaus analizę su tuščiais duomenimis
        """
        empty_analyzer = WeatherAnalyzer()
        result = empty_analyzer.analyze_weekend_rain_forecast()
        
        self.assertEqual(result, {})
    
    def test_get_last_week_data(self):
        """
        Testuojame paskutinės savaitės duomenų gavimą
        """
        result = self.analyzer.get_last_week_data()
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)
        
        # Patikrinome ar duomenys yra per paskutinę savaitę
        max_date = self.historical_data.index.max()
        min_expected_date = max_date - timedelta(days=7)
        
        self.assertTrue(result.index.min() >= min_expected_date)
    
    def test_get_last_week_data_empty(self):
        """
        Testuojame paskutinės savaitės duomenų gavimą su tuščiais duomenimis
        """
        empty_analyzer = WeatherAnalyzer()
        result = empty_analyzer.get_last_week_data()
        
        self.assertTrue(result.empty)
    
    def test_print_analysis_results(self):
        """
        Testuojame analizės rezultatų spausdinimą (be klaidos)
        """
        annual_avg = {'average_temperature': 5.5, 'average_humidity': 75.0}
        day_night = {'average_day_temperature': 6.0, 'average_night_temperature': 4.0}
        weekend_rain = {'weekend_rain_days': 2, 'rain_probability': 25.0}
        
        # Turėtų veikti be klaidų
        try:
            self.analyzer.print_analysis_results(annual_avg, day_night, weekend_rain)
        except Exception as e:
            self.fail(f"print_analysis_results raised {e} unexpectedly!")

class TestWeatherAnalyzerEdgeCases(unittest.TestCase):
    """
    Testai kraštutinių atvejų
    """
    
    def test_analyzer_with_nan_values(self):
        """
        Testuojame analizę su NaN reikšmėmis
        """
        dates = pd.date_range('2024-01-01', periods=24, freq='H')
        data_with_nans = pd.DataFrame({
            'airTemperature': [5.0, np.nan, 7.0, np.nan, 6.0] * 5 + [5.0, 7.0, 6.0, np.nan],
            'relativeHumidity': [75.0, 80.0, np.nan, 70.0, 85.0] * 5 + [75.0, 80.0, 70.0, 85.0]
        }, index=dates)
        
        analyzer = WeatherAnalyzer(data_with_nans)
        result = analyzer.calculate_annual_averages()
        
        # Turėtų skaičiuoti vidurkius ignoruojant NaN
        self.assertIn('average_temperature', result)
        self.assertIn('average_humidity', result)
        self.assertFalse(np.isnan(result['average_temperature']))
        self.assertFalse(np.isnan(result['average_humidity']))
    
    def test_analyzer_with_extreme_values(self):
        """
        Testuojame analizę su kraštutinėmis reikšmėmis
        """
        dates = pd.date_range('2024-01-01', periods=24, freq='H')
        extreme_data = pd.DataFrame({
            'airTemperature': [-50, 50, -30, 40, 0] * 5 + [-50, 50, -30, 40],
            'relativeHumidity': [0, 100, 10, 90, 50] * 5 + [0, 100, 10, 90]
        }, index=dates)
        
        analyzer = WeatherAnalyzer(extreme_data)
        result = analyzer.calculate_annual_averages()
        
        # Turėtų skaičiuoti be klaidų net su kraštutinėmis reikšmėmis
        self.assertIsInstance(result['average_temperature'], (int, float))
        self.assertIsInstance(result['average_humidity'], (int, float))

if __name__ == '__main__':
    # Paleisdami testus
    unittest.main(verbosity=2)
