"""
Pagrindinė Lietuvos oro duomenų analizės programa
Naudoja meteo.lt API duomenų nuskaitymui ir analizei
"""

import sys
import os
from datetime import datetime, timedelta
import pandas as pd
import logging

# Pridedame weather_analysis katalogą į Python kelią
sys.path.append(os.path.join(os.path.dirname(__file__), 'weather_analysis'))

from weather_analysis.weather_api import WeatherAPI, CITY_CODES
from weather_analysis.data_analysis import WeatherAnalyzer
from weather_analysis.visualization import WeatherVisualizer
from weather_analysis.interpolation import TemperatureInterpolator

# Nustatyti logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(name)s  %(levelname)s  %(message)s',
    handlers=[
        logging.FileHandler('weather_analysis.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """
    Pagrindinė programos funkcija
    """
    print("=" * 60)
    print("LIETUVOS ORO DUOMENŲ ANALIZĖS PROGRAMA")
    print("Duomenų šaltinis: api.meteo.lt")
    print("=" * 60)
    
    try:
        # 1. Inicializuojame API klasę
        print("\n  Inicializuojame Weather API...")
        weather_api = WeatherAPI(location_code="vilnius")
        
        # 2. Nuskaitome istorinius duomenis (paskutinės 365 dienos)
        print("\n  Nuskaitome istorinius duomenis...")
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        
        historical_data = weather_api.get_historical_data(start_date, end_date)
        
        if historical_data is None or historical_data.empty:
            print("❌ Nepavyko nuskaityti istorinių duomenų")
            return
        
        print(f"✅ Nuskaityti istoriniai duomenys: {len(historical_data)} įrašų")
        
        # 3. Nuskaitome prognozės duomenis
        print("\n  Nuskaitome prognozės duomenis...")
        forecast_data = weather_api.get_forecast_data()
        
        if forecast_data is None or forecast_data.empty:
            print("⚠️  Nepavyko nuskaityti prognozės duomenų, tęsiame su istoriniais")
            forecast_data = None
        else:
            print(f"✅ Nuskaityti prognozės duomenys: {len(forecast_data)} įrašų")
        
        # 4. Inicializuojame analizės klasę
        print("\n  Inicializuojame duomenų analizę...")
        analyzer = WeatherAnalyzer(historical_data, forecast_data)
        
        # 5. Atliekame duomenų analizę
        print("\n  Atliekame duomenų analizę...")
        
        # Metiniai vidurkiai
        annual_averages = analyzer.calculate_annual_averages()
        
        # Dienos/nakties temperatūros analizė
        day_night_analysis = analyzer.analyze_day_night_temperature()
        
        # Savaitgalių lietaus prognozė (jei yra prognozės duomenų)
        weekend_rain = {}
        if forecast_data is not None:
            weekend_rain = analyzer.analyze_weekend_rain_forecast()
        
        # Spausdiname rezultatus
        analyzer.print_analysis_results(annual_averages, day_night_analysis, weekend_rain)
        
        # 6. Sukuriame vizualizacijas
        print("\n  Kuriame grafikus...")
        visualizer = WeatherVisualizer("plots")
        
        # Paskutinės savaitės duomenys grafikui
        last_week_data = analyzer.get_last_week_data()
        
        if not last_week_data.empty:
            # Temperatūros tendencijos grafikas
            temp_plot_path = visualizer.plot_temperature_trend(
                historical_data=last_week_data,
                forecast_data=forecast_data,
                title="Temperatūros kaita (paskutinė savaitė + prognozė)"
            )
            
            if temp_plot_path:
                print(f"✅ Temperatūros grafikas išsaugotas: {temp_plot_path}")
            
            # Oro sąlygų suvestinė
            dashboard_path = visualizer.plot_weather_dashboard(
                last_week_data,
                title="Oro sąlygų suvestinė (paskutinė savaitė)"
            )
            
            if dashboard_path:
                print(f"✅ Oro sąlygų suvestinė išsaugota: {dashboard_path}")
        
        # 7. Temperatūros interpoliacija
        print("\n  Atliekame temperatūros interpoliaciją...")
        interpolator = TemperatureInterpolator()
        
        if 'airTemperature' in historical_data.columns:
            # Imame paskutinės dienos duomenis interpoliacijai
            last_day_data = historical_data.tail(24)  # Paskutinės 24 valandos
            temp_series = last_day_data['airTemperature']
            
            # Interpoliuojame iki 5 minučių dažnio
            interpolation_stats = interpolator.interpolate_with_statistics(
                temp_series, target_frequency='5T', method='linear'
            )
            
            interpolator.print_interpolation_summary(interpolation_stats)
            
            # Išsaugome interpoliuotus duomenis
            if interpolation_stats.get('interpolated_data') is not None:
                interpolated_df = interpolation_stats['interpolated_data'].to_frame('temperature')
                interpolated_df.to_csv('data/interpolated_temperature.csv')
                print("✅ Interpoliuoti duomenys išsaugoti: data/interpolated_temperature.csv")
        
        # 8. Išsaugome duomenis
        print("\n  Išsaugome duomenis...")
        
        # Sukuriame data katalogą jei neegzistuoja
        os.makedirs('data', exist_ok=True)
        
        # Išsaugome istorinius duomenis
        historical_data.to_csv('data/historical_data.csv')
        print("✅ Istoriniai duomenys išsaugoti: data/historical_data.csv")
        
        # Išsaugome prognozės duomenis jei yra
        if forecast_data is not None and not forecast_data.empty:
            forecast_data.to_csv('data/forecast_data.csv')
            print("✅ Prognozės duomenys išsaugoti: data/forecast_data.csv")
        
        # Išsaugome analizės rezultatus
        results_summary = {
            'analysis_date': datetime.now().isoformat(),
            'location': 'Vilnius',
            'data_period': f"{start_date}  {end_date}",
            'historical_records': len(historical_data),
            'forecast_records': len(forecast_data) if forecast_data is not None else 0,
            'annual_averages': annual_averages,
            'day_night_analysis': day_night_analysis,
            'weekend_rain_forecast': weekend_rain
        }
        
        import json
        with open('data/analysis_results.json', 'w', encoding='utf8') as f:
            json.dump(results_summary, f, ensure_ascii=False, indent=2, default=str)
        
        print("✅ Analizės rezultatai išsaugoti: data/analysis_results.json")
        
        print("\n" + "=" * 60)
        print("PROGRAMA SĖKMINGAI BAIGTA!")
        print(f"Duomenys išsaugoti 'data' kataloge")
        print(f"Grafikai išsaugoti 'plots' kataloge")
        print(f"Programos veikimo žurnalas: weather_analysis.log")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n❌ Programa nutraukta vartotojo")
    except Exception as e:
        logger.error(f"Programos klaida: {e}")
        print(f"\n❌ Programos klaida: {e}")
        print("Žiūrėkite weather_analysis.log failą dėl detalesnės informacijos")

if __name__ == "__main__":
    main()
