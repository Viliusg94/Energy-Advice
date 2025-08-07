# Naudojimo vadovas  Lietuvos oro duomenÅ³ analizÄ—s sistema

## ApÅ¾valga

Å is vadovas apraÅo kaip naudoti Lietuvos oro duomenÅ³ analizÄ—s sistemÄ… praktiniams tikslams. Sistema skirta oro duomenÅ³ nuskaitymui iÅ meteo.lt API, jÅ³ analizei ir vizualizacijai.

## Greitasis startas

### 1. Paprasta analizÄ—

```python
# Importuokite reikalingas klases
from src.weather_api import WeatherAPI
from src.data_analysis import WeatherAnalyzer

# Sukurkite API objektÄ…
api = WeatherAPI("vilnius")

# Nuskaitykite paskutinÄ—s savaitÄ—s duomenis
from datetime import datetime, timedelta
end_date = datetime.now().strftime("%Y%m%d")
start_date = (datetime.now()  timedelta(days=7)).strftime("%Y%m%d")

data = api.get_historical_data(start_date, end_date)

# Atlikite analizÄ™
analyzer = WeatherAnalyzer(data)
results = analyzer.calculate_annual_averages()

print(f"VidutinÄ— temperatÅ«ra: {results['average_temperature']:.1f}Ā°C")
```

### 2. Grafiko kÅ«rimas

```python
from src.visualization import WeatherVisualizer

# Sukurkite vizualizacijos objektÄ…
visualizer = WeatherVisualizer("my_plots")

# Sukurkite temperatÅ«ros grafikÄ…
visualizer.plot_temperature_trend(
    historical_data=data,
    title="Vilniaus temperatÅ«ra (paskutinÄ— savaitÄ—)"
)
```

## DetalÅ«s naudojimo scenarijai

### Scenarijus 1: MÄ—nesio oro analizÄ—

```python
import pandas as pd
from datetime import datetime, timedelta
from src.weather_api import WeatherAPI
from src.data_analysis import WeatherAnalyzer
from src.visualization import WeatherVisualizer

def analyze_monthly_weather(city="vilnius", year=2024, month=1):
    """
    Analizuoja mÄ—nesio oro duomenis
    """
    # Nustatome mÄ—nesio datas
    start_date = f"{year}{month:02d}01"
    if month == 12:
        end_date = f"{year+1}0101"
    else:
        end_date = f"{year}{month+1:02d}01"
    
    # API uÅ¾klausa
    api = WeatherAPI(city)
    data = api.get_historical_data(start_date, end_date)
    
    if data is None or data.empty:
        print(f"NÄ—ra duomenÅ³ {year}{month:02d} mÄ—nesiui")
        return None
    
    # AnalizÄ—
    analyzer = WeatherAnalyzer(data)
    
    # ApskaiÄ¨iuojame statistikas
    monthly_stats = {
        'vidurkiai': analyzer.calculate_annual_averages(),
        'dienos_naktis': analyzer.analyze_day_night_temperature(),
        'duomenu_skaicius': len(data)
    }
    
    # Vizualizacija
    visualizer = WeatherVisualizer("monthly_plots")
    
    # Detalus oro sÄ…lygÅ³ dashboard
    dashboard_path = visualizer.plot_weather_dashboard(
        data, 
        title=f"{city.title()} oro sÄ…lygos  {year}{month:02d}",
        save_file=f"weather_{city}_{year}_{month:02d}.png"
    )
    
    # Koreliacijos analizÄ—
    corr_path = visualizer.plot_correlation_matrix(
        data,
        title=f"Oro parametrÅ³ koreliacija  {city.title()}",
        save_file=f"correlation_{city}_{year}_{month:02d}.png"
    )
    
    return {
        'data': data,
        'statistics': monthly_stats,
        'plots': [dashboard_path, corr_path]
    }

# Naudojimo pavyzdys
results = analyze_monthly_weather("vilnius", 2024, 1)
if results:
    print("MÄ—nesio analizÄ— baigta!")
    print(f"DuomenÅ³ ÄÆraÅÅ³: {results['statistics']['duomenu_skaicius']}")
    print(f"Vid. temperatÅ«ra: {results['statistics']['vidurkiai']['average_temperature']:.1f}Ā°C")
```

### Scenarijus 2: MiestÅ³ palyginimas

```python
def compare_cities(cities=["vilnius", "kaunas", "klaipeda"], days=30):
    """
    Palygina skirtingÅ³ miestÅ³ oro sÄ…lygas
    """
    from datetime import datetime, timedelta
    import matplotlib.pyplot as plt
    
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now()  timedelta(days=days)).strftime("%Y%m%d")
    
    city_data = {}
    city_stats = {}
    
    # Nuskaitome duomenis visiems miestams
    for city in cities:
        print(f"Nuskaitome {city} duomenis...")
        
        api = WeatherAPI(city)
        data = api.get_historical_data(start_date, end_date)
        
        if data is not None and not data.empty:
            analyzer = WeatherAnalyzer(data)
            stats = analyzer.calculate_annual_averages()
            
            city_data[city] = data
            city_stats[city] = stats
            print(f"ā… {city}: {len(data)} ÄÆraÅÅ³")
        else:
            print(f"ā¯ {city}: NÄ—ra duomenÅ³")
    
    # Sukuriame palyginimo grafikÄ…
    if city_stats:
        plt.figure(figsize=(15, 10))
        
        # 2x2 subplot'ai palyginimui
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'MiestÅ³ oro sÄ…lygÅ³ palyginimas ({days} dienÅ³)', fontsize=16)
        
        # TemperatÅ«ros palyginimas
        ax = axes[0, 0]
        temps = [city_stats[city].get('average_temperature', 0) for city in cities if city in city_stats]
        city_names = [city.title() for city in cities if city in city_stats]
        bars = ax.bar(city_names, temps, color=['blue', 'green', 'red', 'orange', 'purple'][:len(city_names)])
        ax.set_title('VidutinÄ— temperatÅ«ra')
        ax.set_ylabel('Ā°C')
        
        # Pridedame reikÅmes ant stulpeliÅ³
        for bar, temp in zip(bars, temps):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{temp:.1f}Ā°C', ha='center', va='bottom')
        
        # DrÄ—gmÄ—s palyginimas
        ax = axes[0, 1]
        humidity = [city_stats[city].get('average_humidity', 0) for city in cities if city in city_stats]
        bars = ax.bar(city_names, humidity, color=['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'plum'][:len(city_names)])
        ax.set_title('VidutinÄ— drÄ—gmÄ—')
        ax.set_ylabel('%')
        
        for bar, hum in zip(bars, humidity):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{hum:.1f}%', ha='center', va='bottom')
        
        # VÄ—jo greiÄ¨io palyginimas
        ax = axes[1, 0]
        wind_speeds = [city_stats[city].get('average_wind_speed', 0) for city in cities if city in city_stats]
        bars = ax.bar(city_names, wind_speeds, color=['skyblue', 'lightsteelblue', 'powderblue', 'lightcyan', 'azure'][:len(city_names)])
        ax.set_title('Vidutinis vÄ—jo greitis')
        ax.set_ylabel('m/s')
        
        for bar, wind in zip(bars, wind_speeds):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                   f'{wind:.1f}', ha='center', va='bottom')
        
        # SlÄ—gio palyginimas
        ax = axes[1, 1]
        pressures = [city_stats[city].get('average_pressure', 0) for city in cities if city in city_stats]
        bars = ax.bar(city_names, pressures, color=['mediumpurple', 'mediumorchid', 'mediumslateblue', 'mediumturquoise', 'mediumseagreen'][:len(city_names)])
        ax.set_title('Vidutinis slÄ—gis')
        ax.set_ylabel('hPa')
        
        for bar, press in zip(bars, pressures):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{press:.0f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(f'city_comparison_{days}days.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Spausdiname detalizuotÄ… palyginimÄ…
        print(f"\nš“ MIESTÅ² PALYGINIMAS ({days} dienÅ³):")
        print("=" * 60)
        
        for city in cities:
            if city in city_stats:
                stats = city_stats[city]
                print(f"\nš¸™ļø¸ {city.upper()}:")
                print(f"   šļø¸ TemperatÅ«ra: {stats.get('average_temperature', 0):.1f}Ā°C")
                print(f"   š’§ DrÄ—gmÄ—: {stats.get('average_humidity', 0):.1f}%")
                print(f"   š’Ø VÄ—jo greitis: {stats.get('average_wind_speed', 0):.1f} m/s")
                print(f"   š“ SlÄ—gis: {stats.get('average_pressure', 0):.0f} hPa")
    
    return city_data, city_stats

# Naudojimo pavyzdys
city_data, city_stats = compare_cities(["vilnius", "kaunas", "klaipeda"], days=7)
```

### Scenarijus 3: TemperatÅ«ros prognozÄ—s su interpoliacija

```python
def detailed_temperature_forecast(city="vilnius", interpolation_freq="5T"):
    """
    Detalios temperatÅ«ros prognozÄ—s su interpoliacija
    """
    from src.weather_api import WeatherAPI
    from src.data_analysis import WeatherAnalyzer
    from src.interpolation import TemperatureInterpolator
    from src.visualization import WeatherVisualizer
    import matplotlib.pyplot as plt
    
    # Nuskaitome duomenis
    api = WeatherAPI(city)
    
    # PaskutinÄ—s 3 dienos istoriniÅ³ duomenÅ³
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now()  timedelta(days=3)).strftime("%Y%m%d")
    
    historical = api.get_historical_data(start_date, end_date)
    forecast = api.get_forecast_data()
    
    if historical is None or historical.empty:
        print("NÄ—ra istoriniÅ³ duomenÅ³")
        return None
    
    # Interpoliacija paskutinÄ—s dienos duomenims
    interpolator = TemperatureInterpolator()
    
    if 'airTemperature' in historical.columns:
        # Pasiimame paskutinÄ—s 24h duomenis
        last_24h = historical.tail(24)
        temp_series = last_24h['airTemperature'].dropna()
        
        if not temp_series.empty:
            print(f"Interpoliuojame temperatÅ«ros duomenis...")
            
            # Palyginame skirtingus metodus
            methods_comparison = interpolator.compare_interpolation_methods(
                temp_series, 
                target_frequency=interpolation_freq
            )
            
            # Paimame geriausiÄ… metodÄ…
            best_method = methods_comparison.get('recommended_method', 'linear')
            
            # Interpoliuojame
            interpolated_stats = interpolator.interpolate_with_statistics(
                temp_series,
                target_frequency=interpolation_freq,
                method=best_method
            )
            
            interpolated_temp = interpolated_stats['interpolated_data']
            
            # Vizualizacija
            plt.figure(figsize=(18, 12))
            
            # Sukuriame 3 subplot'us
            gs = plt.GridSpec(3, 1, height_ratios=[2, 1, 1])
            
            # 1. TemperatÅ«ros tendencija su prognoze
            ax1 = plt.subplot(gs[0])
            
            # Istoriniai duomenys
            ax1.plot(historical.index, historical['airTemperature'], 
                    'o', linewidth=2, markersize=4, color='blue', 
                    label=f'Istoriniai duomenys ({len(historical)} taÅkai)')
            
            # Interpoliuoti duomenys
            if interpolated_temp is not None:
                ax1.plot(interpolated_temp.index, interpolated_temp.values, 
                        '', linewidth=1, color='lightblue', alpha=0.7,
                        label=f'Interpoliuoti ({len(interpolated_temp)} taÅkai)')
            
            # PrognozÄ—s duomenys
            if forecast is not None and not forecast.empty:
                temp_col = None
                for col in ['airTemperature', 'temperature']:
                    if col in forecast.columns:
                        temp_col = col
                        break
                
                if temp_col:
                    ax1.plot(forecast.index, forecast[temp_col], 
                            's', linewidth=2, markersize=4, color='red', 
                            label=f'PrognozÄ— ({len(forecast)} taÅkai)')
            
            ax1.set_title(f'{city.title()} temperatÅ«ros analizÄ— ir prognozÄ—', fontsize=14, fontweight='bold')
            ax1.set_ylabel('TemperatÅ«ra (Ā°C)')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # 2. Interpoliacijos metodÅ³ palyginimas
            ax2 = plt.subplot(gs[1])
            
            if methods_comparison and 'methods' in methods_comparison:
                methods = list(methods_comparison['methods'].keys())
                improvements = []
                
                for method in methods:
                    method_stats = methods_comparison['methods'][method]
                    if method_stats['interpolated_data'] is not None:
                        improvements.append(method_stats['improvement_ratio'])
                    else:
                        improvements.append(0)
                
                bars = ax2.bar(methods, improvements, color=['skyblue', 'lightgreen', 'lightcoral', 'lightyellow'])
                ax2.set_title('Interpoliacijos metodÅ³ efektyvumas')
                ax2.set_ylabel('PagerÄ—jimo santykis')
                
                # PaÅ¾ymime geriausiÄ… metodÄ…
                best_idx = methods.index(best_method) if best_method in methods else 0
                bars[best_idx].set_color('gold')
                bars[best_idx].set_edgecolor('orange')
                bars[best_idx].set_linewidth(2)
            
            # 3. Statistikos palyginimas
            ax3 = plt.subplot(gs[2])
            
            # OriginalÅ«s vs interpoliuoti statistikos
            orig_stats = [temp_series.mean(), temp_series.std(), temp_series.min(), temp_series.max()]
            
            if interpolated_temp is not None:
                interp_stats = [interpolated_temp.mean(), interpolated_temp.std(), 
                              interpolated_temp.min(), interpolated_temp.max()]
            else:
                interp_stats = orig_stats
            
            x = ['Vidurkis', 'Std. nuokrypis', 'Min', 'Max']
            x_pos = range(len(x))
            
            width = 0.35
            ax3.bar([p  width/2 for p in x_pos], orig_stats, width, 
                   label='OriginalÅ«s', color='blue', alpha=0.7)
            ax3.bar([p + width/2 for p in x_pos], interp_stats, width,
                   label='Interpoliuoti', color='red', alpha=0.7)
            
            ax3.set_title('Statistikos palyginimas')
            ax3.set_ylabel('TemperatÅ«ra (Ā°C)')
            ax3.set_xticks(x_pos)
            ax3.set_xticklabels(x)
            ax3.legend()
            
            plt.tight_layout()
            plt.savefig(f'detailed_forecast_{city}.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            # Spausdiname analizÄ—s rezultatus
            print(f"\nšˇÆ DETALI TEMPERATÅŖROS ANALIZÄ–  {city.upper()}")
            print("=" * 50)
            
            print(f"\nš“ INTERPOLIACIJOS REZULTATAI:")
            print(f"   š”¢ OriginalÅ«s taÅkai: {interpolated_stats['original_points']}")
            print(f"   š”¢ Interpoliuoti taÅkai: {interpolated_stats['interpolated_points']}")
            print(f"   š“ PagerÄ—jimas: {interpolated_stats['improvement_ratio']:.1f}x")
            print(f"   š”§ Geriausias metodas: {best_method}")
            print(f"   ā¸° DaÅ¾nis: {interpolation_freq}")
            
            print(f"\nšļø¸ TEMPERATÅŖROS STATISTIKA:")
            print(f"   š“ OriginalÅ«s duomenys:")
            print(f"      Vidurkis: {interpolated_stats['original_mean']:.2f}Ā°C")
            print(f"      MinMax: {interpolated_stats['original_min']:.1f}Ā°C  {interpolated_stats['original_max']:.1f}Ā°C")
            
            if interpolated_temp is not None:
                print(f"   š“ Interpoliuoti duomenys:")
                print(f"      Vidurkis: {interpolated_stats['interpolated_mean']:.2f}Ā°C")
                print(f"      MinMax: {interpolated_stats['interpolated_min']:.1f}Ā°C  {interpolated_stats['interpolated_max']:.1f}Ā°C")
            
            return {
                'historical': historical,
                'forecast': forecast,
                'interpolated': interpolated_temp,
                'interpolation_stats': interpolated_stats,
                'methods_comparison': methods_comparison
            }
    
    return None

# Naudojimo pavyzdys
results = detailed_temperature_forecast("vilnius", "10T")
```

### Scenarijus 4: Automatizuotas ataskaitos generavimas

```python
def generate_weather_report(city="vilnius", days=7, output_format="html"):
    """
    Sukuria automatizuotÄ… oro sÄ…lygÅ³ ataskaitÄ…
    """
    import json
    from datetime import datetime, timedelta
    
    # DuomenÅ³ surinkimas
    api = WeatherAPI(city)
    
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now()  timedelta(days=days)).strftime("%Y%m%d")
    
    historical = api.get_historical_data(start_date, end_date)
    forecast = api.get_forecast_data()
    current = api.get_current_conditions()
    
    if historical is None or historical.empty:
        print("NÄ—ra duomenÅ³ ataskaitos kÅ«rimui")
        return None
    
    # AnalizÄ—
    analyzer = WeatherAnalyzer(historical, forecast)
    
    report_data = {
        'meta': {
            'city': city.title(),
            'report_date': datetime.now().isoformat(),
            'data_period': f"{start_date}  {end_date}",
            'report_days': days
        },
        'data_summary': {
            'historical_records': len(historical),
            'forecast_records': len(forecast) if forecast is not None else 0,
            'data_coverage': (len(historical) / (days * 24)) * 100  # Assuming hourly data
        },
        'current_conditions': current,
        'analysis': {
            'averages': analyzer.calculate_annual_averages(),
            'day_night': analyzer.analyze_day_night_temperature(),
            'extremes': {
                'max_temp': historical['airTemperature'].max() if 'airTemperature' in historical.columns else None,
                'min_temp': historical['airTemperature'].min() if 'airTemperature' in historical.columns else None,
                'max_wind': historical['windSpeed'].max() if 'windSpeed' in historical.columns else None,
                'max_humidity': historical['relativeHumidity'].max() if 'relativeHumidity' in historical.columns else None
            }
        }
    }
    
    # SavaitgaliÅ³ analizÄ— jei yra prognozÄ—s
    if forecast is not None:
        report_data['analysis']['weekend_rain'] = analyzer.analyze_weekend_rain_forecast()
    
    # Grafikai
    visualizer = WeatherVisualizer("report_plots")
    
    plots = []
    
    # TemperatÅ«ros tendencija
    temp_plot = visualizer.plot_temperature_trend(
        historical, forecast,
        title=f"{city.title()} temperatÅ«ros kaita",
        save_file=f"temp_trend_{city}_{days}d.png"
    )
    if temp_plot:
        plots.append(temp_plot)
    
    # Oro sÄ…lygÅ³ dashboard
    dashboard_plot = visualizer.plot_weather_dashboard(
        historical,
        title=f"{city.title()} oro sÄ…lygÅ³ suvestinÄ—",
        save_file=f"dashboard_{city}_{days}d.png"
    )
    if dashboard_plot:
        plots.append(dashboard_plot)
    
    # Koreliacijos matrica
    corr_plot = visualizer.plot_correlation_matrix(
        historical,
        title=f"{city.title()} oro parametrÅ³ koreliacija",
        save_file=f"correlation_{city}_{days}d.png"
    )
    if corr_plot:
        plots.append(corr_plot)
    
    report_data['plots'] = plots
    
    # IÅsaugome ataskaitÄ…
    if output_format.lower() == "json":
        filename = f"weather_report_{city}_{days}d.json"
        with open(filename, 'w', encoding='utf8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2, default=str)
        print(f"š“„ JSON ataskaita iÅsaugota: {filename}")
    
    elif output_format.lower() == "html":
        filename = f"weather_report_{city}_{days}d.html"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Oro sÄ…lygÅ³ ataskaita  {city.title()}</title>
            <meta charset="UTF8">
            <style>
                body {{ fontfamily: Arial, sansserif; margin: 40px; }}
                .header {{ background: #4CAF50; color: white; padding: 20px; textalign: center; }}
                .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
                .stats {{ display: grid; gridtemplatecolumns: repeat(autofit, minmax(200px, 1fr)); gap: 15px; }}
                .statbox {{ background: #f9f9f9; padding: 15px; textalign: center; borderradius: 5px; }}
                .plot {{ textalign: center; margin: 20px 0; }}
                .plot img {{ maxwidth: 100%; height: auto; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>š¤ļø¸ Oro sÄ…lygÅ³ ataskaita</h1>
                <h2>{city.title()}</h2>
                <p>Laikotarpis: {start_date}  {end_date} ({days} dienos)</p>
                <p>Ataskaita sukurta: {datetime.now().strftime('%Y%m%d %H:%M')}</p>
            </div>
            
            <div class="section">
                <h3>š“ DuomenÅ³ suvestinÄ—</h3>
                <div class="stats">
                    <div class="statbox">
                        <h4>IstoriniÅ³ ÄÆraÅÅ³</h4>
                        <p>{report_data['data_summary']['historical_records']}</p>
                    </div>
                    <div class="statbox">
                        <h4>PrognozÄ—s ÄÆraÅÅ³</h4>
                        <p>{report_data['data_summary']['forecast_records']}</p>
                    </div>
                    <div class="statbox">
                        <h4>DuomenÅ³ aprÄ—ptis</h4>
                        <p>{report_data['data_summary']['data_coverage']:.1f}%</p>
                    </div>
                </div>
            </div>
        """
        
        # DabartinÄ—s sÄ…lygos
        if current:
            html_content += f"""
            <div class="section">
                <h3>šļø¸ DabartinÄ—s oro sÄ…lygos</h3>
                <div class="stats">
            """
            
            if 'airTemperature' in current:
                html_content += f"""
                    <div class="statbox">
                        <h4>TemperatÅ«ra</h4>
                        <p>{current['airTemperature']}Ā°C</p>
                    </div>
                """
            
            if 'relativeHumidity' in current:
                html_content += f"""
                    <div class="statbox">
                        <h4>DrÄ—gmÄ—</h4>
                        <p>{current['relativeHumidity']}%</p>
                    </div>
                """
            
            if 'windSpeed' in current:
                html_content += f"""
                    <div class="statbox">
                        <h4>VÄ—jo greitis</h4>
                        <p>{current['windSpeed']} m/s</p>
                    </div>
                """
            
            html_content += "</div></div>"
        
        # Vidurkiai
        if report_data['analysis']['averages']:
            averages = report_data['analysis']['averages']
            html_content += f"""
            <div class="section">
                <h3>š“ Laikotarpio vidurkiai</h3>
                <div class="stats">
                    <div class="statbox">
                        <h4>Vid. temperatÅ«ra</h4>
                        <p>{averages.get('average_temperature', 0):.1f}Ā°C</p>
                    </div>
                    <div class="statbox">
                        <h4>Vid. drÄ—gmÄ—</h4>
                        <p>{averages.get('average_humidity', 0):.1f}%</p>
                    </div>
                    <div class="statbox">
                        <h4>Vid. vÄ—jo greitis</h4>
                        <p>{averages.get('average_wind_speed', 0):.1f} m/s</p>
                    </div>
                    <div class="statbox">
                        <h4>Vid. slÄ—gis</h4>
                        <p>{averages.get('average_pressure', 0):.0f} hPa</p>
                    </div>
                </div>
            </div>
            """
        
        # KraÅtutinÄ—s reikÅmÄ—s
        extremes = report_data['analysis']['extremes']
        if any(extremes.values()):
            html_content += f"""
            <div class="section">
                <h3>š”ā¯„ļø¸ KraÅtutinÄ—s reikÅmÄ—s</h3>
                <div class="stats">
            """
            
            if extremes['max_temp'] is not None:
                html_content += f"""
                    <div class="statbox">
                        <h4>Max temperatÅ«ra</h4>
                        <p>{extremes['max_temp']:.1f}Ā°C</p>
                    </div>
                """
            
            if extremes['min_temp'] is not None:
                html_content += f"""
                    <div class="statbox">
                        <h4>Min temperatÅ«ra</h4>
                        <p>{extremes['min_temp']:.1f}Ā°C</p>
                    </div>
                """
            
            if extremes['max_wind'] is not None:
                html_content += f"""
                    <div class="statbox">
                        <h4>Max vÄ—jo greitis</h4>
                        <p>{extremes['max_wind']:.1f} m/s</p>
                    </div>
                """
            
            if extremes['max_humidity'] is not None:
                html_content += f"""
                    <div class="statbox">
                        <h4>Max drÄ—gmÄ—</h4>
                        <p>{extremes['max_humidity']:.1f}%</p>
                    </div>
                """
            
            html_content += "</div></div>"
        
        # Grafikai
        if plots:
            html_content += """
            <div class="section">
                <h3>š“ Grafikai</h3>
            """
            
            for plot_path in plots:
                plot_name = plot_path.split('/')[1] if '/' in plot_path else plot_path.split('\\')[1]
                html_content += f"""
                <div class="plot">
                    <h4>{plot_name}</h4>
                    <img src="{plot_path}" alt="{plot_name}">
                </div>
                """
            
            html_content += "</div>"
        
        html_content += """
            <div class="section">
                <h3>ā„¹ļø¸ Informacija</h3>
                <p>DuomenÅ³ Åaltinis: <a href="https://api.meteo.lt/">Lietuvos hidrometeorologijos tarnyba</a></p>
                <p>Ataskaita sukurta automatiÅkai naudojant Weather Analysis System</p>
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w', encoding='utf8') as f:
            f.write(html_content)
        
        print(f"š“„ HTML ataskaita iÅsaugota: {filename}")
    
    # Spausdiname pagrindinius rezultatus
    print(f"\nš“‹ ATASKAITOS SUVESTINÄ–  {city.upper()}")
    print("=" * 40)
    print(f"š“… Laikotarpis: {days} dienos")
    print(f"š“ IstoriniÅ³ ÄÆraÅÅ³: {report_data['data_summary']['historical_records']}")
    print(f"š”® PrognozÄ—s ÄÆraÅÅ³: {report_data['data_summary']['forecast_records']}")
    print(f"š“ DuomenÅ³ aprÄ—ptis: {report_data['data_summary']['data_coverage']:.1f}%")
    
    if report_data['analysis']['averages']:
        avg = report_data['analysis']['averages']
        print(f"\nšļø¸ Vid. temperatÅ«ra: {avg.get('average_temperature', 0):.1f}Ā°C")
        print(f"š’§ Vid. drÄ—gmÄ—: {avg.get('average_humidity', 0):.1f}%")
        print(f"š’Ø Vid. vÄ—jo greitis: {avg.get('average_wind_speed', 0):.1f} m/s")
    
    print(f"\nš“ Sukurti grafikai: {len(plots)}")
    print(f"š“„ Ataskaita iÅsaugota: {filename}")
    
    return report_data

# Naudojimo pavyzdys
report = generate_weather_report("vilnius", days=14, output_format="html")
```

## Praktiniai patarimai

### 1. Performance optimizavimas

```python
# Cache API uÅ¾klausas
from functools import lru_cache

@lru_cache(maxsize=32)
def cached_weather_data(city, start_date, end_date):
    api = WeatherAPI(city)
    return api.get_historical_data(start_date, end_date)

# Naudokite pandas optimizacijas
import pandas as pd

# Skaitant didelius CSV failus
data = pd.read_csv('large_weather_data.csv', 
                   parse_dates=['timestamp'],
                   index_col='timestamp',
                   chunksize=10000)

# Atminties optimizavimas
historical_data = historical_data.astype({
    'airTemperature': 'float32',
    'relativeHumidity': 'float32',
    'windSpeed': 'float32'
})
```

### 2. KlaidÅ³ apdorojimas

```python
import logging
from time import sleep

def robust_api_call(api_func, max_retries=3, delay=5):
    """
    API uÅ¾klausÅ³ su retry logika
    """
    for attempt in range(max_retries):
        try:
            result = api_func()
            if result is not None:
                return result
        except Exception as e:
            logging.warning(f"API klaida (bandymas {attempt + 1}): {e}")
            if attempt < max_retries  1:
                sleep(delay)
    
    logging.error("API uÅ¾klausÄ… nepavyko ÄÆvykdyti po visÅ³ bandymÅ³")
    return None

# Naudojimas
api = WeatherAPI("vilnius")
data = robust_api_call(
    lambda: api.get_historical_data("20240101", "20240131")
)
```

### 3. Batch processing

```python
def process_multiple_cities_batch(cities, start_date, end_date):
    """
    Masinis miestÅ³ duomenÅ³ apdorojimas
    """
    import time
    
    results = {}
    
    for i, city in enumerate(cities):
        print(f"Apdorojamas miestas {i+1}/{len(cities)}: {city}")
        
        try:
            api = WeatherAPI(city)
            data = api.get_historical_data(start_date, end_date)
            
            if data is not None and not data.empty:
                analyzer = WeatherAnalyzer(data)
                results[city] = {
                    'data': data,
                    'averages': analyzer.calculate_annual_averages(),
                    'day_night': analyzer.analyze_day_night_temperature()
                }
                
                print(f"ā… {city}: {len(data)} ÄÆraÅÅ³")
            else:
                print(f"ā¯ {city}: NÄ—ra duomenÅ³")
                results[city] = None
        
        except Exception as e:
            print(f"ā¯ {city}: Klaida  {e}")
            results[city] = None
        
        # Pause tarp uÅ¾klausÅ³ kad neperkrauti API
        if i < len(cities)  1:
            time.sleep(2)
    
    return results

# Naudojimas
cities = ["vilnius", "kaunas", "klaipeda", "siauliai", "panevezys"]
batch_results = process_multiple_cities_batch(cities, "20240101", "20240131")
```

### 4. DuomenÅ³ eksportavimas

```python
def export_analysis_results(data, filename_prefix="weather_export"):
    """
    Eksportuoja analizÄ—s rezultatus ÄÆvairiais formatais
    """
    import json
    import pickle
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # CSV eksportas
    if isinstance(data, pd.DataFrame):
        csv_file = f"{filename_prefix}_{timestamp}.csv"
        data.to_csv(csv_file, index=True)
        print(f"š“„ CSV eksportas: {csv_file}")
    
    # JSON eksportas (dictionary rezultatams)
    if isinstance(data, dict):
        json_file = f"{filename_prefix}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        print(f"š“„ JSON eksportas: {json_file}")
    
    # Pickle eksportas (Python objektams)
    pickle_file = f"{filename_prefix}_{timestamp}.pkl"
    with open(pickle_file, 'wb') as f:
        pickle.dump(data, f)
    print(f"š“„ Pickle eksportas: {pickle_file}")
    
    # Excel eksportas (jei pandas DataFrame)
    if isinstance(data, pd.DataFrame):
        try:
            excel_file = f"{filename_prefix}_{timestamp}.xlsx"
            data.to_excel(excel_file, index=True, engine='openpyxl')
            print(f"š“„ Excel eksportas: {excel_file}")
        except ImportError:
            print("ā ļø¸ Excel eksportas neprieinamas  ÄÆdiekite openpyxl")

# Naudojimo pavyzdÅ¾iai
export_analysis_results(historical_data, "vilnius_historical")
export_analysis_results(analysis_results, "vilnius_analysis")
```



## ā ļø¸ Pastabos ir apribojimai

1. **API limitai**: Nenaudokite per daÅ¾nai  rekomenduojama 12 sekundÄ—s tarp uÅ¾klausÅ³
2. **DuomenÅ³ aprÄ—ptis**: Istoriniai duomenys gali bÅ«ti ribotos apimties
3. **Laiko zonos**: Visi duomenys automatiÅkai konvertuojami ÄÆ Lietuvos laiko zonÄ…
4. **Internetinis ryÅys**: Reikalingas stabilas ryÅys su api.meteo.lt

**Daugiau informacijos ir pavyzdÅ¾iÅ³ rasite API dokumentacijoje ir Github repozitorijoje.**
