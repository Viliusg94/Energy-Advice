"""
WeatherAPI klasė Lietuvos hidrometeorologijos tarnybos API integracijai
"""

import requests
import pandas as pd
import pytz
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

# Nustatyti logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lietuvos miestų kodai
CITY_CODES = {
    "vilnius": "vilniaus-ams",
    "kaunas": "kauno-ams", 
    "klaipeda": "klaipedos-ams",
    "siauliai": "siauliu-ams",
    "panevezys": "panevezio-ams"
}

class WeatherAPI:
    """
    Klasė darbui su Lietuvos hidrometeorologijos tarnybos API
    
    Attributes:
        base_url (str): Pagrindinis API URL
        location_code (str): Vietovės kodas
        timezone (pytz.timezone): Lietuvos laiko zona
    """
    
    def __init__(self, location_code: str = "vilnius"):
        """
        Inicializuoja WeatherAPI klasę
        
        Args:
            location_code (str): Vietovės kodas (default: "vilnius")
        """
        self.base_url = "https://api.meteo.lt/"
        self.original_location = location_code
        self.location_code = location_code
        self.station_code = CITY_CODES.get(location_code, "vilniaus-ams") 
        self.timezone = pytz.timezone('Europe/Vilnius')
        
        if location_code not in CITY_CODES:
            logger.warning(f"Vietovės kodas '{location_code}' nerastas. Naudojamas Vilnius.")
            self.location_code = "vilnius"
            self.station_code = "vilniaus-ams"
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
        """
        Atlieka HTTP užklausą į API
        
        Args:
            endpoint (str): API endpoint
            params (Dict[str, Any], optional): Užklausos parametrai
            
        Returns:
            Optional[Dict]: API atsakymas arba None jei klaida
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Klaida atliekant API užklausą: {e}")
            return None
        except ValueError as e:
            logger.error(f"Klaida apdorojant JSON atsakymą: {e}")
            return None
    
    def get_historical_data(self, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        Gauna istorinius oro duomenis nurodytam laikotarpiui
        
        Args:
            start_date (str): Pradžios data (YYYY-MM-DD)
            end_date (str): Pabaigos data (YYYY-MM-DD)
            
        Returns:
            Optional[pd.DataFrame]: Istoriniai duomenys arba None jei klaida
        """
        try:
            # Validuojame datas
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            
            if start_dt > end_dt:
                logger.error("Pradžios data negali būti vėlesnė už pabaigos datą")
                return None
            
            # API užklausa istoriniams duomenims - naudojame latest observations
            endpoint = f"v1/stations/{self.station_code}/observations/latest"
            
            data = self._make_request(endpoint)
            if not data:
                return None
            
            # Konvertuojame į DataFrame
            df = pd.DataFrame(data.get('observations', []))
            
            if df.empty:
                logger.warning("Nėra duomenų nurodytu laikotarpiu")
                return None
            
            # Nustatome laiko indeksą su Lietuvos laiko zona
            if 'observationTimeUtc' in df.columns:
                df['observationTimeUtc'] = pd.to_datetime(df['observationTimeUtc'], utc=True)
                df['observationTime'] = df['observationTimeUtc'].dt.tz_convert(self.timezone)
                df.set_index('observationTime', inplace=True)
            
            logger.info(f"Sėkmingai nuskaityti {len(df)} istorinių įrašų")
            return df
            
        except ValueError as e:
            logger.error(f"Neteisingas datos formatas: {e}")
            return None
        except Exception as e:
            logger.error(f"Klaida gaunant istorinius duomenis: {e}")
            return None
    
    def get_forecast_data(self) -> Optional[pd.DataFrame]:
        """
        Gauna oro prognozės duomenis
        
        Returns:
            Optional[pd.DataFrame]: Prognozės duomenys arba None jei klaida
        """
        try:
            # Naudojame places endpoint prognozėms
            endpoint = f"v1/places/{self.location_code}/forecasts/long-term"
            
            data = self._make_request(endpoint)
            if not data:
                return None
            
            # Konvertuojame į DataFrame
            df = pd.DataFrame(data.get('forecastTimestamps', []))
            
            if df.empty:
                logger.warning("Nėra prognozės duomenų")
                return None
            
            # Nustatome laiko indeksą su Lietuvos laiko zona
            if 'forecastTimeUtc' in df.columns:
                df['forecastTimeUtc'] = pd.to_datetime(df['forecastTimeUtc'], utc=True)
                df['forecastTime'] = df['forecastTimeUtc'].dt.tz_convert(self.timezone)
                df.set_index('forecastTime', inplace=True)
            
            logger.info(f"Sėkmingai nuskaityti {len(df)} prognozės įrašų")
            return df
            
        except Exception as e:
            logger.error(f"Klaida gaunant prognozės duomenis: {e}")
            return None
    
    def get_current_conditions(self) -> Optional[Dict]:
        """
        Gauna dabartinius oro sąlygas
        
        Returns:
            Optional[Dict]: Dabartiniai oro duomenys arba None jei klaida
        """
        try:
            endpoint = f"v1/stations/{self.station_code}/observations/latest"
            data = self._make_request(endpoint)
            
            if data:
                logger.info("Sėkmingai nuskaityti dabartiniai oro duomenys")
            
            return data
            
        except Exception as e:
            logger.error(f"Klaida gaunant dabartinius oro duomenis: {e}")
            return None
