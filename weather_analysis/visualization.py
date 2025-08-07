"""
Oro duomenų vizualizacijos funkcijos
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Tuple, List
import logging
import os

logger = logging.getLogger(__name__)

# Nustatyti matplotlib lietuvių kalbai
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)

class WeatherVisualizer:
    """
    Klasė oro duomenų vizualizacijai
    """
    
    def __init__(self, output_dir: str = "plots"):
        """
        Inicializuoja vizualizacijos klasę
        
        Args:
            output_dir (str): Katalogs grafiekų išsaugojimui
        """
        self.output_dir = output_dir
        
        # Sukuriame katalogą jei neegzistuoja
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Sukurtas katalogs grafiekams: {output_dir}")
    
    def plot_temperature_trend(self, historical_data: Optional[pd.DataFrame] = None, 
                             forecast_data: Optional[pd.DataFrame] = None,
                             title: str = "Temperatūros kaita", 
                             save_file: str = "temperature_trend.png") -> str:
        """
        Sukuria temperatūros kaitos grafiką
        
        Args:
            historical_data (pd.DataFrame, optional): Istoriniai duomenys
            forecast_data (pd.DataFrame, optional): Prognozės duomenys
            title (str): Grafiko pavadinimas
            save_file (str): Failo pavadinimas išsaugojimui
            
        Returns:
            str: Išsaugoto failo kelias
        """
        try:
            plt.figure(figsize=(14, 8))
            
            # Braižome istorinius duomenis
            if historical_data is not None and not historical_data.empty:
                if 'airTemperature' in historical_data.columns:
                    plt.plot(historical_data.index, historical_data['airTemperature'], 
                            label='Istoriniai duomenys', color='blue', linewidth=2)
                    logger.info(f"Išbraižyti {len(historical_data)} istoriniai duomenys")
            
            # Braižome prognozės duomenis
            if forecast_data is not None and not forecast_data.empty:
                temp_col = None
                for col in ['airTemperature', 'temperature', 'temp']:
                    if col in forecast_data.columns:
                        temp_col = col
                        break
                
                if temp_col:
                    plt.plot(forecast_data.index, forecast_data[temp_col], 
                            label='Prognozė', color='red', linewidth=2, linestyle='--')
                    logger.info(f"Išbraižyti {len(forecast_data)} prognozės duomenys")
            
            # Grafiko formatavimas
            plt.title(title, fontsize=16, fontweight='bold')
            plt.xlabel('Data ir laikas', fontsize=12)
            plt.ylabel('Temperatūra (°C)', fontsize=12)
            plt.legend(fontsize=12)
            plt.grid(True, alpha=0.3)
            
            # Sukuriame datumus X ašyje
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Išsaugome grafiką
            file_path = os.path.join(self.output_dir, save_file)
            plt.savefig(file_path, dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info(f"Grafikas išsaugotas: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Klaida kuriant temperatūros grafiką: {e}")
            return ""
    
    def plot_weather_dashboard(self, data: pd.DataFrame, 
                             title: str = "Oro sąlygų suvestinė",
                             save_file: str = "weather_dashboard.png") -> str:
        """
        Sukuria visapusišką oro sąlygų grafiką
        
        Args:
            data (pd.DataFrame): Oro duomenys
            title (str): Grafiko pavadinimas
            save_file (str): Failo pavadinimas
            
        Returns:
            str: Išsaugoto failo kelias
        """
        try:
            if data.empty:
                logger.warning("Nėra duomenų grafiko kūrimui")
                return ""
            
            # Sukuriame subplot'us
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle(title, fontsize=16, fontweight='bold')
            
            # 1. Temperatūros grafikas
            if 'airTemperature' in data.columns:
                axes[0, 0].plot(data.index, data['airTemperature'], color='red', linewidth=2)
                axes[0, 0].set_title('Temperatūra')
                axes[0, 0].set_ylabel('°C')
                axes[0, 0].grid(True, alpha=0.3)
            
            # 2. Drėgmės grafikas
            if 'relativeHumidity' in data.columns:
                axes[0, 1].plot(data.index, data['relativeHumidity'], color='blue', linewidth=2)
                axes[0, 1].set_title('Santykinė drėgmė')
                axes[0, 1].set_ylabel('%')
                axes[0, 1].grid(True, alpha=0.3)
            
            # 3. Vėjo greičio grafikas
            if 'windSpeed' in data.columns:
                axes[1, 0].plot(data.index, data['windSpeed'], color='green', linewidth=2)
                axes[1, 0].set_title('Vėjo greitis')
                axes[1, 0].set_ylabel('m/s')
                axes[1, 0].grid(True, alpha=0.3)
            
            # 4. Slėgio grafikas
            if 'seaLevelPressure' in data.columns:
                axes[1, 1].plot(data.index, data['seaLevelPressure'], color='purple', linewidth=2)
                axes[1, 1].set_title('Jūros lygio slėgis')
                axes[1, 1].set_ylabel('hPa')
                axes[1, 1].grid(True, alpha=0.3)
            
            # Formatuojame visus ašis
            for ax in axes.flat:
                ax.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            # Išsaugome grafiką
            file_path = os.path.join(self.output_dir, save_file)
            plt.savefig(file_path, dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info(f"Oro sąlygų suvestinė išsaugota: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Klaida kuriant oro sąlygų suvestinę: {e}")
            return ""
    
    def plot_precipitation_analysis(self, data: pd.DataFrame,
                                  title: str = "Kritulių analizė",
                                  save_file: str = "precipitation_analysis.png") -> str:
        """
        Sukuria kritulių analizės grafiką
        
        Args:
            data (pd.DataFrame): Oro duomenys
            title (str): Grafiko pavadinimas
            save_file (str): Failo pavadinimas
            
        Returns:
            str: Išsaugoto failo kelias
        """
        try:
            if data.empty:
                logger.warning("Nėra duomenų kritulių analizei")
                return ""
            
            precipitation_cols = ['totalPrecipitation', 'precipitation', 'rain']
            precip_col = None
            
            for col in precipitation_cols:
                if col in data.columns:
                    precip_col = col
                    break
            
            if precip_col is None:
                logger.warning("Nerasta kritulių duomenų stulpelių")
                return ""
            
            plt.figure(figsize=(14, 10))
            
            # Sukuriame subplot'us
            gs = plt.GridSpec(3, 1, height_ratios=[2, 1, 1])
            
            # 1. Kritulių kiekis laike
            ax1 = plt.subplot(gs[0])
            bars = ax1.bar(data.index, data[precip_col], color='skyblue', alpha=0.7)
            ax1.set_title('Kritulių kiekis laike')
            ax1.set_ylabel('mm')
            ax1.grid(True, alpha=0.3)
            
            # 2. Savaitgalių krituliai
            ax2 = plt.subplot(gs[1])
            weekend_mask = data.index.weekday.isin([5, 6])
            weekend_rain = data[weekend_mask][precip_col]
            weekday_rain = data[~weekend_mask][precip_col]
            
            rain_comparison = [weekday_rain.sum(), weekend_rain.sum()]
            labels = ['Darbo dienos', 'Savaitgaliai']
            colors = ['lightcoral', 'lightblue']
            
            ax2.bar(labels, rain_comparison, color=colors)
            ax2.set_title('Kritulių palyginimas')
            ax2.set_ylabel('Bendras mm')
            
            # 3. Lietingų dienų histograma
            ax3 = plt.subplot(gs[2])
            daily_precip = data[precip_col].resample('D').sum()
            rainy_days = daily_precip[daily_precip > 0]
            
            if not rainy_days.empty:
                ax3.hist(rainy_days, bins=10, color='green', alpha=0.7, edgecolor='black')
                ax3.set_title('Lietingų dienų kritulių pasiskirstymas')
                ax3.set_xlabel('Kritulių kiekis (mm)')
                ax3.set_ylabel('Dienų skaičius')
            
            plt.suptitle(title, fontsize=16, fontweight='bold')
            plt.tight_layout()
            
            # Išsaugome grafiką
            file_path = os.path.join(self.output_dir, save_file)
            plt.savefig(file_path, dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info(f"Kritulių analizė išsaugota: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Klaida kuriant kritulių analizę: {e}")
            return ""
    
    def plot_correlation_matrix(self, data: pd.DataFrame,
                              title: str = "Oro parametrų koreliacijos matrica",
                              save_file: str = "correlation_matrix.png") -> str:
        """
        Sukuria oro parametrų koreliacijos matricos grafiką
        
        Args:
            data (pd.DataFrame): Oro duomenys
            title (str): Grafiko pavadinimas
            save_file (str): Failo pavadinimas
            
        Returns:
            str: Išsaugoto failo kelias
        """
        try:
            if data.empty:
                logger.warning("Nėra duomenų koreliacijos matricai")
                return ""
            
            # Išfiltruojame tik skaitinius stulpelius
            numeric_data = data.select_dtypes(include=[np.number])
            
            if numeric_data.empty:
                logger.warning("Nėra skaitinių duomenų koreliacijos matricai")
                return ""
            
            # Skaičiuojame koreliaciją
            correlation_matrix = numeric_data.corr()
            
            plt.figure(figsize=(12, 10))
            
            # Sukuriame heatmap
            mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
            sns.heatmap(correlation_matrix, 
                       mask=mask,
                       annot=True, 
                       cmap='coolwarm', 
                       center=0,
                       square=True,
                       linewidths=0.5,
                       cbar_kws={"shrink": .8})
            
            plt.title(title, fontsize=16, fontweight='bold')
            plt.tight_layout()
            
            # Išsaugome grafiką
            file_path = os.path.join(self.output_dir, save_file)
            plt.savefig(file_path, dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info(f"Koreliacijos matrica išsaugota: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Klaida kuriant koreliacijos matricą: {e}")
            return ""
