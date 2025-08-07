# -*- coding: utf-8 -*-
"""
Lietuvos oro duomenų analizės sistema - Pagrindinė programa
"""
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any

# Importuojame mūsų modulius
from src.weather_api import WeatherAPI
from src.data_analysis import WeatherAnalyzer
from src.visualization import WeatherVisualizer
from src.interpolation import TemperatureInterpolator

# Konfigūruojame logging sistemą
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weather_analysis.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """
    Pagrindinė programos funkcija
    """
    try:
        logger.info("Paleidžiama Lietuvos oro duomenų analizės sistema")
        
        # Sukuriame katalogus duomenims ir grafikams
        os.makedirs('data', exist_ok=True)
        os.makedirs('plots', exist_ok=True)
        
        # Inicializuojame API objektą Vilniui
        print("Inicializuojama API prisijungimas...")
        api = WeatherAPI('vilnius')
        
        # Nustatome datos intervalą (paskutinės 30 dienų)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        print("DĖMESIO: Istoriniai duomenys neprieinami per meteo.lt API")
        print("Naudojami tik prognozės duomenys (realūs API duomenys)")
        historical_data = None
        
        # Gauname prognozės duomenis
        print("Nuskaitoma oro prognozė...")
        forecast_data = api.get_forecast_data(days=7)
        
        if forecast_data is None or forecast_data.empty:
            print("ĮSPĖJIMAS: Nepavyko gauti prognozės duomenų")
            forecast_data = None
        else:
            print(f"Gauti prognozės duomenys: {len(forecast_data)} įrašų")
            
        # Išsaugome duomenis (tik prognozės duomenis)
        if forecast_data is not None:
            forecast_data.to_csv('data/forecast_data.csv', encoding='utf-8')
            print("Prognozės duomenys išsaugoti: data/forecast_data.csv")
            
        # Inicializuojame analizės objektą (tik su prognozės duomenimis)
        if forecast_data is None or forecast_data.empty:
            print("KLAIDA: Nepavyko gauti prognozės duomenų iš API")
            return
            
        print("Atliekama duomenų analizė su realiais API duomenimis...")
        analyzer = WeatherAnalyzer(historical_data=None, forecast_data=forecast_data)
        
        # Apskaičiuojame metinius vidurkius
        yearly_averages = analyzer.calculate_yearly_averages()
        print("\nMETINIAI VIDURKIAI:")
        for key, value in yearly_averages.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
            
        # Analizuojame dienos/nakties temperatūrą
        day_night_analysis = analyzer.analyze_day_night_temperature()
        print("\nDIENOS/NAKTIES TEMPERATŪROS ANALIZĖ:")
        for key, value in day_night_analysis.items():
            print(f"  {key.replace('_', ' ').title()}: {value}°C")
            
        # Analizuojame savaitgalių lietaus prognozes
        weekend_rain = analyzer.analyze_weekend_rain_forecast()
        print("\nSAVAITGALIŲ LIETAUS PROGNOZĖ:")
        if weekend_rain:
            print(f"  Savaitgalių skaičius: {weekend_rain.get('savaitgalių_skaičius', 0)}")
            print(f"  Savaitgaliai su lietumi: {weekend_rain.get('savaitgaliai_su_lietumi', 0)}")
            print(f"  Lietaus tikimybė: {weekend_rain.get('lietaus_tikimybė_procentais', 0)}%")
            
        # Generuojame išsamią ataskaitą
        full_report = analyzer.generate_summary_report()
        
        # Išsaugome analizės rezultatus
        with open('data/analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump(full_report, f, indent=2, ensure_ascii=False, default=str)
            
        # Sukuriame vizualizacijas su realiais API duomenimis
        print("\nKuriamos vizualizacijos su realiais meteo.lt API duomenimis...")
        visualizer = WeatherVisualizer(historical_data=None, forecast_data=forecast_data)
        
        # Temperatūros tendencijų grafikas
        temp_plot = visualizer.plot_temperature_trend()
        if temp_plot:
            print(f"Sukurtas temperatūros grafikas: {temp_plot}")
            
        # Oro sąlygų dashboard
        dashboard_plot = visualizer.create_weather_dashboard()
        if dashboard_plot:
            print(f"Sukurtas dashboard: {dashboard_plot}")
            
        # Koreliacijos matrica
        correlations = analyzer.calculate_correlations()
        if correlations is not None:
            heatmap_plot = visualizer.plot_correlation_heatmap(correlations)
            if heatmap_plot:
                print(f"Sukurta koreliacijos matrica: {heatmap_plot}")
                
        # Kritulių analizė
        precipitation_plot = visualizer.plot_precipitation_analysis()
        if precipitation_plot:
            print(f"Sukurtas kritulių analizės grafikas: {precipitation_plot}")
            
        # Analizės suvestinė
        summary_plot = visualizer.create_summary_visualization(full_report)
        if summary_plot:
            print(f"Sukurta analizės suvestinė: {summary_plot}")
            
        # Temperatūros interpoliacija (naudojame prognozės duomenis)
        if forecast_data is not None and 'temperatura' in forecast_data.columns:
            print("\nAtliekama temperatūros interpoliacija su prognozės duomenimis...")
            temp_series = {}
            for timestamp, row in forecast_data.head(24).iterrows():
                time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                temp_series[time_str] = row['temperatura']
                
            interpolator = TemperatureInterpolator(temp_series)
            
            # Lyginame interpoliacijos metodus
            comparison = interpolator.compare_methods()
            print("INTERPOLIACIJOS METODŲ PALYGINIMAS:")
            for method, results in comparison.get('metodų_palyginimas', {}).items():
                if 'klaida' not in results:
                    print(f"  {method.title()}:")
                    print(f"    Taškų skaičius: {results.get('taškų_skaičius', 'N/A')}")
                    print(f"    Laikas: {results.get('interpoliacijos_laikas_s', 'N/A')}s")
                    
            # Atliekame geriausią interpoliaciją ir išsaugome
            best_interpolated = interpolator.interpolate_to_5min(temp_series, method='linear')
            if best_interpolated is not None:
                # Konvertuojame į pandas Series ir išsaugome
                import pandas as pd
                if isinstance(best_interpolated, dict):
                    timestamps = list(best_interpolated.keys())
                    temperatures = list(best_interpolated.values())
                    interpolated_df = pd.DataFrame({
                        'timestamp': timestamps,
                        'temperatura': temperatures
                    })
                    interpolated_df.to_csv('data/interpolated_temperature.csv', 
                                         encoding='utf-8', index=False)
                    print("Interpoliuoti duomenys išsaugoti: data/interpolated_temperature.csv")
                
            # Validuojame interpoliaciją
            validation = interpolator.validate_interpolation()
            if validation:
                with open('data/interpolation_validation.json', 'w', encoding='utf-8') as f:
                    json.dump(validation, f, indent=2, ensure_ascii=False)
                    
        print("\nSISTEMOS VEIKLOS SUVESTINĖ (REALŪS API DUOMENYS):")
        if forecast_data is not None:
            print(f"  Prognozės duomenų: {len(forecast_data)} įrašų (realūs meteo.lt API)")
        print(f"  Sukurti grafikai: plots/ kataloge")
        print(f"  Analizės rezultatai: data/analysis_results.json")
        print(f"  API šaltinis: api.meteo.lt (oficialūs duomenys)")
        
        logger.info("Programa sėkmingai baigė darbą")
        
    except KeyboardInterrupt:
        print("\nPrograma nutraukta vartotojo")
        logger.info("Programa nutraukta vartotojo")
        
    except Exception as e:
        print(f"KRITINĖ KLAIDA: {e}")
        logger.error(f"Kritinė programa klaida: {e}", exc_info=True)


def demo_multiple_cities():
    """
    Demonstracijos funkcija keliems miestams
    """
    cities = ['vilnius', 'kaunas', 'klaipeda']
    city_data = {}
    
    print("KELIŲ MIESTŲ DEMO REŽIMAS")
    print("=" * 40)
    
    for city in cities:
        try:
            print(f"Nuskaitomi {city.title()} prognozės duomenys...")
            api = WeatherAPI(city)
            
            # Gauname prognozės duomenis (nes istoriniai neprieinami)
            data = api.get_forecast_data(days=7)
            
            if data is not None and not data.empty:
                city_data[city] = data
                print(f"  {city.title()}: {len(data)} prognozės įrašų")
                
                # Greitų statistikos iš prognozės duomenų
                if 'temperatura' in data.columns:
                    avg_temp = data['temperatura'].mean()
                    min_temp = data['temperatura'].min()
                    max_temp = data['temperatura'].max()
                    print(f"  Vidutinė temperatūra: {avg_temp:.1f}°C")
                    print(f"  Temperatūros diapazonas: {min_temp:.1f}°C - {max_temp:.1f}°C")
                    
        except Exception as e:
            print(f"Klaida nuskaitant {city} duomenis: {e}")
            
    if len(city_data) > 1:
        # Sukuriame miestų palyginimo grafiką
        visualizer = WeatherVisualizer()
        comparison_plot = visualizer.plot_city_comparison(city_data)
        if comparison_plot:
            print(f"\nMiestų palyginimo grafikas: {comparison_plot}")
            
        # Išsaugome visų miestų duomenis
        for city, data in city_data.items():
            data.to_csv(f'data/{city}_data.csv', encoding='utf-8')
            
    print("\nDemo užbaigtas!")


if __name__ == "__main__":
    print("Lietuvos oro duomenų analizės sistema")
    print("=" * 50)
    print("1. Standartinė analizė (Vilnius)")
    print("2. Kelių miestų palyginimas")
    print("3. Išeiti")
    
    try:
        choice = input("\nPasirinkite režimą (1-3): ").strip()
        
        if choice == '1':
            main()
        elif choice == '2':
            demo_multiple_cities()
        elif choice == '3':
            print("Programa uždaroma...")
        else:
            print("Neteisingas pasirinkimas. Paleidžiamas standartinis režimas...")
            main()
            
    except KeyboardInterrupt:
        print("\nPrograma nutraukta")
    except Exception as e:
        print(f"Klaida: {e}")
        logger.error(f"Main klaida: {e}", exc_info=True)