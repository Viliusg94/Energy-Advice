# -*- coding: utf-8 -*-
"""
TemperatureInterpolator klasės unit testai
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Pridedame src katalogą į Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from interpolation import TemperatureInterpolator


class TestTemperatureInterpolator:
    """
    TemperatureInterpolator klasės testai
    """
    
    def setup_method(self):
        """
        Pradinis testų nustatymas
        """
        # Sukuriame test temperatūros duomenis kas 30 minučių
        dates = pd.date_range('2024-01-01 00:00', '2024-01-01 12:00', freq='30min', tz='Europe/Vilnius')
        np.random.seed(42)
        
        # Sukuriame realistiškas temperatūros reikšmes su trendu
        base_temps = np.linspace(-2, 5, len(dates))  # Temperatūra kyla per dieną
        noise = np.random.normal(0, 1, len(dates))  # Pridedame triukšmą
        temperatures = base_temps + noise
        
        self.temperature_data = pd.Series(temperatures, index=dates, name='temperatura')
        self.interpolator = TemperatureInterpolator(self.temperature_data)
        
    def test_init_with_data(self):
        """
        Testuoja objekto inicializavimą su duomenimis
        """
        assert self.interpolator.original_data is not None
        assert len(self.interpolator.original_data) > 0
        assert self.interpolator.interpolated_data is None
        
    def test_init_without_data(self):
        """
        Testuoja objekto inicializavimą be duomenų
        """
        interpolator = TemperatureInterpolator()
        assert interpolator.original_data is None
        assert interpolator.interpolated_data is None
        
    def test_interpolate_to_5min_linear_success(self):
        """
        Testuoja tiesinę interpoliaciją iki 5 minučių
        """
        result = self.interpolator.interpolate_to_5min('linear')
        
        assert isinstance(result, pd.Series)
        assert not result.empty
        assert len(result) > len(self.temperature_data)
        
        # Patikrinome ar laiko intervalas teisingas (5 min)
        time_diffs = result.index[1:] - result.index[:-1]
        expected_diff = timedelta(minutes=5)
        assert all(diff == expected_diff for diff in time_diffs)
        
    def test_interpolate_to_5min_time_success(self):
        """
        Testuoja laiko pagrįstą interpoliaciją
        """
        result = self.interpolator.interpolate_to_5min('time')
        
        assert isinstance(result, pd.Series)
        assert not result.empty
        assert len(result) > len(self.temperature_data)
        
    def test_interpolate_to_5min_polynomial_success(self):
        """
        Testuoja polinominę interpoliaciją
        """
        result = self.interpolator.interpolate_to_5min('polynomial', polynomial_order=2)
        
        assert isinstance(result, pd.Series)
        assert not result.empty
        assert len(result) > len(self.temperature_data)
        
    def test_interpolate_to_5min_spline_success(self):
        """
        Testuoja spline interpoliaciją
        """
        result = self.interpolator.interpolate_to_5min('spline')
        
        assert isinstance(result, pd.Series)
        assert not result.empty
        assert len(result) > len(self.temperature_data)
        
    def test_interpolate_invalid_method(self):
        """
        Testuoja interpoliaciją su neteisingų metodu
        """
        result = self.interpolator.interpolate_to_5min('invalid_method')
        assert result is None
        
    def test_interpolate_no_data(self):
        """
        Testuoja interpoliaciją be duomenų
        """
        interpolator = TemperatureInterpolator()
        result = interpolator.interpolate_to_5min('linear')
        assert result is None
        
    def test_interpolate_insufficient_data(self):
        """
        Testuoja interpoliaciją su nepakankamais duomenimis
        """
        # Sukuriame duomenis tik su vienu tašku
        single_point = pd.Series([5.0], 
                               index=[datetime(2024, 1, 1, 12, 0, 0)], 
                               name='temperatura')
        
        interpolator = TemperatureInterpolator(single_point)
        result = interpolator.interpolate_to_5min('linear')
        assert result is None
        
    def test_interpolate_with_nan_values(self):
        """
        Testuoja interpoliaciją su NaN reikšmėmis
        """
        # Pridedame NaN reikšmių
        data_with_nan = self.temperature_data.copy()
        data_with_nan.iloc[2] = np.nan
        data_with_nan.iloc[5] = np.nan
        
        interpolator = TemperatureInterpolator(data_with_nan)
        result = interpolator.interpolate_to_5min('linear')
        
        assert isinstance(result, pd.Series)
        assert not result.empty
        assert not result.isnull().any()  # Interpoliuoti duomenys neturėtų turėti NaN
        
    def test_compare_methods_success(self):
        """
        Testuoja metodų palyginimą
        """
        comparison = self.interpolator.compare_methods()
        
        assert isinstance(comparison, dict)
        assert 'originalūs_duomenys' in comparison
        assert 'metodų_palyginimas' in comparison
        
        # Patikriname ar visi metodai buvo testuoti
        methods_results = comparison['metodų_palyginimas']
        for method in self.interpolator.interpolation_methods:
            assert method in methods_results
            
            if 'klaida' not in methods_results[method]:
                assert 'taškų_skaičius' in methods_results[method]
                assert 'interpoliacijos_laikas_s' in methods_results[method]
                assert 'kokybės_metrikos' in methods_results[method]
                
    def test_compare_methods_specific_list(self):
        """
        Testuoja metodų palyginimą su konkrečiu metodų sąrašu
        """
        methods_to_test = ['linear', 'time']
        comparison = self.interpolator.compare_methods(methods_to_test)
        
        assert isinstance(comparison, dict)
        methods_results = comparison['metodų_palyginimas']
        
        for method in methods_to_test:
            assert method in methods_results
            
    def test_calculate_quality_metrics(self):
        """
        Testuoja kokybės metrikų skaičiavimą
        """
        interpolated = self.interpolator.interpolate_to_5min('linear')
        metrics = self.interpolator._calculate_quality_metrics(interpolated)
        
        assert isinstance(metrics, dict)
        
        expected_metrics = ['vidurkis', 'standartinis_nuokrypis', 'minimumas', 
                          'maksimumas', 'vidutinis_gradientas', 'maksimalus_gradientas',
                          'tankumo_koeficientas']
        
        for metric in expected_metrics:
            if metric in metrics:
                assert isinstance(metrics[metric], (int, float))
                assert not np.isnan(metrics[metric])
                
    def test_validate_interpolation_success(self):
        """
        Testuoja interpoliacijos validavimą
        """
        validation = self.interpolator.validate_interpolation(test_ratio=0.2)
        
        assert isinstance(validation, dict)
        assert 'train_duomenų_skaičius' in validation
        assert 'test_duomenų_skaičius' in validation
        assert 'metodų_validacija' in validation
        
        # Patikriname ar yra validacijos metrikos
        method_validations = validation['metodų_validacija']
        for method, results in method_validations.items():
            if 'klaida' not in results:
                expected_metrics = ['vidutinė_absoliuti_klaida', 'šaknies_kvadratinė_klaida', 
                                  'maksimali_klaida', 'testuotų_taškų_skaičius']
                
                for metric in expected_metrics:
                    assert metric in results
                    if metric != 'testuotų_taškų_skaičius':
                        assert isinstance(results[metric], (int, float))
                        assert results[metric] >= 0  # Klaidos negali būti neigiamos
                        
    def test_validate_interpolation_small_dataset(self):
        """
        Testuoja validavimą su mažu duomenų rinkiniu
        """
        # Sukuriame mažą duomenų rinkinį
        small_dates = pd.date_range('2024-01-01', periods=5, freq='H', tz='Europe/Vilnius')
        small_temps = pd.Series(range(5), index=small_dates, name='temperatura')
        
        interpolator = TemperatureInterpolator(small_temps)
        validation = interpolator.validate_interpolation(test_ratio=0.2)
        
        assert isinstance(validation, dict)
        assert validation['test_duomenų_skaičius'] >= 1
        
    def test_export_interpolated_data_csv(self):
        """
        Testuoja duomenų eksportavimą CSV formatu
        """
        # Pirmiau interpoliuojame
        self.interpolator.interpolate_to_5min('linear')
        
        test_filepath = 'test_export.csv'
        
        try:
            success = self.interpolator.export_interpolated_data(test_filepath, 'csv')
            
            assert success is True
            assert os.path.exists(test_filepath)
            
            # Patikriname ar galime nuskaityti atgal
            imported_data = pd.read_csv(test_filepath, index_col=0, parse_dates=True)
            assert not imported_data.empty
            
        finally:
            # Išvalome test failą
            if os.path.exists(test_filepath):
                os.remove(test_filepath)
                
    def test_export_interpolated_data_json(self):
        """
        Testuoja duomenų eksportavimą JSON formatu
        """
        self.interpolator.interpolate_to_5min('linear')
        
        test_filepath = 'test_export.json'
        
        try:
            success = self.interpolator.export_interpolated_data(test_filepath, 'json')
            
            assert success is True
            assert os.path.exists(test_filepath)
            
        finally:
            if os.path.exists(test_filepath):
                os.remove(test_filepath)
                
    def test_export_no_interpolated_data(self):
        """
        Testuoja eksportavimą be interpoliuotų duomenų
        """
        interpolator = TemperatureInterpolator(self.temperature_data)
        # Nedarome interpoliacijos
        
        success = interpolator.export_interpolated_data('test.csv', 'csv')
        assert success is False
        
    def test_export_unsupported_format(self):
        """
        Testuoja eksportavimą su nepalaikoma formatu
        """
        self.interpolator.interpolate_to_5min('linear')
        
        success = self.interpolator.export_interpolated_data('test.xyz', 'xyz')
        assert success is False
        
    def test_interpolation_preserves_trends(self):
        """
        Testuoja ar interpoliacija išlaiko duomenų tendencijas
        """
        # Sukuriame duomenis su aiškiu trendu
        dates = pd.date_range('2024-01-01', periods=10, freq='H', tz='Europe/Vilnius')
        trend_temps = pd.Series(range(0, 20, 2), index=dates, name='temperatura')  # Linijinis augimas
        
        interpolator = TemperatureInterpolator(trend_temps)
        interpolated = interpolator.interpolate_to_5min('linear')
        
        # Patikriname ar tendencija išliko (duomenys auga)
        assert interpolated.iloc[-1] > interpolated.iloc[0]
        
        # Patikriname ar nėra didelių šuolių
        diffs = interpolated.diff().dropna()
        max_diff = diffs.abs().max()
        
        # Maksimalus skirtumas neturi būti per didelis lyginant su originaliaisiais duomenis
        original_max_diff = trend_temps.diff().abs().max()
        assert max_diff <= original_max_diff * 2  # Leistinas 2x padidėjimas
        
    def test_different_polynomial_orders(self):
        """
        Testuoja skirtingas polinomo eiles
        """
        orders = [1, 2, 3]
        
        for order in orders:
            result = self.interpolator.interpolate_to_5min('polynomial', polynomial_order=order)
            assert isinstance(result, pd.Series)
            assert not result.empty
            
    def test_interpolation_time_range_preservation(self):
        """
        Testuoja ar interpoliacija išlaiko laiko diapazoną
        """
        original_start = self.temperature_data.index.min()
        original_end = self.temperature_data.index.max()
        
        interpolated = self.interpolator.interpolate_to_5min('linear')
        
        interpolated_start = interpolated.index.min()
        interpolated_end = interpolated.index.max()
        
        # Interpoliuoti duomenys turėtų būti tame pačiame laiko diapazone
        assert interpolated_start == original_start
        assert interpolated_end == original_end
        
    def test_interpolation_methods_list(self):
        """
        Testuoja interpoliacijos metodų sąrašą
        """
        expected_methods = ['linear', 'time', 'polynomial', 'spline']
        assert self.interpolator.interpolation_methods == expected_methods
        
    @pytest.mark.parametrize("method", ['linear', 'time', 'polynomial', 'spline'])
    def test_all_interpolation_methods(self, method):
        """
        Parametrizuotas testas visiems interpoliacijos metodams
        """
        result = self.interpolator.interpolate_to_5min(method)
        
        assert isinstance(result, pd.Series)
        assert not result.empty
        assert len(result) > len(self.temperature_data)
        assert result.name == 'temperatura'
        
    def test_interpolation_with_extreme_values(self):
        """
        Testuoja interpoliaciją su ekstremaliomis reikšmėmis
        """
        # Sukuriame duomenis su dideliais temperatūros svyravimais
        dates = pd.date_range('2024-01-01', periods=5, freq='2H', tz='Europe/Vilnius')
        extreme_temps = pd.Series([-30, 40, -25, 35, -20], index=dates, name='temperatura')
        
        interpolator = TemperatureInterpolator(extreme_temps)
        result = interpolator.interpolate_to_5min('linear')
        
        assert isinstance(result, pd.Series)
        assert not result.empty
        
        # Patikriname ar interpoliuotos reikšmės yra tarp originalių ekstremumai
        assert result.min() >= extreme_temps.min()
        assert result.max() <= extreme_temps.max()
        
    def test_memory_efficiency_large_dataset(self):
        """
        Testuoja atminties efektyvumą su dideliu duomenų rinkiniu
        """
        # Sukuriame didesnį duomenų rinkinį (savaitė kas 15 min)
        large_dates = pd.date_range('2024-01-01', '2024-01-08', freq='15min', tz='Europe/Vilnius')
        large_temps = pd.Series(np.random.normal(5, 10, len(large_dates)), 
                              index=large_dates, name='temperatura')
        
        interpolator = TemperatureInterpolator(large_temps)
        
        # Matuojame interpoliacijos laiką
        import time
        start = time.time()
        result = interpolator.interpolate_to_5min('linear')
        end = time.time()
        
        assert isinstance(result, pd.Series)
        assert (end - start) < 10  # Neturi užtrukti ilgiau nei 10 sekundžių
        
    def test_interpolation_data_integrity(self):
        """
        Testuoja duomenų vientisumo išlaikymą po interpoliacijos
        """
        original_mean = self.temperature_data.mean()
        
        interpolated = self.interpolator.interpolate_to_5min('linear')
        interpolated_mean = interpolated.mean()
        
        # Vidurkiai neturėtų labai skirtis (tolerancija 10%)
        assert abs(interpolated_mean - original_mean) / abs(original_mean) < 0.1