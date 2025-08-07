# -*- coding: utf-8 -*-
"""
Temperatūros duomenų interpoliacijos modulis
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import interpolate
from typing import Optional, Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)


class TemperatureInterpolator:
    """
    Klasė temperatūros duomenų interpoliacijai
    """
    
    def __init__(self, temperature_data: Optional[pd.Series] = None):
        """
        Inicializuoja TemperatureInterpolator objektą
        
        Args:
            temperature_data (pd.Series, optional): Temperatūros duomenų seka
        """
        self.original_data = temperature_data
        self.interpolated_data = None
        self.interpolation_methods = [
            'linear', 'time', 'polynomial', 'spline'
        ]
        
    def interpolate_to_5min(self, method: str = 'linear', 
                          polynomial_order: int = 2) -> Optional[pd.Series]:
        """
        Interpoliuoja temperatūros duomenis iki 5 minučių dažnio
        
        Args:
            method (str): Interpoliacijos metodas
            polynomial_order (int): Polinomo eilė polynomial metodui
            
        Returns:
            pd.Series: Interpoliuoti duomenys arba None klaidos atveju
        """
        try:
            if self.original_data is None or self.original_data.empty:
                logger.error("Nėra duomenų interpoliacijai")
                return None
                
            if method not in self.interpolation_methods:
                logger.error(f"Nepalaikomas interpoliacijos metodas: {method}")
                return None
                
            # Pašaliname NaN reikšmes
            clean_data = self.original_data.dropna()
            
            if len(clean_data) < 2:
                logger.error("Nepakanka duomenų interpoliacijai (mažiau nei 2 taškai)")
                return None
                
            # Sukuriame 5 minučių dažnio laiko indeksą
            start_time = clean_data.index.min()
            end_time = clean_data.index.max()
            
            new_index = pd.date_range(
                start=start_time,
                end=end_time,
                freq='5min'
            )
            
            # Atliekame interpoliaciją pagal pasirinktą metodą
            if method == 'linear':
                result = self._linear_interpolation(clean_data, new_index)
            elif method == 'time':
                result = self._time_interpolation(clean_data, new_index)
            elif method == 'polynomial':
                result = self._polynomial_interpolation(clean_data, new_index, polynomial_order)
            elif method == 'spline':
                result = self._spline_interpolation(clean_data, new_index)
            else:
                logger.error(f"Nerealizuotas metodas: {method}")
                return None
                
            self.interpolated_data = result
            
            logger.info(f"Interpoliacija atlikta metodas '{method}': "
                       f"{len(clean_data)} -> {len(result)} taškų")
            return result
            
        except Exception as e:
            logger.error(f"Klaida interpoliuojant duomenis: {e}")
            return None
            
    def _linear_interpolation(self, data: pd.Series, new_index: pd.DatetimeIndex) -> pd.Series:
        """
        Atlieka tiesinę interpoliaciją
        
        Args:
            data (pd.Series): Originalūs duomenys
            new_index (pd.DatetimeIndex): Naujas laiko indeksas
            
        Returns:
            pd.Series: Interpoliuoti duomenys
        """
        try:
            # Konvertuojame laiką į skaičius
            original_times = data.index.astype(np.int64) // 10**9  # Unix timestamp
            original_temps = data.values
            new_times = new_index.astype(np.int64) // 10**9
            
            # Atliekame tiesinę interpoliaciją
            interpolated_temps = np.interp(new_times, original_times, original_temps)
            
            return pd.Series(interpolated_temps, index=new_index, name='temperatura')
            
        except Exception as e:
            logger.error(f"Klaida atliekant tiesinę interpoliaciją: {e}")
            raise
            
    def _time_interpolation(self, data: pd.Series, new_index: pd.DatetimeIndex) -> pd.Series:
        """
        Atlieka laiko pagrįstą interpoliaciją
        
        Args:
            data (pd.Series): Originalūs duomenys
            new_index (pd.DatetimeIndex): Naujas laiko indeksas
            
        Returns:
            pd.Series: Interpoliuoti duomenys
        """
        try:
            # Sukuriame DataFrame su nauju indeksu
            combined_index = data.index.union(new_index)
            temp_df = pd.DataFrame(index=combined_index)
            temp_df['temperatura'] = data
            
            # Atliekame laiko interpoliaciją
            temp_df['temperatura'] = temp_df['temperatura'].interpolate(method='time')
            
            return temp_df.loc[new_index, 'temperatura']
            
        except Exception as e:
            logger.error(f"Klaida atliekant laiko interpoliaciją: {e}")
            raise
            
    def _polynomial_interpolation(self, data: pd.Series, new_index: pd.DatetimeIndex, 
                                order: int) -> pd.Series:
        """
        Atlieka polinominę interpoliaciją
        
        Args:
            data (pd.Series): Originalūs duomenys
            new_index (pd.DatetimeIndex): Naujas laiko indeksas
            order (int): Polinomo eilė
            
        Returns:
            pd.Series: Interpoliuoti duomenys
        """
        try:
            # Konvertuojame laiką į skaičius
            original_times = data.index.astype(np.int64) // 10**9
            original_temps = data.values
            new_times = new_index.astype(np.int64) // 10**9
            
            # Normalizuojame laiko reikšmes geresniam skaitmeniniam stabilumui
            time_min = original_times.min()
            time_max = original_times.max()
            norm_original_times = (original_times - time_min) / (time_max - time_min)
            norm_new_times = (new_times - time_min) / (time_max - time_min)
            
            # Sukuriame polinomo koeficientus
            coefficients = np.polyfit(norm_original_times, original_temps, order)
            
            # Apskaičiuojame interpoliuotas reikšmes
            interpolated_temps = np.polyval(coefficients, norm_new_times)
            
            return pd.Series(interpolated_temps, index=new_index, name='temperatura')
            
        except Exception as e:
            logger.error(f"Klaida atliekant polinominę interpoliaciją: {e}")
            raise
            
    def _spline_interpolation(self, data: pd.Series, new_index: pd.DatetimeIndex) -> pd.Series:
        """
        Atlieka spline interpoliaciją
        
        Args:
            data (pd.Series): Originalūs duomenys
            new_index (pd.DatetimeIndex): Naujas laiko indeksas
            
        Returns:
            pd.Series: Interpoliuoti duomenys
        """
        try:
            # Konvertuojame laiką į skaičius
            original_times = data.index.astype(np.int64) // 10**9
            original_temps = data.values
            new_times = new_index.astype(np.int64) // 10**9
            
            # Sukuriame cubic spline interpoliatorių
            spline_func = interpolate.interp1d(
                original_times, original_temps, 
                kind='cubic', bounds_error=False, fill_value='extrapolate'
            )
            
            # Apskaičiuojame interpoliuotas reikšmes
            interpolated_temps = spline_func(new_times)
            
            return pd.Series(interpolated_temps, index=new_index, name='temperatura')
            
        except Exception as e:
            logger.error(f"Klaida atliekant spline interpoliaciją: {e}")
            raise
            
    def compare_methods(self, methods: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Palygina skirtingus interpoliacijos metodus
        
        Args:
            methods (List[str], optional): Metodų sąrašas palyginimui
            
        Returns:
            Dict: Palyginimo rezultatų žodynas
        """
        try:
            if self.original_data is None or self.original_data.empty:
                logger.error("Nėra duomenų metodų palyginimui")
                return {}
                
            if methods is None:
                methods = self.interpolation_methods
                
            results = {
                'originalūs_duomenys': len(self.original_data),
                'metodų_palyginimas': {}
            }
            
            for method in methods:
                try:
                    # Matuojame interpoliacijos laiką
                    start_time = datetime.now()
                    interpolated = self.interpolate_to_5min(method)
                    end_time = datetime.now()
                    
                    if interpolated is not None:
                        interpolation_time = (end_time - start_time).total_seconds()
                        
                        # Skaičiuojame kokybės metrikas
                        quality_metrics = self._calculate_quality_metrics(interpolated)
                        
                        results['metodų_palyginimas'][method] = {
                            'taškų_skaičius': len(interpolated),
                            'interpoliacijos_laikas_s': round(interpolation_time, 4),
                            'kokybės_metrikos': quality_metrics
                        }
                    else:
                        results['metodų_palyginimas'][method] = {
                            'klaida': 'Nepavyko atlikti interpoliacijos'
                        }
                        
                except Exception as e:
                    results['metodų_palyginimas'][method] = {
                        'klaida': str(e)
                    }
                    
            logger.info(f"Palyginti {len(methods)} interpoliacijos metodai")
            return results
            
        except Exception as e:
            logger.error(f"Klaida lyginant metodus: {e}")
            return {}
            
    def _calculate_quality_metrics(self, interpolated_data: pd.Series) -> Dict[str, float]:
        """
        Apskaičiuoja interpoliacijos kokybės metrikas
        
        Args:
            interpolated_data (pd.Series): Interpoliuoti duomenys
            
        Returns:
            Dict: Kokybės metrikų žodynas
        """
        try:
            metrics = {}
            
            if not interpolated_data.empty:
                # Pagrindinės statistikos
                metrics['vidurkis'] = round(interpolated_data.mean(), 2)
                metrics['standartinis_nuokrypis'] = round(interpolated_data.std(), 2)
                metrics['minimumas'] = round(interpolated_data.min(), 2)
                metrics['maksimumas'] = round(interpolated_data.max(), 2)
                
                # Interpoliacijos lygumo metrika (gradientas)
                if len(interpolated_data) > 1:
                    gradients = np.diff(interpolated_data.values)
                    metrics['vidutinis_gradientas'] = round(np.mean(np.abs(gradients)), 4)
                    metrics['maksimalus_gradientas'] = round(np.max(np.abs(gradients)), 4)
                    
                # Duomenų tankumo palyginimas su originaliais
                if self.original_data is not None:
                    density_ratio = len(interpolated_data) / len(self.original_data)
                    metrics['tankumo_koeficientas'] = round(density_ratio, 2)
                    
            return metrics
            
        except Exception as e:
            logger.error(f"Klaida skaičiuojant kokybės metrikas: {e}")
            return {}
            
    def validate_interpolation(self, test_ratio: float = 0.1) -> Dict[str, Any]:
        """
        Validuoja interpoliacijos tikslumą pašalinant dalis duomenų
        
        Args:
            test_ratio (float): Testų duomenų dalis
            
        Returns:
            Dict: Validacijos rezultatų žodynas
        """
        try:
            if self.original_data is None or self.original_data.empty:
                logger.error("Nėra duomenų validacijai")
                return {}
                
            # Atsitiktinai išrenkame test duomenis
            np.random.seed(42)  # Pakartojamumui
            n_test = max(1, int(len(self.original_data) * test_ratio))
            test_indices = np.random.choice(
                len(self.original_data), size=n_test, replace=False
            )
            
            # Padalijame duomenis
            train_data = self.original_data.drop(self.original_data.index[test_indices])
            test_data = self.original_data.iloc[test_indices]
            
            # Sukuriame atskirą interpoliatorių su train duomenimis
            temp_interpolator = TemperatureInterpolator(train_data)
            
            validation_results = {
                'train_duomenų_skaičius': len(train_data),
                'test_duomenų_skaičius': len(test_data),
                'metodų_validacija': {}
            }
            
            # Testuojame kiekvieną metodą
            for method in self.interpolation_methods:
                try:
                    # Interpoliuojame train duomenis
                    interpolated = temp_interpolator.interpolate_to_5min(method)
                    
                    if interpolated is not None:
                        # Apskaičiuojame klaidas test taškuose
                        errors = []
                        for test_time, true_temp in test_data.items():
                            # Randame arčiausią interpoliuotą reikšmę
                            closest_time = interpolated.index[
                                np.argmin(np.abs(interpolated.index - test_time))
                            ]
                            predicted_temp = interpolated[closest_time]
                            error = abs(predicted_temp - true_temp)
                            errors.append(error)
                            
                        # Skaičiuojame metrikos
                        mae = np.mean(errors)  # Mean Absolute Error
                        rmse = np.sqrt(np.mean([e**2 for e in errors]))  # Root Mean Square Error
                        max_error = np.max(errors)
                        
                        validation_results['metodų_validacija'][method] = {
                            'vidutinė_absoliuti_klaida': round(mae, 3),
                            'šaknies_kvadratinė_klaida': round(rmse, 3),
                            'maksimali_klaida': round(max_error, 3),
                            'testuotų_taškų_skaičius': len(errors)
                        }
                    else:
                        validation_results['metodų_validacija'][method] = {
                            'klaida': 'Nepavyko atlikti interpoliacijos'
                        }
                        
                except Exception as e:
                    validation_results['metodų_validacija'][method] = {
                        'klaida': str(e)
                    }
                    
            logger.info("Atlikta interpoliacijos validacija")
            return validation_results
            
        except Exception as e:
            logger.error(f"Klaida validuojant interpoliaciją: {e}")
            return {}
            
    def export_interpolated_data(self, filepath: str, 
                               format: str = 'csv') -> bool:
        """
        Eksportuoja interpoliuotus duomenis į failą
        
        Args:
            filepath (str): Failo kelias
            format (str): Failo formatas ('csv', 'excel', 'json')
            
        Returns:
            bool: True jei sėkmingai išeksportuota
        """
        try:
            if self.interpolated_data is None or self.interpolated_data.empty:
                logger.error("Nėra interpoliuotų duomenų eksportavimui")
                return False
                
            if format.lower() == 'csv':
                self.interpolated_data.to_csv(filepath, encoding='utf-8')
            elif format.lower() in ['excel', 'xlsx']:
                self.interpolated_data.to_excel(filepath, encoding='utf-8')
            elif format.lower() == 'json':
                self.interpolated_data.to_json(filepath, orient='index', 
                                             date_format='iso', force_ascii=False)
            else:
                logger.error(f"Nepalaikomas failo formatas: {format}")
                return False
                
            logger.info(f"Interpoliuoti duomenys išeksportuoti: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Klaida eksportuojant duomenis: {e}")
            return False