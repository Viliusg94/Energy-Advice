"""
Temperatūros interpoliacijos funkcijos
"""

import pandas as pd
import numpy as np
from typing import Optional, Union
import logging

logger = logging.getLogger(__name__)

class TemperatureInterpolator:
    """
    Klasė temperatūros duomenų interpoliacijai
    """
    
    def __init__(self):
        """
        Inicializuoja interpoliacijos klasę
        """
        self.supported_methods = ['linear', 'time', 'polynomial', 'spline']
    
    def interpolate_temperature(self, temperature_series: pd.Series, 
                              target_frequency: str = '5T',
                              method: str = 'linear') -> Optional[pd.Series]:
        """
        Interpoliuoja temperatūros duomenis iki nurodyto dažnio
        
        Args:
            temperature_series (pd.Series): Temperatūros duomenų serija
            target_frequency (str): Tikslo dažnis (default: '5T' = 5 minutės)
            method (str): Interpoliacijos metodas (default: 'linear')
            
        Returns:
            Optional[pd.Series]: Interpoliuoti duomenys arba None jei klaida
        """
        try:
            if temperature_series.empty:
                logger.warning("Tuščia temperatūros serija interpoliacijai")
                return None
            
            if method not in self.supported_methods:
                logger.warning(f"Nepalaikomas interpoliacijos metodas: {method}. Naudojamas 'linear'")
                method = 'linear'
            
            # Tikrinome ar serija turi datetime indeksą
            if not isinstance(temperature_series.index, pd.DatetimeIndex):
                logger.error("Temperatūros serija turi turėti datetime indeksą")
                return None
            
            # Pašaliname NaN reikšmes
            clean_series = temperature_series.dropna()
            
            if clean_series.empty:
                logger.warning("Po NaN pašalinimo nebeliko duomenų")
                return None
            
            # Sukuriame naują indeksą su reikiamu dažniu
            start_time = clean_series.index.min()
            end_time = clean_series.index.max()
            
            new_index = pd.date_range(start=start_time, end=end_time, freq=target_frequency)
            
            # Persampliuojame į naują indeksą
            resampled = clean_series.reindex(new_index)
            
            # Interpoliuojame trūkstamas reikšmes
            if method == 'linear':
                interpolated = resampled.interpolate(method='linear')
            elif method == 'time':
                interpolated = resampled.interpolate(method='time')
            elif method == 'polynomial':
                interpolated = resampled.interpolate(method='polynomial', order=2)
            elif method == 'spline':
                interpolated = resampled.interpolate(method='spline', order=3)
            else:
                interpolated = resampled.interpolate(method='linear')
            
            # Pašaliname likusius NaN (gali būti pradžioje ar pabaigoje)
            interpolated = interpolated.dropna()
            
            logger.info(f"Sėkmingai interpoliuoti duomenys: {len(clean_series)} -> {len(interpolated)} taškai")
            logger.info(f"Interpoliacijos metodas: {method}, dažnis: {target_frequency}")
            
            return interpolated
            
        except Exception as e:
            logger.error(f"Klaida interpoliuojant temperatūros duomenis: {e}")
            return None
    
    def interpolate_with_statistics(self, temperature_series: pd.Series,
                                  target_frequency: str = '5T',
                                  method: str = 'linear') -> dict:
        """
        Interpoliuoja duomenis ir grąžina statistiką
        
        Args:
            temperature_series (pd.Series): Temperatūros duomenų serija
            target_frequency (str): Tikslo dažnis
            method (str): Interpoliacijos metodas
            
        Returns:
            dict: Interpoliuoti duomenys ir statistika
        """
        try:
            original_count = len(temperature_series.dropna())
            
            interpolated = self.interpolate_temperature(temperature_series, target_frequency, method)
            
            if interpolated is None:
                return {
                    'interpolated_data': None,
                    'original_points': original_count,
                    'interpolated_points': 0,
                    'improvement_ratio': 0,
                    'method': method,
                    'frequency': target_frequency
                }
            
            interpolated_count = len(interpolated)
            improvement_ratio = interpolated_count / original_count if original_count > 0 else 0
            
            statistics = {
                'interpolated_data': interpolated,
                'original_points': original_count,
                'interpolated_points': interpolated_count,
                'improvement_ratio': improvement_ratio,
                'method': method,
                'frequency': target_frequency,
                'original_min': temperature_series.min(),
                'original_max': temperature_series.max(),
                'original_mean': temperature_series.mean(),
                'interpolated_min': interpolated.min(),
                'interpolated_max': interpolated.max(),
                'interpolated_mean': interpolated.mean()
            }
            
            logger.info(f"Interpoliacijos statistika: {original_count} -> {interpolated_count} taškai")
            return statistics
            
        except Exception as e:
            logger.error(f"Klaida skaičiuojant interpoliacijos statistiką: {e}")
            return {
                'interpolated_data': None,
                'original_points': 0,
                'interpolated_points': 0,
                'improvement_ratio': 0,
                'method': method,
                'frequency': target_frequency
            }
    
    def compare_interpolation_methods(self, temperature_series: pd.Series,
                                    target_frequency: str = '5T') -> dict:
        """
        Palygina skirtingus interpoliacijos metodus
        
        Args:
            temperature_series (pd.Series): Temperatūros duomenų serija
            target_frequency (str): Tikslo dažnis
            
        Returns:
            dict: Palyginimo rezultatai
        """
        try:
            results = {}
            
            for method in self.supported_methods:
                logger.info(f"Testuojamas interpoliacijos metodas: {method}")
                result = self.interpolate_with_statistics(temperature_series, target_frequency, method)
                results[method] = result
            
            # Pažymime geriausią metodą (pagal R² arba kitą metriką)
            best_method = 'linear'  # Default
            
            logger.info("Interpoliacijos metodų palyginimas baigtas")
            return {
                'methods': results,
                'recommended_method': best_method
            }
            
        except Exception as e:
            logger.error(f"Klaida lyginant interpoliacijos metodus: {e}")
            return {}
    
    def validate_interpolation(self, original: pd.Series, interpolated: pd.Series) -> dict:
        """
        Validuoja interpoliacijos kokybę
        
        Args:
            original (pd.Series): Originalūs duomenys
            interpolated (pd.Series): Interpoliuoti duomenys
            
        Returns:
            dict: Validacijos rezultatai
        """
        try:
            if original.empty or interpolated.empty:
                return {'valid': False, 'reason': 'Tuščios serijos'}
            
            # Patikrinome temperatūros diapazoną
            orig_min, orig_max = original.min(), original.max()
            interp_min, interp_max = interpolated.min(), interpolated.max()
            
            # Tolerancija - 20% nuo originalaus diapazono
            tolerance = (orig_max - orig_min) * 0.2
            
            valid_range = (interp_min >= orig_min - tolerance and 
                          interp_max <= orig_max + tolerance)
            
            # Patikrinime vidurkių skirtumą
            mean_diff = abs(original.mean() - interpolated.mean())
            valid_mean = mean_diff <= tolerance
            
            # Bendras validumas
            is_valid = valid_range and valid_mean
            
            validation_result = {
                'valid': is_valid,
                'valid_range': valid_range,
                'valid_mean': valid_mean,
                'original_range': (orig_min, orig_max),
                'interpolated_range': (interp_min, interp_max),
                'mean_difference': mean_diff,
                'tolerance': tolerance
            }
            
            logger.info(f"Interpoliacijos validacija: {'SĖKMINGA' if is_valid else 'NESĖKMINGA'}")
            return validation_result
            
        except Exception as e:
            logger.error(f"Klaida validuojant interpoliaciją: {e}")
            return {'valid': False, 'reason': f'Klaida: {e}'}
    
    def print_interpolation_summary(self, statistics: dict):
        """
        Išspausdina interpoliacijos suvestinę
        
        Args:
            statistics (dict): Interpoliacijos statistika
        """
        print("=" * 50)
        print("TEMPERATŪROS INTERPOLIACIJOS SUVESTINĖ")
        print("=" * 50)
        
        if not statistics or statistics.get('interpolated_data') is None:
            print("Interpoliacija nepavyko arba nėra duomenų")
            return
        
        print(f"Metodas: {statistics.get('method', 'Nežinomas')}")
        print(f"Dažnis: {statistics.get('frequency', 'Nežinomas')}")
        print(f"Originalūs taškai: {statistics.get('original_points', 0)}")
        print(f"Interpoliuoti taškai: {statistics.get('interpolated_points', 0)}")
        print(f"Pagerėjimo santykis: {statistics.get('improvement_ratio', 0):.2f}x")
        
        if 'original_mean' in statistics:
            print(f"\nOriginalūs duomenys:")
            print(f"  Vidurkis: {statistics['original_mean']:.2f}°C")
            print(f"  Min: {statistics['original_min']:.2f}°C")
            print(f"  Max: {statistics['original_max']:.2f}°C")
            
        if 'interpolated_mean' in statistics:
            print(f"\nInterpoliuoti duomenys:")
            print(f"  Vidurkis: {statistics['interpolated_mean']:.2f}°C")
            print(f"  Min: {statistics['interpolated_min']:.2f}°C")
            print(f"  Max: {statistics['interpolated_max']:.2f}°C")
        
        print("=" * 50)
