"""
Oro duomenų analizės funkcijos
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class WeatherAnalyzer:
    """
    Klasė oro duomenų analizei ir statistikos skaičiavimui
    """
    
    def __init__(self, historical_data: Optional[pd.DataFrame] = None, 
                 forecast_data: Optional[pd.DataFrame] = None):
        """
        Inicializuoja analizės klasę
        
        Args:
            historical_data (pd.DataFrame, optional): Istoriniai duomenys
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
            
            # Užtikriname suderinamumą
            hist_cols = set(self.historical_data.columns)
            forecast_cols = set(self.forecast_data.columns)
            common_cols = hist_cols.intersection(forecast_cols)
            
            if not common_cols:
                logger.warning("Nėra bendrų stulpelių tarp istorinių ir prognozės duomenų")
                return pd.DataFrame()
            
            # Filtruojame tik bendrus stulpelius
            hist_filtered = self.historical_data[list(common_cols)]
            forecast_filtered = self.forecast_data[list(common_cols)]
            
            # Sujungiame
            self.combined_data = pd.concat([hist_filtered, forecast_filtered])
            self.combined_data.sort_index(inplace=True)
            
            logger.info(f"Sėkmingai sujungti duomenys: {len(self.combined_data)} įrašų")
            return self.combined_data
            
        except Exception as e:
            logger.error(f"Klaida sujungiant duomenis: {e}")
            return pd.DataFrame()
    
    def calculate_annual_averages(self, data: Optional[pd.DataFrame] = None) -> Dict[str, float]:
        """
        Apskaičiuoja metinius vidurkius
        
        Args:
            data (pd.DataFrame, optional): Duomenys analizei
            
        Returns:
            Dict[str, float]: Metiniai vidurkiai
        """
        try:
            if data is None:
                data = self.historical_data
            
            if data is None or data.empty:
                logger.warning("Nėra duomenų metinių vidurkių skaičiavimui")
                return {}
            
            results = {}
            
            # Temperatūros vidurkis
            if 'airTemperature' in data.columns:
                results['average_temperature'] = data['airTemperature'].mean()
            
            # Drėgmės vidurkis
            if 'relativeHumidity' in data.columns:
                results['average_humidity'] = data['relativeHumidity'].mean()
            
            # Vėjo greičio vidurkis
            if 'windSpeed' in data.columns:
                results['average_wind_speed'] = data['windSpeed'].mean()
            
            # Slėgio vidurkis
            if 'seaLevelPressure' in data.columns:
                results['average_pressure'] = data['seaLevelPressure'].mean()
            
            logger.info("Sėkmingai apskaičiuoti metiniai vidurkiai")
            return results
            
        except Exception as e:
            logger.error(f"Klaida skaičiuojant metinius vidurkius: {e}")
            return {}
    
    def analyze_day_night_temperature(self, data: Optional[pd.DataFrame] = None) -> Dict[str, float]:
        """
        Analizuoja dienos ir nakties temperatūros skirtumus
        
        Args:
            data (pd.DataFrame, optional): Duomenys analizei
            
        Returns:
            Dict[str, float]: Dienos ir nakties temperatūros statistika
        """
        try:
            if data is None:
                data = self.historical_data
            
            if data is None or data.empty or 'airTemperature' not in data.columns:
                logger.warning("Nėra temperatūros duomenų analizei")
                return {}
            
            # Filtruojame pagal laiko intervalus
            # Diena: 08:00-20:00, Naktis: 20:00-08:00
            day_mask = (data.index.hour >= 8) & (data.index.hour < 20)
            night_mask = ~day_mask
            
            day_temps = data[day_mask]['airTemperature']
            night_temps = data[night_mask]['airTemperature']
            
            results = {
                'average_day_temperature': day_temps.mean() if not day_temps.empty else 0,
                'average_night_temperature': night_temps.mean() if not night_temps.empty else 0,
                'day_night_difference': (day_temps.mean() - night_temps.mean()) if not day_temps.empty and not night_temps.empty else 0
            }
            
            logger.info("Sėkmingai apskaičiuota dienos/nakties temperatūros analizė")
            return results
            
        except Exception as e:
            logger.error(f"Klaida analizuojant dienos/nakties temperatūrą: {e}")
            return {}
    
    def analyze_weekend_rain_forecast(self, data: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """
        Analizuoja savaitgalių lietaus prognozes
        
        Args:
            data (pd.DataFrame, optional): Prognozės duomenys
            
        Returns:
            Dict[str, Any]: Savaitgalių lietaus statistika
        """
        try:
            if data is None:
                data = self.forecast_data
            
            if data is None or data.empty:
                logger.warning("Nėra prognozės duomenų analizei")
                return {}
            
            # Filtruojame savaitgalius (šeštadienis = 5, sekmadienis = 6)
            weekend_mask = data.index.weekday.isin([5, 6])
            weekend_data = data[weekend_mask]
            
            if weekend_data.empty:
                return {'weekend_rain_days': 0, 'total_weekends': 0, 'rain_probability': 0}
            
            # Skaičiuojame lietingus savaitgalius
            rain_days = 0
            if 'totalPrecipitation' in weekend_data.columns:
                rain_days = (weekend_data['totalPrecipitation'] > 0).sum()
            elif 'precipitation' in weekend_data.columns:
                rain_days = (weekend_data['precipitation'] > 0).sum()
            
            total_weekend_days = len(weekend_data)
            rain_probability = (rain_days / total_weekend_days * 100) if total_weekend_days > 0 else 0
            
            results = {
                'weekend_rain_days': rain_days,
                'total_weekend_days': total_weekend_days,
                'rain_probability': rain_probability
            }
            
            logger.info("Sėkmingai apskaičiuota savaitgalių lietaus analizė")
            return results
            
        except Exception as e:
            logger.error(f"Klaida analizuojant savaitgalių lietų: {e}")
            return {}
    
    def get_last_week_data(self, data: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Gauna paskutinės savaitės duomenis
        
        Args:
            data (pd.DataFrame, optional): Duomenys filtravimui
            
        Returns:
            pd.DataFrame: Paskutinės savaitės duomenys
        """
        try:
            if data is None:
                data = self.historical_data
            
            if data is None or data.empty:
                return pd.DataFrame()
            
            # Apskaičiuojame paskutinę savaitę
            end_date = data.index.max()
            start_date = end_date - timedelta(days=7)
            
            last_week_data = data[data.index >= start_date]
            
            logger.info(f"Gauti {len(last_week_data)} paskutinės savaitės įrašai")
            return last_week_data
            
        except Exception as e:
            logger.error(f"Klaida gaunant paskutinės savaitės duomenis: {e}")
            return pd.DataFrame()
    
    def print_analysis_results(self, annual_avg: Dict[str, float], 
                             day_night: Dict[str, float], 
                             weekend_rain: Dict[str, Any]):
        """
        Išspausdina analizės rezultatus
        
        Args:
            annual_avg: Metiniai vidurkiai
            day_night: Dienos/nakties temperatūros
            weekend_rain: Savaitgalių lietaus duomenys
        """
        print("=" * 50)
        print("ORO DUOMENŲ ANALIZĖS REZULTATAI")
        print("=" * 50)
        
        if annual_avg:
            print("\nMETINiai VIDURKIAI:")
            for key, value in annual_avg.items():
                formatted_key = key.replace('_', ' ').title()
                if 'temperature' in key.lower():
                    print(f"  {formatted_key}: {value:.1f}°C")
                elif 'humidity' in key.lower():
                    print(f"  {formatted_key}: {value:.1f}%")
                elif 'wind' in key.lower():
                    print(f"  {formatted_key}: {value:.1f} m/s")
                elif 'pressure' in key.lower():
                    print(f"  {formatted_key}: {value:.1f} hPa")
                else:
                    print(f"  {formatted_key}: {value:.2f}")
        
        if day_night:
            print("\nDIENOS/NAKTIES TEMPERATŪRA:")
            for key, value in day_night.items():
                formatted_key = key.replace('_', ' ').title()
                print(f"  {formatted_key}: {value:.1f}°C")
        
        if weekend_rain:
            print("\nSAVAITGALIŲ LIETAUS PROGNOZĖ:")
            for key, value in weekend_rain.items():
                formatted_key = key.replace('_', ' ').title()
                if 'probability' in key.lower():
                    print(f"  {formatted_key}: {value:.1f}%")
                else:
                    print(f"  {formatted_key}: {value}")
        
        print("=" * 50)
