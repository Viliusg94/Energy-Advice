# -*- coding: utf-8 -*-
"""
Lietuvos oro duomenų API modulis
"""
import requests
import pandas as pd
import pytz
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging
import time

# Konfigūruojame logging sistemą
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherAPI:
    """
    Klasė skirta darbui su Lietuvos hidrometeorologijos tarnybos API
    """
    
    def __init__(self, location_code: str = "vilnius"):
        """
        Inicializuoja WeatherAPI objektą
        
        Args:
            location_code (str): Vietovės kodas (vilnius, kaunas, klaipeda, siauliai, panevezys)
        """
        self.location_code = location_code
        self.base_url = "https://api.meteo.lt/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Weather-Analysis-System/1.0'
        })
        
        # Lietuvos laiko zona
        self.lithuania_tz = pytz.timezone('Europe/Vilnius')
        
        # Miestų kodai
        self.city_codes = {
            'vilnius': 'vilnius',
            'kaunas': 'kaunas',
            'klaipeda': 'klaipeda',
            'siauliai': 'siauliai',
            'panevezys': 'panevezys'
        }
        
        if location_code not in self.city_codes:
            raise ValueError(f"Nepalaikomas miesto kodas: {location_code}")
            
    def _make_request(self, endpoint: str, params: Optional[Dict] = None, 
                     max_retries: int = 3) -> Optional[Dict[str, Any]]:
        """
        Atlieka HTTP užklausą su retry logika
        
        Args:
            endpoint (str): API endpoint
            params (Dict, optional): Užklausos parametrai
            max_retries (int): Maksimalus bandymų skaičius
            
        Returns:
            Dict: API atsakymas arba None klaidos atveju
        """
        url = f"{self.base_url}/{endpoint}"
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                logger.info(f"Sėkminga užklausa į {endpoint}")
                return data
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Bandymas {attempt + 1} nepavyko: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Visi bandymai nepavyko endpoint: {endpoint}")
                    return None
                    
    def get_historical_data(self, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        Gauna istorinius oro duomenis - šiuo metu API nepalaiko istorinių duomenų
        Grąžina None su informatyvia žinute
        
        Args:
            start_date (str): Pradžios data (YYYY-MM-DD formatu)
            end_date (str): Pabaigos data (YYYY-MM-DD formatu)
            
        Returns:
            pd.DataFrame: None - istoriniai duomenys neprieinami per API
        """
        logger.warning("METEO.LT API APRIBOJIMAS: Istoriniai duomenys neprieinami")
        logger.info("API palaiko tik prognozes (forecasts). Naudokite get_forecast_data()")
        logger.info(f"Užklausa istoriniams duomenims {start_date} - {end_date} praleidžiama")
        return None
            
    def get_forecast_data(self, days: int = 7) -> Optional[pd.DataFrame]:
        """
        Gauna oro prognozės duomenis
        
        Args:
            days (int): Dienų skaičius prognozei
            
        Returns:
            pd.DataFrame: Prognozės duomenys arba None klaidos atveju
        """
        try:
            endpoint = f"places/{self.location_code}/forecasts/long-term"
            data = self._make_request(endpoint)
            
            if not data or 'forecastTimestamps' not in data:
                logger.error("Nepavyko gauti prognozės duomenų")
                return None
                
            # Konvertuojame į DataFrame
            forecasts = data['forecastTimestamps']
            df = pd.DataFrame(forecasts)
            
            if df.empty:
                logger.warning("Gauti tušti prognozės duomenys")
                return df
                
            # Apdorojame laiko stulpelį
            df['forecastTimeUtc'] = pd.to_datetime(df['forecastTimeUtc'], utc=True)
            df['forecastTimeLocal'] = df['forecastTimeUtc'].dt.tz_convert(self.lithuania_tz)
            
            # Filtruojame pagal dienų skaičių
            cutoff_date = datetime.now(self.lithuania_tz) + timedelta(days=days)
            df = df[df['forecastTimeLocal'] <= cutoff_date]
            
            # Nustatome indeksą
            df.set_index('forecastTimeLocal', inplace=True)
            
            # Pervardiname stulpelius lietuviškai
            column_mapping = {
                'airTemperature': 'temperatura',
                'relativeHumidity': 'dregme',
                'windSpeed': 'vejo_greitis',
                'seaLevelPressure': 'slegimasJuros',
                'totalPrecipitation': 'krituliai'
            }
            
            df = df.rename(columns=column_mapping)
            
            logger.info(f"Gauti prognozės duomenys {days} dienoms: {len(df)} įrašų")
            return df
            
        except Exception as e:
            logger.error(f"Klaida gaunant prognozės duomenis: {e}")
            return None
            
    def get_current_weather(self) -> Optional[Dict[str, Any]]:
        """
        Gauna dabartinius oro duomenis iš forecast endpoint (latest)
        
        Returns:
            Dict: Dabartiniai oro duomenys arba None klaidos atveju
        """
        try:
            # Naudojame forecast endpoint kaip alternatives dabartiniams duomenims
            endpoint = f"places/{self.location_code}/forecasts/long-term"
            data = self._make_request(endpoint)
            
            if not data or 'forecastTimestamps' not in data:
                logger.error("Nepavyko gauti dabartinių oro duomenų")
                return None
                
            # Paimame pirmą forecast įrašą kaip artimiausią dabartiniam laikui
            current_forecast = data['forecastTimestamps'][0]
            
            # Formuojame result dict pagal standartinį formatą
            result = {
                'place': data['place'],
                'observationTimeUtc': current_forecast['forecastTimeUtc'],
                'airTemperature': current_forecast.get('airTemperature'),
                'relativeHumidity': current_forecast.get('relativeHumidity'),
                'windSpeed': current_forecast.get('windSpeed'),
                'seaLevelPressure': current_forecast.get('seaLevelPressure'),
                'totalPrecipitation': current_forecast.get('totalPrecipitation'),
                'conditionCode': current_forecast.get('conditionCode'),
                'cloudCover': current_forecast.get('cloudCover'),
                'windDirection': current_forecast.get('windDirection'),
                'feelsLikeTemperature': current_forecast.get('feelsLikeTemperature')
            }
                
            logger.info("Gauti dabartiniai oro duomenys (iš forecast)")
            return result
            
        except Exception as e:
            logger.error(f"Klaida gaunant dabartinius oro duomenis: {e}")
            return None
            
    def predict_weekend_rain(self) -> Optional[Dict[str, str]]:
        """
        Prognozuoja savaitgalio lietaus tikimybę
        
        Returns:
            Dict: Savaitgalio lietaus prognozė arba None klaidos atveju
        """
        try:
            forecast_data = self.get_forecast_data(days=7)
            if forecast_data is None or forecast_data.empty:
                return None
                
            # Randame šeštadienio ir sekmadienio duomenis
            weekend_data = {}
            
            for idx, row in forecast_data.iterrows():
                day_name = idx.strftime('%A').lower()
                if day_name in ['saturday', 'sunday']:
                    lithuanian_day = 'šeštadienis' if day_name == 'saturday' else 'sekmadienis'
                    
                    precipitation = row.get('krituliai', 0)
                    if precipitation > 0:
                        weekend_data[lithuanian_day] = f"Tikėtinas lietus: {precipitation}mm"
                    else:
                        weekend_data[lithuanian_day] = "Sausas oras"
                        
            return weekend_data if weekend_data else {"info": "Savaitgalio duomenų nerasta"}
            
        except Exception as e:
            logger.error(f"Klaida prognozuojant savaitgalio lietų: {e}")
            return None
                
            logger.info("Gauti dabartiniai oro duomenys")
            return data
            
        except Exception as e:
            logger.error(f"Klaida gaunant dabartinius oro duomenis: {e}")
            return None