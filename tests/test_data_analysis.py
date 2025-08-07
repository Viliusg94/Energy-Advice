# -*- coding: utf-8 -*-
"""
WeatherAnalyzer klasės unit testai
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Pridedame src katalogą į Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_analysis import WeatherAnalyzer


class TestWeatherAnalyzer:
    """
    WeatherAnalyzer klasės testai
    """
    
    def setup_method(self):
        """
        Pradinis testų nustatymas
        """
        # Sukuriame test duomenis
        dates = pd.date_range('2024-01-01', '2024-01-30', freq='H', tz='Europe/Vilnius')
        
        # Istoriniai duomenys
        np.random.seed(42)
        self.historical_data = pd.DataFrame({
            'temperatura': np.random.normal(5, 10, len(dates)),
            'dregme': np.random.uniform(40, 90, len(dates)),
            'vejo_greitis': np.random.uniform(0, 15, len(dates)),
            'slegimasJuros': np.random.normal(1013, 20, len(dates)),
            'krituliai': np.random.exponential(0.5, len(dates))
        }, index=dates)
        
        # Prognozės duomenys (mažesnė dalis)
        forecast_dates = pd.date_range('2024-01-31', '2024-02-07', freq='3H', tz='Europe/Vilnius')
        self.forecast_data = pd.DataFrame({
            'temperatura': np.random.normal(7, 8, len(forecast_dates)),
            'dregme': np.random.uniform(50, 85, len(forecast_dates)),
            'vejo_greitis': np.random.uniform(1, 12, len(forecast_dates)),
            'slegimasJuros': np.random.normal(1015, 15, len(forecast_dates)),
            'krituliai': np.random.exponential(0.3, len(forecast_dates))
        }, index=forecast_dates)
        
        self.analyzer = WeatherAnalyzer(self.historical_data, self.forecast_data)
        
    def test_init_with_data(self):
        """
        Testuoja objekto inicializavimą su duomenimis
        """
        analyzer = WeatherAnalyzer(self.historical_data, self.forecast_data)
        
        assert analyzer.historical_data is not None
        assert analyzer.forecast_data is not None
        assert analyzer.combined_data is not None
        
    def test_init_without_data(self):
        """
        Testuoja objekto inicializavimą be duomenų
        """
        analyzer = WeatherAnalyzer()
        
        assert analyzer.historical_data is None
        assert analyzer.forecast_data is None
        assert analyzer.combined_data is None
        
    def test_combine_data_success(self):
        """
        Testuoja duomenų sujungimą
        """
        combined = self.analyzer.combine_data()
        
        assert isinstance(combined, pd.DataFrame)
        assert not combined.empty
        assert 'duomenu_tipas' in combined.columns
        assert 'istoriniai' in combined['duomenu_tipas'].values
        assert 'prognozė' in combined['duomenu_tipas'].values
        
    def test_combine_data_no_common_columns(self):
        """
        Testuoja duomenų sujungimą be bendrų stulpelių
        """
        # Sukuriame duomenis be bendrų stulpelių
        hist_data = pd.DataFrame({'col1': [1, 2, 3]}, 
                                index=pd.date_range('2024-01-01', periods=3, freq='D'))
        forecast_data = pd.DataFrame({'col2': [4, 5, 6]}, 
                                   index=pd.date_range('2024-01-04', periods=3, freq='D'))
        
        analyzer = WeatherAnalyzer(hist_data, forecast_data)
        result = analyzer.combine_data()
        
        assert result.empty
        
    def test_calculate_yearly_averages_success(self):
        """
        Testuoja metinių vidurkių skaičiavimą
        """
        averages = self.analyzer.calculate_yearly_averages()
        
        assert isinstance(averages, dict)
        assert len(averages) > 0
        
        expected_keys = ['vidutinė_metų_temperatūra', 'vidutinė_metų_drėgmė', 
                        'vidutinis_vėjo_greitis', 'vidutinis_slėgimas']
        
        for key in expected_keys:
            if key in averages:
                assert isinstance(averages[key], (int, float))
                
    def test_calculate_yearly_averages_no_data(self):
        """
        Testuoja metinių vidurkių skaičiavimą be duomenų
        """
        analyzer = WeatherAnalyzer()
        averages = analyzer.calculate_yearly_averages()
        
        assert averages == {}
        
    def test_analyze_day_night_temperature_success(self):
        """
        Testuoja dienos/nakties temperatūros analizę
        """
        analysis = self.analyzer.analyze_day_night_temperature()
        
        assert isinstance(analysis, dict)
        
        expected_keys = ['vidutinė_dienos_temperatūra', 'vidutinė_nakties_temperatūra',
                        'maksimali_dienos_temperatūra', 'minimali_dienos_temperatūra',
                        'maksimali_nakties_temperatūra', 'minimali_nakties_temperatūra']
        
        for key in expected_keys:
            if key in analysis:
                assert isinstance(analysis[key], (int, float))
                
        # Patikriname ar yra temperatūros skirtumas
        if 'dienos_nakties_skirtumas' in analysis:
            assert isinstance(analysis['dienos_nakties_skirtumas'], (int, float))
            
    def test_analyze_day_night_temperature_no_temp_data(self):
        """
        Testuoja dienos/nakties analizę be temperatūros duomenų
        """
        # Sukuriame duomenis be temperatūros stulpelio
        data_no_temp = self.historical_data.drop('temperatura', axis=1)
        analyzer = WeatherAnalyzer(data_no_temp)
        
        result = analyzer.analyze_day_night_temperature()
        assert result == {}
        
    def test_analyze_weekend_rain_forecast_success(self):
        """
        Testuoja savaitgalių lietaus prognozės analizę
        """
        analysis = self.analyzer.analyze_weekend_rain_forecast()
        
        assert isinstance(analysis, dict)
        
        expected_keys = ['savaitgalių_skaičius', 'savaitgaliai_su_lietumi',
                        'lietaus_tikimybė_procentais', 'savaitgalių_detalizacija']
        
        for key in expected_keys:
            if key in analysis:
                if key == 'savaitgalių_detalizacija':
                    assert isinstance(analysis[key], list)
                else:
                    assert isinstance(analysis[key], (int, float))
                    
    def test_analyze_weekend_rain_forecast_no_forecast(self):
        """
        Testuoja savaitgalių analizę be prognozės duomenų
        """
        analyzer = WeatherAnalyzer(self.historical_data)
        result = analyzer.analyze_weekend_rain_forecast()
        
        assert result == {}
        
    def test_calculate_correlations_success(self):
        """
        Testuoja koreliacijos skaičiavimą
        """
        correlations = self.analyzer.calculate_correlations()
        
        assert isinstance(correlations, pd.DataFrame)
        assert not correlations.empty
        assert correlations.shape[0] == correlations.shape[1]  # Kvadratinė matrica
        
        # Patikrinome ar diagonale yra 1 (savikoreliacija)
        diagonal = np.diag(correlations.values)
        assert np.allclose(diagonal, 1.0, rtol=1e-10)
        
    def test_calculate_correlations_no_numeric_data(self):
        """
        Testuoja koreliacijos skaičiavimą be skaitinių duomenų
        """
        # Sukuriame duomenis tik su tekstiniais stulpeliais
        text_data = pd.DataFrame({
            'tekstas1': ['a', 'b', 'c'],
            'tekstas2': ['x', 'y', 'z']
        }, index=pd.date_range('2024-01-01', periods=3, freq='D'))
        
        analyzer = WeatherAnalyzer(text_data)
        result = analyzer.calculate_correlations()
        
        assert result is None
        
    def test_find_extremes_success(self):
        """
        Testuoja ekstremumų paieška
        """
        extremes = self.analyzer.find_extremes()
        
        assert isinstance(extremes, dict)
        
        possible_keys = ['aukščiausia_temperatūra', 'žemiausia_temperatūra',
                        'didžiausias_vėjo_greitis', 'aukščiausias_slėgimas',
                        'žemiausias_slėgimas']
        
        for key in possible_keys:
            if key in extremes:
                assert isinstance(extremes[key], dict)
                assert 'reikšmė' in extremes[key]
                assert 'data' in extremes[key]
                assert isinstance(extremes[key]['reikšmė'], (int, float))
                assert isinstance(extremes[key]['data'], str)
                
    def test_find_extremes_no_data(self):
        """
        Testuoja ekstremumų paiešką be duomenų
        """
        analyzer = WeatherAnalyzer()
        result = analyzer.find_extremes()
        
        assert result == {}
        
    def test_generate_summary_report_success(self):
        """
        Testuoja išsamios ataskaitos generavimą
        """
        report = self.analyzer.generate_summary_report()
        
        assert isinstance(report, dict)
        assert 'analizės_data' in report
        assert 'duomenų_kiekis' in report
        
        # Patikriname ar yra analizės sekcijos
        expected_sections = ['metiniai_vidurkiai', 'dienos_nakties_analizė',
                           'savaitgalių_lietaus_prognozė', 'ekstremaliuosius_rodikliai']
        
        for section in expected_sections:
            if section in report:
                assert isinstance(report[section], dict)
                
    def test_data_validation(self):
        """
        Testuoja duomenų validavimą
        """
        # Testuojame su NaN reikšmėmis
        data_with_nan = self.historical_data.copy()
        data_with_nan.loc[data_with_nan.index[0], 'temperatura'] = np.nan
        
        analyzer = WeatherAnalyzer(data_with_nan)
        averages = analyzer.calculate_yearly_averages()
        
        # Turėtų vis tiek grąžinti rezultatus, ignoruodamas NaN
        assert isinstance(averages, dict)
        
    def test_empty_dataframe_handling(self):
        """
        Testuoja tuščio DataFrame apdorojimą
        """
        empty_df = pd.DataFrame()
        analyzer = WeatherAnalyzer(empty_df, empty_df)
        
        result = analyzer.calculate_yearly_averages()
        assert result == {}
        
        result = analyzer.analyze_day_night_temperature()
        assert result == {}
        
    def test_weekend_identification(self):
        """
        Testuoja savaitgalių identifikavimą
        """
        # Sukuriame duomenis su žinomais savaitgaliais
        dates = pd.date_range('2024-01-06', '2024-01-14', freq='D', tz='Europe/Vilnius')  # Šeštadienis - sekmadienis
        test_forecast = pd.DataFrame({
            'krituliai': [1.0, 2.0, 0.0, 0.0, 0.0, 3.0, 1.5, 0.0, 0.0]  # Savaitgalio duomenys
        }, index=dates)
        
        analyzer = WeatherAnalyzer(forecast_data=test_forecast)
        result = analyzer.analyze_weekend_rain_forecast()
        
        assert 'savaitgalių_skaičius' in result
        assert result['savaitgalių_skaičius'] > 0
        
    @pytest.mark.parametrize("temp_values", [
        [10, 20, 30, 15, 25],
        [-5, 0, 5, -10, 2],
        [0.1, 0.2, 0.3, 0.4, 0.5]
    ])
    def test_temperature_analysis_different_ranges(self, temp_values):
        """
        Parametrizuotas testas skirtingiems temperatūros diapazonams
        """
        dates = pd.date_range('2024-01-01', periods=len(temp_values), freq='H', tz='Europe/Vilnius')
        test_data = pd.DataFrame({'temperatura': temp_values}, index=dates)
        
        analyzer = WeatherAnalyzer(test_data)
        result = analyzer.analyze_day_night_temperature()
        
        # Turėtų grąžinti rezultatus bet kokiam temperatūros diapazonui
        assert isinstance(result, dict)
        
    def test_data_types_consistency(self):
        """
        Testuoja duomenų tipų nuoseklumą
        """
        averages = self.analyzer.calculate_yearly_averages()
        
        # Visi skaitiniai rezultatai turi būti float
        for key, value in averages.items():
            assert isinstance(value, (int, float))
            if isinstance(value, float):
                assert not np.isnan(value)  # Neturi būti NaN
                
    def test_large_dataset_performance(self):
        """
        Testuoja didelių duomenų rinkinių apdorojimą
        """
        # Sukuriame didesnį duomenų rinkinį
        large_dates = pd.date_range('2023-01-01', '2024-01-01', freq='10min', tz='Europe/Vilnius')
        large_data = pd.DataFrame({
            'temperatura': np.random.normal(10, 15, len(large_dates)),
            'dregme': np.random.uniform(30, 95, len(large_dates)),
            'vejo_greitis': np.random.uniform(0, 20, len(large_dates)),
        }, index=large_dates)
        
        analyzer = WeatherAnalyzer(large_data)
        
        # Testuojame ar greitai apskaičiuoja
        import time
        start = time.time()
        averages = analyzer.calculate_yearly_averages()
        end = time.time()
        
        assert isinstance(averages, dict)
        assert (end - start) < 5  # Neturi užtrukti ilgiau nei 5 sekundės