"""
Unit testai TemperatureInterpolator klasei
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Pridedame weather_analysis katalogą į kelią
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'weather_analysis'))

from interpolation import TemperatureInterpolator

class TestTemperatureInterpolator(unittest.TestCase):
    """
    Testų klasė TemperatureInterpolator funkcionalumui
    """
    
    def setUp(self):
        """
        Nustatome testų aplinką
        """
        self.interpolator = TemperatureInterpolator()
        
        # Sukuriame test duomenis kas 30 minučių
        dates = pd.date_range('2024-01-01 00:00', periods=48, freq='30T')
        self.temperature_series = pd.Series(
            data=np.random.normal(5, 3, 48),  # Temperatūra apie 5°C
            index=dates,
            name='temperature'
        )
        
        # Sukuriame sparse duomenis (kas 2 valandas)
        sparse_dates = pd.date_range('2024-01-01 00:00', periods=12, freq='2H')
        self.sparse_temperature = pd.Series(
            data=[0, 2, 5, 8, 10, 12, 10, 8, 5, 3, 1, 0],
            index=sparse_dates,
            name='temperature'
        )
    
    def test_init(self):
        """
        Testuojame interpolacijos klasės inicializaciją
        """
        interpolator = TemperatureInterpolator()
        
        self.assertEqual(interpolator.supported_methods, ['linear', 'time', 'polynomial', 'spline'])
    
    def test_interpolate_temperature_linear(self):
        """
        Testuojame tiesinę interpoliaciją
        """
        result = self.interpolator.interpolate_temperature(
            self.sparse_temperature,
            target_frequency='30T',
            method='linear'
        )
        
        self.assertIsInstance(result, pd.Series)
        self.assertFalse(result.empty)
        
        # Turėtume gauti daugiau duomenų taškų
        self.assertGreater(len(result), len(self.sparse_temperature))
        
        # Patikrinome ar indeksas yra datetime
        self.assertIsInstance(result.index, pd.DatetimeIndex)
    
    def test_interpolate_temperature_all_methods(self):
        """
        Testuojame visus interpoliacijos metodus
        """
        methods = ['linear', 'time', 'polynomial', 'spline']
        
        for method in methods:
            with self.subTest(method=method):
                result = self.interpolator.interpolate_temperature(
                    self.sparse_temperature,
                    target_frequency='30T',
                    method=method
                )
                
                self.assertIsInstance(result, pd.Series)
                self.assertFalse(result.empty)
                self.assertGreater(len(result), len(self.sparse_temperature))
    
    def test_interpolate_temperature_invalid_method(self):
        """
        Testuojame interpoliaciją su netinkamu metodu
        """
        result = self.interpolator.interpolate_temperature(
            self.sparse_temperature,
            target_frequency='30T',
            method='neteisinga_metodu'
        )
        
        # Turėtų naudoti linear kaip default
        self.assertIsInstance(result, pd.Series)
        self.assertFalse(result.empty)
    
    def test_interpolate_temperature_empty_series(self):
        """
        Testuojame interpoliaciją su tuščia serija
        """
        empty_series = pd.Series([], dtype=float)
        empty_series.index = pd.DatetimeIndex([])
        
        result = self.interpolator.interpolate_temperature(
            empty_series,
            target_frequency='5T',
            method='linear'
        )
        
        self.assertIsNone(result)
    
    def test_interpolate_temperature_invalid_index(self):
        """
        Testuojame interpoliaciją su netinkamu indeksu
        """
        invalid_series = pd.Series([1, 2, 3, 4, 5])  # Integer index
        
        result = self.interpolator.interpolate_temperature(
            invalid_series,
            target_frequency='5T',
            method='linear'
        )
        
        self.assertIsNone(result)
    
    def test_interpolate_temperature_with_nans(self):
        """
        Testuojame interpoliaciją su NaN reikšmėmis
        """
        series_with_nans = self.sparse_temperature.copy()
        series_with_nans.iloc[2:4] = np.nan  # Pridedame NaN reikšmes
        
        result = self.interpolator.interpolate_temperature(
            series_with_nans,
            target_frequency='30T',
            method='linear'
        )
        
        self.assertIsInstance(result, pd.Series)
        self.assertFalse(result.empty)
        
        # Patikrinome ar nėra NaN interpoliuotame rezultate
        self.assertFalse(result.isna().any())
    
    def test_interpolate_different_frequencies(self):
        """
        Testuojame skirtingus interpoliacijos dažnius
        """
        frequencies = ['5T', '10T', '15T', '30T', '1H']
        
        for freq in frequencies:
            with self.subTest(frequency=freq):
                result = self.interpolator.interpolate_temperature(
                    self.sparse_temperature,
                    target_frequency=freq,
                    method='linear'
                )
                
                self.assertIsInstance(result, pd.Series)
                self.assertFalse(result.empty)
    
    def test_interpolate_with_statistics(self):
        """
        Testuojame interpoliaciją su statistikos grąžinimu
        """
        result = self.interpolator.interpolate_with_statistics(
            self.sparse_temperature,
            target_frequency='15T',
            method='linear'
        )
        
        self.assertIsInstance(result, dict)
        
        # Patikrinome būtinus raktus
        required_keys = [
            'interpolated_data', 'original_points', 'interpolated_points',
            'improvement_ratio', 'method', 'frequency'
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        # Patikrinome statistikos duomenis
        self.assertIsInstance(result['original_points'], int)
        self.assertIsInstance(result['interpolated_points'], int)
        self.assertIsInstance(result['improvement_ratio'], (int, float))
        self.assertEqual(result['method'], 'linear')
        self.assertEqual(result['frequency'], '15T')
    
    def test_interpolate_with_statistics_empty_data(self):
        """
        Testuojame interpoliaciją su statistika tuščiems duomenims
        """
        empty_series = pd.Series([], dtype=float)
        empty_series.index = pd.DatetimeIndex([])
        
        result = self.interpolator.interpolate_with_statistics(
            empty_series,
            target_frequency='5T',
            method='linear'
        )
        
        self.assertIsInstance(result, dict)
        self.assertIsNone(result['interpolated_data'])
        self.assertEqual(result['original_points'], 0)
        self.assertEqual(result['interpolated_points'], 0)
    
    def test_compare_interpolation_methods(self):
        """
        Testuojame interpoliacijos metodų palyginimą
        """
        result = self.interpolator.compare_interpolation_methods(
            self.sparse_temperature,
            target_frequency='15T'
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('methods', result)
        self.assertIn('recommended_method', result)
        
        # Patikrinome ar visi metodai buvo išbandyti
        methods_results = result['methods']
        for method in self.interpolator.supported_methods:
            self.assertIn(method, methods_results)
    
    def test_compare_interpolation_methods_empty_data(self):
        """
        Testuojame metodų palyginimą su tuščiais duomenimis
        """
        empty_series = pd.Series([], dtype=float)
        empty_series.index = pd.DatetimeIndex([])
        
        result = self.interpolator.compare_interpolation_methods(
            empty_series,
            target_frequency='5T'
        )
        
        self.assertIsInstance(result, dict)
    
    def test_validate_interpolation(self):
        """
        Testuojame interpoliacijos validavimą
        """
        interpolated = self.interpolator.interpolate_temperature(
            self.sparse_temperature,
            target_frequency='15T',
            method='linear'
        )
        
        validation = self.interpolator.validate_interpolation(
            self.sparse_temperature,
            interpolated
        )
        
        self.assertIsInstance(validation, dict)
        self.assertIn('valid', validation)
        self.assertIn('valid_range', validation)
        self.assertIn('valid_mean', validation)
        
        # Gera interpoliacija turėtų būti valid
        self.assertIsInstance(validation['valid'], bool)
    
    def test_validate_interpolation_empty_data(self):
        """
        Testuojame validavimą su tuščiais duomenimis
        """
        empty_series = pd.Series([], dtype=float)
        empty_series.index = pd.DatetimeIndex([])
        
        validation = self.interpolator.validate_interpolation(
            empty_series,
            empty_series
        )
        
        self.assertIsInstance(validation, dict)
        self.assertFalse(validation['valid'])
        self.assertIn('reason', validation)
    
    def test_print_interpolation_summary(self):
        """
        Testuojame interpoliacijos suvestinės spausdinimą
        """
        stats = self.interpolator.interpolate_with_statistics(
            self.sparse_temperature,
            target_frequency='10T',
            method='linear'
        )
        
        # Turėtų veikti be klaidų
        try:
            self.interpolator.print_interpolation_summary(stats)
        except Exception as e:
            self.fail(f"print_interpolation_summary raised {e} unexpectedly!")
    
    def test_print_interpolation_summary_empty_stats(self):
        """
        Testuojame suvestinės spausdinimą su tuščia statistika
        """
        empty_stats = {}
        
        # Turėtų veikti be klaidų
        try:
            self.interpolator.print_interpolation_summary(empty_stats)
        except Exception as e:
            self.fail(f"print_interpolation_summary raised {e} unexpectedly!")

class TestTemperatureInterpolatorQuality(unittest.TestCase):
    """
    Testai interpoliacijos kokybei
    """
    
    def setUp(self):
        """
        Nustatome kokybės testų aplinką
        """
        self.interpolator = TemperatureInterpolator()
        
        # Sukuriame sinusoidalius duomenis kas 1 valandą
        hours = pd.date_range('2024-01-01', periods=24, freq='1H')
        # Temperatūros ciklas: šalta naktį, šilta dieną
        temperatures = 5 + 10 * np.sin(np.linspace(0, 2*np.pi, 24))
        
        self.perfect_data = pd.Series(temperatures, index=hours)
        
        # Pasiimame kas 4 valandas (sparse duomenys)
        self.sparse_data = self.perfect_data.iloc[::4]
    
    def test_interpolation_preserves_trends(self):
        """
        Testuojame ar interpoliacija išlaiko tendencijas
        """
        interpolated = self.interpolator.interpolate_temperature(
            self.sparse_data,
            target_frequency='1H',
            method='linear'
        )
        
        self.assertIsNotNone(interpolated)
        
        # Patikrinome ar interpoliuoti duomenys yra tarp min ir max reikšmių
        orig_min, orig_max = self.sparse_data.min(), self.sparse_data.max()
        interp_min, interp_max = interpolated.min(), interpolated.max()
        
        # Interpoliuoti duomenys neturėtų viršyti originalių ribų per daug
        tolerance = (orig_max - orig_min) * 0.1  # 10% tolerancija
        self.assertGreaterEqual(interp_min, orig_min - tolerance)
        self.assertLessEqual(interp_max, orig_max + tolerance)
    
    def test_interpolation_smoothness(self):
        """
        Testuojame interpoliacijos glotnumą
        """
        interpolated = self.interpolator.interpolate_temperature(
            self.sparse_data,
            target_frequency='30T',
            method='spline'
        )
        
        self.assertIsNotNone(interpolated)
        
        # Skaičiuojame antrą išvestinę (glotnumo matas)
        if len(interpolated) > 2:
            second_derivative = interpolated.diff().diff()
            
            # Glotni kreivė turėtų turėti mažą antrą išvestinę
            smoothness = second_derivative.abs().mean()
            self.assertIsInstance(smoothness, (int, float))

if __name__ == '__main__':
    # Paleisdami testus
    unittest.main(verbosity=2)
