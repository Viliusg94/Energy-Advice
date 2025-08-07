# -*- coding: utf-8 -*-
"""
Oro duomenų analizės modulis
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class WeatherAnalyzer:
    """
    Klasė oro duomenų analizei ir statistinių skaičiavimų atlikimui
    """
    
    def __init__(self, historical_data: Optional[pd.DataFrame] = None, 
                 forecast_data: Optional[pd.DataFrame] = None):
        """
        Inicializuoja WeatherAnalyzer objektą
        
        Args:
            historical_data (pd.DataFrame, optional): Istoriniai oro duomenys
            forecast_data (pd.DataFrame, optional): Prognozės duomenys
        """
        self.historical_data = historical_data
        self.forecast_data = forecast_data
        self.combined_data = None
        
        if historical_data is not None and forecast_data is not None:
            self.combine_data()
            
    def combine_data(self) -> pd.DataFrame:
        """
        Sujungia istorinius ir prognozės duomenis
        
        Returns:
            pd.DataFrame: Sujungti duomenys
        """
        try:
            if self.historical_data is None or self.forecast_data is None:
                logger.warning("Trūksta duomenų sujungimui")
                return pd.DataFrame()
                
            # Užtikriname, kad stulpeliai sutampa
            common_columns = list(set(self.historical_data.columns) & 
                                set(self.forecast_data.columns))
            
            if not common_columns:
                logger.error("Nėra bendrų stulpelių tarp istorinių ir prognozės duomenų")
                return pd.DataFrame()
                
            hist_subset = self.historical_data[common_columns]
            forecast_subset = self.forecast_data[common_columns]
            
            # Pridedame duomenų tipo žymę
            hist_subset = hist_subset.copy()
            forecast_subset = forecast_subset.copy()
            hist_subset['duomenu_tipas'] = 'istoriniai'
            forecast_subset['duomenu_tipas'] = 'prognozė'
            
            # Sujungiame duomenis
            self.combined_data = pd.concat([hist_subset, forecast_subset], 
                                         sort=False)
            self.combined_data.sort_index(inplace=True)
            
            logger.info(f"Sujungti duomenys: {len(self.combined_data)} įrašų")
            return self.combined_data
            
        except Exception as e:
            logger.error(f"Klaida sujungiant duomenis: {e}")
            return pd.DataFrame()
            
    def calculate_yearly_averages(self) -> Dict[str, float]:
        """
        Apskaičiuoja metinius vidurkius
        
        Returns:
            Dict: Metinių vidurkių žodynas
        """
        try:
            if self.historical_data is None or self.historical_data.empty:
                logger.error("Nėra istorinių duomenų metinių vidurkių skaičiavimui")
                return {}
                
            # Filtruojame paskutiniųjų 365 dienų duomenis
            end_date = self.historical_data.index.max()
            start_date = end_date - timedelta(days=365)
            yearly_data = self.historical_data[
                self.historical_data.index >= start_date
            ]
            
            if yearly_data.empty:
                logger.warning("Nėra duomenų paskutiniesiems 365 dienoms")
                return {}
                
            results = {}
            
            # Apskaičiuojame vidurkius
            if 'temperatura' in yearly_data.columns:
                avg_temp = yearly_data['temperatura'].mean()
                results['vidutinė_metų_temperatūra'] = round(avg_temp, 2)
                
            if 'dregme' in yearly_data.columns:
                avg_humidity = yearly_data['dregme'].mean()
                results['vidutinė_metų_drėgmė'] = round(avg_humidity, 2)
                
            if 'vejo_greitis' in yearly_data.columns:
                avg_wind = yearly_data['vejo_greitis'].mean()
                results['vidutinis_vėjo_greitis'] = round(avg_wind, 2)
                
            if 'slegimasJuros' in yearly_data.columns:
                avg_pressure = yearly_data['slegimasJuros'].mean()
                results['vidutinis_slėgimas'] = round(avg_pressure, 2)
                
            logger.info(f"Apskaičiuoti metiniai vidurkiai: {len(results)} parametrų")
            return results
            
        except Exception as e:
            logger.error(f"Klaida skaičiuojant metinius vidurkius: {e}")
            return {}
            
    def analyze_day_night_temperature(self) -> Dict[str, float]:
        """
        Analizuoja dienos ir nakties temperatūros skirtumus
        
        Returns:
            Dict: Dienos ir nakties temperatūrų analizė
        """
        try:
            if self.historical_data is None or self.historical_data.empty:
                logger.error("Nėra duomenų dienos/nakties analizei")
                return {}
                
            if 'temperatura' not in self.historical_data.columns:
                logger.error("Nėra temperatūros duomenų")
                return {}
                
            # Išskiriame valandas
            df_with_hours = self.historical_data.copy()
            df_with_hours['valanda'] = df_with_hours.index.hour
            
            # Dienos laikas: 8:00-20:00
            day_mask = (df_with_hours['valanda'] >= 8) & (df_with_hours['valanda'] < 20)
            night_mask = ~day_mask
            
            day_temp = df_with_hours[day_mask]['temperatura']
            night_temp = df_with_hours[night_mask]['temperatura']
            
            results = {}
            
            if not day_temp.empty:
                results['vidutinė_dienos_temperatūra'] = round(day_temp.mean(), 2)
                results['maksimali_dienos_temperatūra'] = round(day_temp.max(), 2)
                results['minimali_dienos_temperatūra'] = round(day_temp.min(), 2)
                
            if not night_temp.empty:
                results['vidutinė_nakties_temperatūra'] = round(night_temp.mean(), 2)
                results['maksimali_nakties_temperatūra'] = round(night_temp.max(), 2)
                results['minimali_nakties_temperatūra'] = round(night_temp.min(), 2)
                
            if 'vidutinė_dienos_temperatūra' in results and 'vidutinė_nakties_temperatūra' in results:
                temp_diff = results['vidutinė_dienos_temperatūra'] - results['vidutinė_nakties_temperatūra']
                results['dienos_nakties_skirtumas'] = round(temp_diff, 2)
                
            logger.info("Atlikta dienos/nakties temperatūros analizė")
            return results
            
        except Exception as e:
            logger.error(f"Klaida analizuojant dienos/nakties temperatūrą: {e}")
            return {}
            
    def analyze_weekend_rain_forecast(self) -> Dict[str, Any]:
        """
        Analizuoja savaitgalių lietaus prognozes
        
        Returns:
            Dict: Savaitgalių lietaus prognozės analizė
        """
        try:
            if self.forecast_data is None or self.forecast_data.empty:
                logger.error("Nėra prognozės duomenų savaitgalių analizei")
                return {}
                
            if 'krituliai' not in self.forecast_data.columns:
                logger.error("Nėra kritulių duomenų prognozėse")
                return {}
                
            # Išskiriame savaitgalius (šeštadienis=5, sekmadienis=6)
            df_weekends = self.forecast_data[
                self.forecast_data.index.dayofweek.isin([5, 6])
            ].copy()
            
            if df_weekends.empty:
                logger.warning("Nėra savaitgalių duomenų prognozėse")
                return {'savaitgalių_skaičius': 0}
                
            # Suskaidome pagal savaitgalius
            df_weekends['savaitgalio_data'] = df_weekends.index.date
            weekend_groups = df_weekends.groupby('savaitgalio_data')
            
            total_weekends = len(weekend_groups)
            rainy_weekends = 0
            weekend_details = []
            
            for date, group in weekend_groups:
                # Tikrinome ar yra lietaus (krituliai > 0)
                has_rain = (group['krituliai'] > 0).any()
                if has_rain:
                    rainy_weekends += 1
                    
                avg_precipitation = group['krituliai'].mean()
                weekend_details.append({
                    'data': str(date),
                    'lietaus_prognozė': has_rain,
                    'vidutiniai_krituliai': round(avg_precipitation, 2)
                })
                
            rain_percentage = (rainy_weekends / total_weekends * 100) if total_weekends > 0 else 0
            
            results = {
                'savaitgalių_skaičius': total_weekends,
                'savaitgaliai_su_lietumi': rainy_weekends,
                'lietaus_tikimybė_procentais': round(rain_percentage, 1),
                'savaitgalių_detalizacija': weekend_details
            }
            
            logger.info(f"Analizuoti {total_weekends} savaitgaliai, {rainy_weekends} su lietumi")
            return results
            
        except Exception as e:
            logger.error(f"Klaida analizuojant savaitgalių prognozes: {e}")
            return {}
            
    def calculate_correlations(self) -> Optional[pd.DataFrame]:
        """
        Apskaičiuoja oro parametrų koreliacijas
        
        Returns:
            pd.DataFrame: Koreliacijos matrica
        """
        try:
            data_to_analyze = self.combined_data if self.combined_data is not None else self.historical_data
            
            if data_to_analyze is None or data_to_analyze.empty:
                logger.error("Nėra duomenų koreliacijos analizei")
                return None
                
            # Išrenkame tik skaičiuojamuosius stulpelius
            numeric_columns = data_to_analyze.select_dtypes(include=[np.number]).columns
            
            if len(numeric_columns) < 2:
                logger.warning("Nepakanka skaitinių stulpelių koreliacijos analizei")
                return None
                
            correlation_matrix = data_to_analyze[numeric_columns].corr()
            
            logger.info(f"Apskaičiuotos koreliacijos {len(numeric_columns)} parametrų")
            return correlation_matrix
            
        except Exception as e:
            logger.error(f"Klaida skaičiuojant koreliacijas: {e}")
            return None
            
    def find_extremes(self) -> Dict[str, Any]:
        """
        Suranda ekstremaliuosius oro rodiklius
        
        Returns:
            Dict: Ekstremaliųjų reikšmių žodynas
        """
        try:
            data_to_analyze = self.combined_data if self.combined_data is not None else self.historical_data
            
            if data_to_analyze is None or data_to_analyze.empty:
                logger.error("Nėra duomenų ekstremumų paieškai")
                return {}
                
            results = {}
            
            # Temperatūros ekstremumas
            if 'temperatura' in data_to_analyze.columns:
                temp_max_idx = data_to_analyze['temperatura'].idxmax()
                temp_min_idx = data_to_analyze['temperatura'].idxmin()
                
                results['aukščiausia_temperatūra'] = {
                    'reikšmė': round(data_to_analyze.loc[temp_max_idx, 'temperatura'], 2),
                    'data': str(temp_max_idx)
                }
                results['žemiausia_temperatūra'] = {
                    'reikšmė': round(data_to_analyze.loc[temp_min_idx, 'temperatura'], 2),
                    'data': str(temp_min_idx)
                }
                
            # Vėjo greičio ekstremumas
            if 'vejo_greitis' in data_to_analyze.columns:
                wind_max_idx = data_to_analyze['vejo_greitis'].idxmax()
                results['didžiausias_vėjo_greitis'] = {
                    'reikšmė': round(data_to_analyze.loc[wind_max_idx, 'vejo_greitis'], 2),
                    'data': str(wind_max_idx)
                }
                
            # Slėgimo ekstremumas
            if 'slegimasJuros' in data_to_analyze.columns:
                pressure_max_idx = data_to_analyze['slegimasJuros'].idxmax()
                pressure_min_idx = data_to_analyze['slegimasJuros'].idxmin()
                
                results['aukščiausias_slėgimas'] = {
                    'reikšmė': round(data_to_analyze.loc[pressure_max_idx, 'slegimasJuros'], 2),
                    'data': str(pressure_max_idx)
                }
                results['žemiausias_slėgimas'] = {
                    'reikšmė': round(data_to_analyze.loc[pressure_min_idx, 'slegimasJuros'], 2),
                    'data': str(pressure_min_idx)
                }
                
            logger.info(f"Rasti ekstremumų: {len(results)} parametrų")
            return results
            
        except Exception as e:
            logger.error(f"Klaida ieškant ekstremumų: {e}")
            return {}
            
    def generate_summary_report(self) -> Dict[str, Any]:
        """
        Generuoja išsamią duomenų analizės ataskaitą
        
        Returns:
            Dict: Ataskaitos žodynas
        """
        try:
            report = {
                'analizės_data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'duomenų_kiekis': {}
            }
            
            # Duomenų kiekio informacija
            if self.historical_data is not None:
                report['duomenų_kiekis']['istoriniai'] = len(self.historical_data)
                
            if self.forecast_data is not None:
                report['duomenų_kiekis']['prognozės'] = len(self.forecast_data)
                
            if self.combined_data is not None:
                report['duomenų_kiekis']['bendras'] = len(self.combined_data)
                
            # Pridedame analizės rezultatus
            report['metiniai_vidurkiai'] = self.calculate_yearly_averages()
            report['dienos_nakties_analizė'] = self.analyze_day_night_temperature()
            report['savaitgalių_lietaus_prognozė'] = self.analyze_weekend_rain_forecast()
            report['ekstremaliuosius_rodikliai'] = self.find_extremes()
            
            logger.info("Sugeneruota išsami analizės ataskaita")
            return report
            
        except Exception as e:
            logger.error(f"Klaida generuojant ataskaitą: {e}")
            return {}