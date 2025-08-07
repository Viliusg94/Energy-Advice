# -*- coding: utf-8 -*-
"""
Oro duomenų vizualizacijos modulis
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
import logging
import os

# Konfigūruojame matplotlib lietuvių kalbai
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

logger = logging.getLogger(__name__)


class WeatherVisualizer:
    """
    Klasė oro duomenų vizualizavimui ir grafikų kūrimui
    """
    
    def __init__(self, historical_data: Optional[pd.DataFrame] = None, 
                 forecast_data: Optional[pd.DataFrame] = None,
                 plots_dir: str = "plots"):
        """
        Inicializuoja WeatherVisualizer objektą
        
        Args:
            historical_data (pd.DataFrame, optional): Istoriniai oro duomenys
            forecast_data (pd.DataFrame, optional): Prognozės duomenys
            plots_dir (str): Katalogo pavadinimas grafikams išsaugoti
        """
        self.historical_data = historical_data
        self.forecast_data = forecast_data
        self.plots_dir = plots_dir
        
        # Sukuriame plots katalogą jei neegzistuoja
        os.makedirs(plots_dir, exist_ok=True)
        
        # Nustatome vizualizacijos stilių
        sns.set_style("whitegrid")
        plt.style.use('seaborn-v0_8')
        
    def plot_temperature_trend(self, days_back: int = 7, 
                             forecast_days: int = 7) -> str:
        """
        Sukuria temperatūros tendencijų grafiką
        
        Args:
            days_back (int): Dienų skaičius atgal istoriniams duomenims
            forecast_days (int): Dienų skaičius prognozei
            
        Returns:
            str: Išsaugoto grafiko failo kelias
        """
        try:
            fig, ax = plt.subplots(figsize=(14, 8))
            
            # Istoriniai duomenys
            if self.historical_data is not None and not self.historical_data.empty:
                # Filtruojame paskutinių dienų duomenis
                end_date = self.historical_data.index.max()
                start_date = end_date - timedelta(days=days_back)
                recent_hist = self.historical_data[
                    self.historical_data.index >= start_date
                ]
                
                if 'temperatura' in recent_hist.columns:
                    ax.plot(recent_hist.index, recent_hist['temperatura'], 
                           label='Istoriniai duomenys', color='blue', linewidth=2)
                    
            # Prognozės duomenys
            if self.forecast_data is not None and not self.forecast_data.empty:
                # Filtruojame prognozės duomenis
                forecast_end = datetime.now() + timedelta(days=forecast_days)
                forecast_subset = self.forecast_data[
                    self.forecast_data.index <= forecast_end
                ]
                
                if 'temperatura' in forecast_subset.columns:
                    ax.plot(forecast_subset.index, forecast_subset['temperatura'], 
                           label='Prognozė', color='red', linewidth=2, linestyle='--')
                    
            # Graiko formatavimas
            ax.set_title('Temperatūros tendencijos ir prognozė', 
                        fontsize=16, fontweight='bold')
            ax.set_xlabel('Data ir laikas', fontsize=12)
            ax.set_ylabel('Temperatūra (°C)', fontsize=12)
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)
            
            # Pageriniame x ašies formatavimą
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Išsaugome grafiką
            filename = 'temperature_trend.png'
            filepath = os.path.join(self.plots_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Temperatūros grafikas išsaugotas: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Klaida kuriant temperatūros grafiką: {e}")
            return ""
            
    def create_weather_dashboard(self) -> str:
        """
        Sukuria visapusišką oro sąlygų dashboard'ą
        
        Returns:
            str: Išsaugoto grafiko failo kelias
        """
        try:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('Oro sąlygų valdymo skydas', fontsize=18, fontweight='bold')
            
            data_to_use = self.historical_data if self.historical_data is not None else pd.DataFrame()
            
            if data_to_use.empty:
                logger.warning("Nėra duomenų dashboard kūrimui")
                return ""
                
            # 1. Temperatūros grafikas
            if 'temperatura' in data_to_use.columns:
                axes[0, 0].plot(data_to_use.index, data_to_use['temperatura'], 
                               color='red', linewidth=1.5)
                axes[0, 0].set_title('Temperatūra laike', fontsize=14)
                axes[0, 0].set_ylabel('Temperatūra (°C)')
                axes[0, 0].grid(True, alpha=0.3)
                
            # 2. Drėgmės grafikas
            if 'dregme' in data_to_use.columns:
                axes[0, 1].plot(data_to_use.index, data_to_use['dregme'], 
                               color='blue', linewidth=1.5)
                axes[0, 1].set_title('Santykine drėgmė', fontsize=14)
                axes[0, 1].set_ylabel('Drėgmė (%)')
                axes[0, 1].grid(True, alpha=0.3)
                
            # 3. Vėjo greicio grafikas
            if 'vejo_greitis' in data_to_use.columns:
                axes[1, 0].plot(data_to_use.index, data_to_use['vejo_greitis'], 
                               color='green', linewidth=1.5)
                axes[1, 0].set_title('Vėjo greitis', fontsize=14)
                axes[1, 0].set_ylabel('Greitis (m/s)')
                axes[1, 0].grid(True, alpha=0.3)
                
            # 4. Slėgimo grafikas
            if 'slegimasJuros' in data_to_use.columns:
                axes[1, 1].plot(data_to_use.index, data_to_use['slegimasJuros'], 
                               color='purple', linewidth=1.5)
                axes[1, 1].set_title('Atmosferos slėgimas', fontsize=14)
                axes[1, 1].set_ylabel('Slėgimas (hPa)')
                axes[1, 1].grid(True, alpha=0.3)
                
            # Formatuojame x ašis
            for ax in axes.flat:
                ax.tick_params(axis='x', rotation=45)
                
            plt.tight_layout()
            
            # Išsaugome grafiką
            filename = 'weather_dashboard.png'
            filepath = os.path.join(self.plots_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Dashboard grafikas išsaugotas: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Klaida kuriant dashboard: {e}")
            return ""
            
    def plot_correlation_heatmap(self, correlation_matrix: Optional[pd.DataFrame] = None) -> str:
        """
        Sukuria koreliacijos matricą heatmap formatu
        
        Args:
            correlation_matrix (pd.DataFrame, optional): Koreliacijos matrica
            
        Returns:
            str: Išsaugoto grafiko failo kelias
        """
        try:
            if correlation_matrix is None:
                # Skaičiuojame koreliacijas iš turimų duomenų
                data_to_use = self.historical_data if self.historical_data is not None else pd.DataFrame()
                if data_to_use.empty:
                    logger.warning("Nėra duomenų koreliacijos matricai")
                    return ""
                    
                numeric_cols = data_to_use.select_dtypes(include=[np.number]).columns
                correlation_matrix = data_to_use[numeric_cols].corr()
                
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Lietuviški stulpelių pavadinimai
            column_names_lt = {
                'temperatura': 'Temperatūra',
                'dregme': 'Drėgmė',
                'vejo_greitis': 'Vėjo greitis',
                'slegimasJuros': 'Slėgimas',
                'krituliai': 'Krituliai'
            }
            
            # Pervardiname stulpelius
            corr_renamed = correlation_matrix.rename(
                columns=column_names_lt, index=column_names_lt
            )
            
            # Sukuriame heatmap
            mask = np.triu(np.ones_like(corr_renamed))
            sns.heatmap(corr_renamed, mask=mask, annot=True, cmap='RdYlBu_r', 
                       center=0, square=True, linewidths=0.5, 
                       cbar_kws={"shrink": .8}, fmt='.2f', ax=ax)
            
            ax.set_title('Oro parametrų koreliacijos matrica', 
                        fontsize=16, fontweight='bold', pad=20)
            
            plt.tight_layout()
            
            # Išsaugome grafiką
            filename = 'correlation_heatmap.png'
            filepath = os.path.join(self.plots_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Koreliacijos matrica išsaugota: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Klaida kuriant koreliacijos matricą: {e}")
            return ""
            
    def plot_precipitation_analysis(self) -> str:
        """
        Sukuria kritulių analizės grafiką
        
        Returns:
            str: Išsaugoto grafiko failo kelias
        """
        try:
            if self.historical_data is None or self.historical_data.empty:
                logger.warning("Nėra duomenų kritulių analizei")
                return ""
                
            if 'krituliai' not in self.historical_data.columns:
                logger.warning("Nėra kritulių duomenų")
                return ""
                
            fig, axes = plt.subplots(2, 1, figsize=(14, 10))
            fig.suptitle('Kritulių analizė', fontsize=16, fontweight='bold')
            
            # 1. Kritulių kiekis laike
            axes[0].plot(self.historical_data.index, self.historical_data['krituliai'], 
                        color='blue', linewidth=1, alpha=0.7)
            axes[0].fill_between(self.historical_data.index, 
                               self.historical_data['krituliai'], 
                               alpha=0.3, color='blue')
            axes[0].set_title('Kritulių kiekis laike', fontsize=14)
            axes[0].set_ylabel('Krituliai (mm)')
            axes[0].grid(True, alpha=0.3)
            
            # 2. Kritulių pasiskirstymo histograma
            rain_data = self.historical_data[self.historical_data['krituliai'] > 0]['krituliai']
            
            if not rain_data.empty:
                axes[1].hist(rain_data, bins=30, color='lightblue', 
                           alpha=0.7, edgecolor='black')
                axes[1].set_title('Kritulių kiekio pasiskirstymas (tik lietingi periodai)', 
                                fontsize=14)
                axes[1].set_xlabel('Kritulių kiekis (mm)')
                axes[1].set_ylabel('Dažnis')
                axes[1].grid(True, alpha=0.3)
                
                # Pridedame statistikas
                mean_rain = rain_data.mean()
                median_rain = rain_data.median()
                axes[1].axvline(mean_rain, color='red', linestyle='--', 
                              label=f'Vidurkis: {mean_rain:.1f} mm')
                axes[1].axvline(median_rain, color='green', linestyle='--', 
                              label=f'Mediana: {median_rain:.1f} mm')
                axes[1].legend()
            else:
                axes[1].text(0.5, 0.5, 'Nėra kritulių duomenų', 
                           ha='center', va='center', transform=axes[1].transAxes, 
                           fontsize=16)
                
            plt.tight_layout()
            
            # Išsaugome grafiką
            filename = 'precipitation_analysis.png'
            filepath = os.path.join(self.plots_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Kritulių analizės grafikas išsaugotas: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Klaida kuriant kritulių analizės grafiką: {e}")
            return ""
            
    def plot_city_comparison(self, city_data: Dict[str, pd.DataFrame]) -> str:
        """
        Sukuria miestų palyginimo grafiką
        
        Args:
            city_data (Dict): Žodynas su miestų duomenimis
            
        Returns:
            str: Išsaugoto grafiko failo kelias
        """
        try:
            if not city_data:
                logger.warning("Nėra duomenų miestų palyginimui")
                return ""
                
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('Miestų oro sąlygų palyginimas', fontsize=18, fontweight='bold')
            
            # Spalvų paletė miestams
            colors = plt.cm.Set3(np.linspace(0, 1, len(city_data)))
            
            # 1. Temperatūros palyginimas
            for i, (city, data) in enumerate(city_data.items()):
                if 'temperatura' in data.columns:
                    axes[0, 0].plot(data.index, data['temperatura'], 
                                   label=city.title(), color=colors[i], linewidth=1.5)
            axes[0, 0].set_title('Temperatūros palyginimas', fontsize=14)
            axes[0, 0].set_ylabel('Temperatūra (°C)')
            axes[0, 0].legend()
            axes[0, 0].grid(True, alpha=0.3)
            
            # 2. Drėgmės palyginimas
            for i, (city, data) in enumerate(city_data.items()):
                if 'dregme' in data.columns:
                    axes[0, 1].plot(data.index, data['dregme'], 
                                   label=city.title(), color=colors[i], linewidth=1.5)
            axes[0, 1].set_title('Drėgmės palyginimas', fontsize=14)
            axes[0, 1].set_ylabel('Drėgmė (%)')
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)
            
            # 3. Vidutinių temperatūrų stulpelių grafikas
            city_names = []
            avg_temps = []
            for city, data in city_data.items():
                if 'temperatura' in data.columns and not data['temperatura'].empty:
                    city_names.append(city.title())
                    avg_temps.append(data['temperatura'].mean())
                    
            if city_names:
                bars = axes[1, 0].bar(city_names, avg_temps, color=colors[:len(city_names)])
                axes[1, 0].set_title('Vidutinės temperatūros pagal miestus', fontsize=14)
                axes[1, 0].set_ylabel('Temperatūra (°C)')
                
                # Pridedame reikšmes ant stulpelių
                for bar, temp in zip(bars, avg_temps):
                    height = bar.get_height()
                    axes[1, 0].text(bar.get_x() + bar.get_width()/2., height + 0.1,
                                   f'{temp:.1f}°C', ha='center', va='bottom')
                                   
            # 4. Temperatūros diapazonų palyginimas (box plot)
            temp_data_for_box = []
            labels_for_box = []
            for city, data in city_data.items():
                if 'temperatura' in data.columns and not data['temperatura'].empty:
                    temp_data_for_box.append(data['temperatura'].values)
                    labels_for_box.append(city.title())
                    
            if temp_data_for_box:
                box_plot = axes[1, 1].boxplot(temp_data_for_box, labels=labels_for_box, 
                                            patch_artist=True)
                axes[1, 1].set_title('Temperatūros pasiskirstymas', fontsize=14)
                axes[1, 1].set_ylabel('Temperatūra (°C)')
                
                # Spalviname box plot
                for patch, color in zip(box_plot['boxes'], colors[:len(box_plot['boxes'])]):
                    patch.set_facecolor(color)
                    
            # Formatuojame x ašis
            for ax in axes.flat:
                ax.tick_params(axis='x', rotation=45)
                
            plt.tight_layout()
            
            # Išsaugome grafiką
            filename = 'city_comparison.png'
            filepath = os.path.join(self.plots_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Miestų palyginimo grafikas išsaugotas: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Klaida kuriant miestų palyginimo grafiką: {e}")
            return ""
            
    def create_summary_visualization(self, analysis_results: Dict[str, Any]) -> str:
        """
        Sukuria bendrą analizės rezultatų vizualizaciją
        
        Args:
            analysis_results (Dict): Analizės rezultatų žodynas
            
        Returns:
            str: Išsaugoto grafiko failo kelias
        """
        try:
            fig = plt.figure(figsize=(16, 12))
            fig.suptitle('Oro duomenų analizės suvestinė', fontsize=20, fontweight='bold')
            
            # Sukuriame grid layout
            gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
            
            # 1. Metiniai vidurkiai (pie chart)
            if 'metiniai_vidurkiai' in analysis_results:
                ax1 = fig.add_subplot(gs[0, 0])
                yearly_data = analysis_results['metiniai_vidurkiai']
                if yearly_data:
                    values = list(yearly_data.values())
                    labels = [key.replace('_', ' ').title() for key in yearly_data.keys()]
                    ax1.pie([1]*len(values), labels=labels, autopct='%1.1f', startangle=90)
                    ax1.set_title('Metiniai vidurkiai', fontsize=12)
                    
            # 2. Dienos/nakties temperatūra
            if 'dienos_nakties_analizė' in analysis_results:
                ax2 = fig.add_subplot(gs[0, 1])
                day_night = analysis_results['dienos_nakties_analizė']
                if 'vidutinė_dienos_temperatūra' in day_night and 'vidutinė_nakties_temperatūra' in day_night:
                    temps = [day_night['vidutinė_dienos_temperatūra'], 
                           day_night['vidutinė_nakties_temperatūra']]
                    labels = ['Diena', 'Naktis']
                    bars = ax2.bar(labels, temps, color=['orange', 'navy'])
                    ax2.set_title('Dienos/nakties temperatūra', fontsize=12)
                    ax2.set_ylabel('Temperatūra (°C)')
                    
                    # Pridedame reikšmes
                    for bar, temp in zip(bars, temps):
                        height = bar.get_height()
                        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                               f'{temp:.1f}°C', ha='center', va='bottom')
                               
            # 3. Savaitgalių lietaus statistika
            if 'savaitgalių_lietaus_prognozė' in analysis_results:
                ax3 = fig.add_subplot(gs[0, 2])
                weekend_data = analysis_results['savaitgalių_lietaus_prognozė']
                if 'savaitgalių_skaičius' in weekend_data and weekend_data['savaitgalių_skaičius'] > 0:
                    total = weekend_data['savaitgalių_skaičius']
                    rainy = weekend_data.get('savaitgaliai_su_lietumi', 0)
                    dry = total - rainy
                    
                    ax3.pie([rainy, dry], labels=['Su lietumi', 'Be lietaus'], 
                           autopct='%1.1f%%', colors=['lightblue', 'lightcoral'])
                    ax3.set_title('Savaitgalių lietaus prognozė', fontsize=12)
                    
            # Duomenų lentelė (tekstinė informacija)
            ax4 = fig.add_subplot(gs[1, :])
            ax4.axis('off')
            
            info_text = "PAGRINDINIAI STATISTINIAI RODIKLIAI:\n\n"
            
            if 'metiniai_vidurkiai' in analysis_results:
                yearly = analysis_results['metiniai_vidurkiai']
                for key, value in yearly.items():
                    info_text += f"{key.replace('_', ' ').title()}: {value}\n"
                    
            if 'ekstremaliuosius_rodikliai' in analysis_results:
                extremes = analysis_results['ekstremaliuosius_rodikliai']
                info_text += "\nEKSTREMALUOSI RODIKLIAI:\n"
                for key, value in extremes.items():
                    if isinstance(value, dict) and 'reikšmė' in value:
                        info_text += f"{key.replace('_', ' ').title()}: {value['reikšmė']}\n"
                        
            ax4.text(0.05, 0.95, info_text, transform=ax4.transAxes, 
                    fontsize=11, verticalalignment='top', fontfamily='monospace',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
            
            # Duomenų kiekio informacija
            ax5 = fig.add_subplot(gs[2, :])
            ax5.axis('off')
            
            data_info = "DUOMENŲ KIEKIO INFORMACIJA:\n\n"
            if 'duomenų_kiekis' in analysis_results:
                data_counts = analysis_results['duomenų_kiekis']
                for key, value in data_counts.items():
                    data_info += f"{key.title()}: {value} įrašų\n"
                    
            if 'analizės_data' in analysis_results:
                data_info += f"\nAnalizės data: {analysis_results['analizės_data']}"
                
            ax5.text(0.05, 0.95, data_info, transform=ax5.transAxes, 
                    fontsize=11, verticalalignment='top', fontfamily='monospace',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
            
            # Išsaugome grafiką
            filename = 'analysis_summary.png'
            filepath = os.path.join(self.plots_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Analizės suvestinės grafikas išsaugotas: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Klaida kuriant suvestinės grafiką: {e}")
            return ""