# Naudojimo vadovas - Lietuvos oro duomenų analizės sistema

## Turinys

1. [Greitas startas](#greitas-startas)
2. [Pagrindinės funkcijos](#pagrindinės-funkcijos)
3. [Praktiniai pavyzdžiai](#praktiniai-pavyzdžiai)
4. [Pažengusiems naudotojams](#pažengusiems-naudotojams)
5. [Dažniausi klausimai](#dažniausi-klausimai)
6. [Trikčių šalinimas](#trikčių-šalinimas)

## Greitas startas

### 1. Programos paleidimas 

```bash
# Aktyvuokite virtual environment
source weather_env/bin/activate  # macOS/Linux
weather_env\Scripts\activate     # Windows

# Paleiskite pagrindinę programą
python main.py
```

Programa automatiškai:
- Prisijungs prie meteo.lt API
- Parsisiųs paskutinių 30 dienų oro duomenis Vilniui
- Atliks išsamią analizę
- Sukurs vizualizacijas `plots/` kataloge
- Išsaugos duomenis `data/` kataloge

### 2. Interaktyvus režimas

```bash
python main.py
```

Programos menu:
```
1. Standartinė analizė (Vilnius)
2. Kelių miestų palyginimas  
3. Išeiti
```

## Pagrindinės funkcijos

### API duomenų gavimas

#### Istoriniai duomenys
```python
from src.weather_api import WeatherAPI
from datetime import datetime, timedelta

# Sukuriamas API objektas
api = WeatherAPI('vilnius')

# Nustatomas datos intervalas
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

# Gaunami duomenys
data = api.get_historical_data(
    start_date.strftime('%Y-%m-%d'),
    end_date.strftime('%Y-%m-%d')
)

print(f"Gauti duomenys: {len(data)} įrašų")
print(data.head())
```

#### Prognozės duomenys
```python
# Gauti 5 dienų prognozę
forecast = api.get_forecast_data(days=5)

if forecast is not None:
    print("Ateities temperatūros:")
    print(forecast['temperatura'].head(10))
```

#### Dabartiniai duomenys
```python
current = api.get_current_weather()
if current:
    print(f"Dabar: {current.get('airTemperature', 'N/A')}°C")
    print(f"Drėgmė: {current.get('relativeHumidity', 'N/A')}%")
```

### Duomenų analizė

#### Metiniai vidurkiai
```python
from src.data_analysis import WeatherAnalyzer

analyzer = WeatherAnalyzer(historical_data, forecast_data)
averages = analyzer.calculate_yearly_averages()

print("METINIAI VIDURKIAI:")
for param, value in averages.items():
    print(f"  {param.replace('_', ' ').title()}: {value}")
```

#### Dienos ir nakties analizė
```python
day_night = analyzer.analyze_day_night_temperature()

print("\nDIENOS/NAKTIES TEMPERATŪRA:")
if 'vidutinė_dienos_temperatūra' in day_night:
    print(f"  Dienos vidurkis: {day_night['vidutinė_dienos_temperatūra']:.1f}°C")
if 'vidutinė_nakties_temperatūra' in day_night:  
    print(f"  Nakties vidurkis: {day_night['vidutinė_nakties_temperatūra']:.1f}°C")
if 'dienos_nakties_skirtumas' in day_night:
    print(f"  Skirtumas: {day_night['dienos_nakties_skirtumas']:.1f}°C")
```

#### Savaitgalių lietaus prognozė
```python
weekend_rain = analyzer.analyze_weekend_rain_forecast()

print("\nSAVAITGALIŲ LIETAUS PROGNOZĖ:")
print(f"  Iš viso savaitgalių: {weekend_rain.get('savaitgalių_skaičius', 0)}")
print(f"  Su lietumi: {weekend_rain.get('savaitgaliai_su_lietumi', 0)}")
print(f"  Tikimybė: {weekend_rain.get('lietaus_tikimybė_procentais', 0)}%")

# Detali informacija
for detail in weekend_rain.get('savaitgalių_detalizacija', []):
    status = "Lietingas" if detail['lietaus_prognozė'] else "Sausas"
    print(f"  {detail['data']}: {status} ({detail['vidutiniai_krituliai']} mm)")
```

### Vizualizacija

#### Temperatūros grafikas
```python
from src.visualization import WeatherVisualizer

visualizer = WeatherVisualizer(historical_data, forecast_data)

# Temperatūros tendencijų grafikas
temp_plot = visualizer.plot_temperature_trend(days_back=14, forecast_days=7)
print(f"Temperatūros grafikas: {temp_plot}")
```

#### Oro sąlygų dashboard
```python
# 4-in-1 dashboard su visais parametrais
dashboard = visualizer.create_weather_dashboard()
print(f"Dashboard: {dashboard}")
```

#### Koreliacijos matrica
```python
correlations = analyzer.calculate_correlations()
heatmap = visualizer.plot_correlation_heatmap(correlations)
print(f"Koreliacijos matrica: {heatmap}")
```

#### Kritulių analizė
```python
precipitation_plot = visualizer.plot_precipitation_analysis()
print(f"Kritulių analizė: {precipitation_plot}")
```

### Temperatūros interpoliacija

#### Pagrindinė interpoliacija
```python
from src.interpolation import TemperatureInterpolator

# Sukuriamas interpoliatorius
interpolator = TemperatureInterpolator(historical_data['temperatura'])

# Tiesinė interpoliacija iki 5 min dažnio
interpolated = interpolator.interpolate_to_5min('linear')

print(f"Originalūs duomenys: {len(historical_data)} taškų")
print(f"Interpoliuoti: {len(interpolated)} taškų")
print(f"Tankumas padidėjo: {len(interpolated) / len(historical_data):.1f}x")
```

#### Metodų palyginimas
```python
# Palyginti visus metodus
comparison = interpolator.compare_methods()

print("\nINTERPOLIACIJOS METODŲ PALYGINIMAS:")
for method, results in comparison['metodų_palyginimas'].items():
    if 'klaida' not in results:
        print(f"  {method.upper()}:")
        print(f"    Taškai: {results['taškų_skaičius']}")
        print(f"    Laikas: {results['interpoliacijos_laikas_s']}s")
        
        metrics = results.get('kokybės_metrikos', {})
        if 'vidurkis' in metrics:
            print(f"    Vidurkis: {metrics['vidurkis']}°C")
```

#### Interpoliacijos validavimas
```python
# Validuoti interpoliacijos tikslumą
validation = interpolator.validate_interpolation(test_ratio=0.15)

print("\nVALIDACIJOS REZULTATAI:")
for method, results in validation['metodų_validacija'].items():
    if 'klaida' not in results:
        print(f"  {method.upper()}:")
        print(f"    MAE: {results['vidutinė_absoliuti_klaida']:.3f}°C")
        print(f"    RMSE: {results['šaknies_kvadratinė_klaida']:.3f}°C")
        print(f"    Max klaida: {results['maksimali_klaida']:.3f}°C")
```

#### Duomenų eksportavimas
```python
# Išsaugoti interpoliuotus duomenis
success = interpolator.export_interpolated_data('data/temp_5min.csv', 'csv')
if success:
    print("Duomenys išsaugoti: data/temp_5min.csv")
    
# Įvairi formatai
interpolator.export_interpolated_data('data/temp_5min.xlsx', 'excel')
interpolator.export_interpolated_data('data/temp_5min.json', 'json')
```

## Praktiniai pavyzdžiai

### Pavyzdys 1: Savaitės oro analizė

```python
from src.weather_api import WeatherAPI
from src.data_analysis import WeatherAnalyzer
from src.visualization import WeatherVisualizer
from datetime import datetime, timedelta

def weekly_weather_analysis():
    """Savaitės oro sąlygų analizė"""
    
    # 1. Gauti duomenis
    api = WeatherAPI('vilnius')
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    data = api.get_historical_data(
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )
    
    if data is None:
        print("Nepavyko gauti duomenų")
        return
        
    # 2. Analizė
    analyzer = WeatherAnalyzer(data)
    
    # Temperatūros statistikos
    temp_stats = {
        'vidurkis': data['temperatura'].mean(),
        'maksimumas': data['temperatura'].max(),
        'minimumas': data['temperatura'].min(),
        'standartinis_nuokrypis': data['temperatura'].std()
    }
    
    print("SAVAITĖS TEMPERATŪROS STATISTIKOS:")
    for key, value in temp_stats.items():
        print(f"  {key.title()}: {value:.1f}°C")
        
    # Lietingi periodai
    rainy_periods = data[data['krituliai'] > 0]
    rain_hours = len(rainy_periods)
    rain_percentage = (rain_hours / len(data)) * 100
    
    print(f"\nKRITULIŲ STATISTIKA:")
    print(f"  Lietingų valandų: {rain_hours} iš {len(data)}")
    print(f"  Procentualiai: {rain_percentage:.1f}%")
    print(f"  Bendras kritulių kiekis: {data['krituliai'].sum():.1f}mm")
    
    # 3. Vizualizacija
    visualizer = WeatherVisualizer(data)
    plots = [
        visualizer.create_weather_dashboard(),
        visualizer.plot_precipitation_analysis()
    ]
    
    print(f"\nSukurti grafikai:")
    for plot in plots:
        if plot:
            print(f"  - {plot}")

# Paleisti analizę
weekly_weather_analysis()
```

### Pavyzdys 2: Miestų palyginimas

```python
def compare_cities(cities=['vilnius', 'kaunas', 'klaipeda'], days=14):
    """Kelių miestų oro sąlygų palyginimas"""
    
    city_data = {}
    city_stats = {}
    
    print(f"Lyginami miestai: {', '.join(cities)}")
    print("Nuskaitomi duomenys...")
    
    # Gauti duomenis visiems miestams
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    for city in cities:
        try:
            api = WeatherAPI(city)
            data = api.get_historical_data(
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d')
            )
            
            if data is not None and not data.empty:
                city_data[city] = data
                
                # Apskaičiuoti statistikas
                city_stats[city] = {
                    'vidutinė_temperatūra': data['temperatura'].mean(),
                    'vidutinė_drėgmė': data['dregme'].mean(),
                    'vidutinis_vėjas': data['vejo_greitis'].mean(),
                    'kritulių_suma': data['krituliai'].sum(),
                    'duomenų_kiekis': len(data)
                }
                
                print(f"  {city.title()}: {len(data)} įrašų")
            else:
                print(f"  {city.title()}: Nepavyko gauti duomenų")
                
        except Exception as e:
            print(f"  {city.title()}: Klaida - {e}")
    
    # Atspausdinti palyginimą
    if city_stats:
        print("\nMIESTŲ PALYGINIMAS:")
        print(f"{'Miestas':<12} {'Temp°C':<8} {'Drėgmė%':<8} {'Vėjas m/s':<10} {'Krituliai mm':<12}")
        print("-" * 50)
        
        for city, stats in city_stats.items():
            print(f"{city.title():<12} "
                  f"{stats['vidutinė_temperatūra']:<8.1f} "
                  f"{stats['vidutinė_drėgmė']:<8.1f} "
                  f"{stats['vidutinis_vėjas']:<10.1f} "
                  f"{stats['kritulių_suma']:<12.1f}")
    
    # Vizualizacija
    if len(city_data) > 1:
        visualizer = WeatherVisualizer()
        comparison_plot = visualizer.plot_city_comparison(city_data)
        if comparison_plot:
            print(f"\nMiestų palyginimo grafikas: {comparison_plot}")
            
    return city_data, city_stats

# Paleisti palyginimą
cities_data, cities_stats = compare_cities(['vilnius', 'kaunas', 'klaipeda'])
```

### Pavyzdys 3: Temperatūros prognozės tikslumą

```python
def forecast_accuracy_analysis():
    """Analizuoti prognozės tikslumą lyginant su faktiniais duomenimis"""
    
    api = WeatherAPI('vilnius')
    
    # Gauti senos prognozės duomenis (pvz., praėjusią savaitę)
    # Tikrame projekte reikėtų saugoti senas prognozes
    
    # Gauti faktinius duomenis paskutinėms dienoms
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3)
    
    actual_data = api.get_historical_data(
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )
    
    if actual_data is None:
        print("Nepavyko gauti faktinių duomenų")
        return
        
    # Gauti dabartinę prognozę
    current_forecast = api.get_forecast_data(days=7)
    
    if current_forecast is None:
        print("Nepavyko gauti prognozės")
        return
        
    print("PROGNOZĖS ANALIZĖ:")
    print(f"Faktiniai duomenys: {len(actual_data)} įrašų")
    print(f"Prognozės duomenys: {len(current_forecast)} įrašų")
    
    # Analizuoti temperatūros tendencijas
    if not actual_data.empty and not current_forecast.empty:
        actual_trend = actual_data['temperatura'].diff().mean()
        forecast_trend = current_forecast['temperatura'].diff().mean()
        
        print(f"\nTEMPERATŪROS TENDENCIJOS:")
        print(f"  Faktinė tendencija: {actual_trend:.3f}°C/val")
        print(f"  Prognozės tendencija: {forecast_trend:.3f}°C/val")
        
        # Prognozės vizualizacija
        visualizer = WeatherVisualizer(actual_data, current_forecast)
        forecast_plot = visualizer.plot_temperature_trend(days_back=3, forecast_days=7)
        print(f"\nPrognozės grafikas: {forecast_plot}")

forecast_accuracy_analysis()
```

### Pavyzdys 4: Automatizuota kasdienė ataskaita

```python
import json
from datetime import datetime

def daily_weather_report(city='vilnius', save_to_file=True):
    """Automatizuota kasdienė oro ataskaita"""
    
    api = WeatherAPI(city)
    
    # Gauti šiandien duomenis
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    historical = api.get_historical_data(yesterday, today)
    forecast = api.get_forecast_data(days=3)
    current = api.get_current_weather()
    
    # Sukurti ataskaitos žodyną
    report = {
        'ataskaitos_data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'miestas': city.title(),
        'dabartiniai_duomenys': current,
        'vakar_statistikos': {},
        'prognozė_3_dienoms': {}
    }
    
    # Vakarykščių duomenų analizė
    if historical is not None and not historical.empty:
        yesterday_data = historical[historical.index.date == datetime.strptime(yesterday, '%Y-%m-%d').date()]
        
        if not yesterday_data.empty:
            report['vakar_statistikos'] = {
                'vidutinė_temperatūra': round(yesterday_data['temperatura'].mean(), 1),
                'maksimali_temperatūra': round(yesterday_data['temperatura'].max(), 1),
                'minimali_temperatūra': round(yesterday_data['temperatura'].min(), 1),
                'kritulių_suma': round(yesterday_data['krituliai'].sum(), 1),
                'vidutinė_drėgmė': round(yesterday_data['dregme'].mean(), 1)
            }
    
    # Prognozės suvestinė
    if forecast is not None and not forecast.empty:
        report['prognozė_3_dienoms'] = {
            'vidutinė_temperatūra': round(forecast['temperatura'].mean(), 1),
            'maksimali_temperatūra': round(forecast['temperatura'].max(), 1),
            'minimali_temperatūra': round(forecast['temperatura'].min(), 1),
            'lietaus_tikimybė': "Taip" if forecast['krituliai'].sum() > 0 else "Ne",
            'kritulių_suma': round(forecast['krituliai'].sum(), 1)
        }
    
    # Atspausdinti ataskaitą
    print(f"\n{'='*50}")
    print(f"KASDIENĖ ORO ATASKAITA - {report['miestas'].upper()}")
    print(f"Data: {report['ataskaitos_data']}")
    print(f"{'='*50}")
    
    if current:
        print(f"\nDABARTINIAI DUOMENYS:")
        print(f"  Temperatūra: {current.get('airTemperature', 'N/A')}°C")
        print(f"  Drėgmė: {current.get('relativeHumidity', 'N/A')}%")
        print(f"  Vėjas: {current.get('windSpeed', 'N/A')} m/s")
    
    if report['vakar_statistikos']:
        print(f"\nVAKAR STATISTIKOS:")
        stats = report['vakar_statistikos']
        print(f"  Temperatūra: {stats['minimali_temperatūra']}°C - {stats['maksimali_temperatūra']}°C (vid. {stats['vidutinė_temperatūra']}°C)")
        print(f"  Krituliai: {stats['kritulių_suma']} mm")
        print(f"  Drėgmė: {stats['vidutinė_drėgmė']}%")
    
    if report['prognozė_3_dienoms']:
        print(f"\nPROGNOZĖ 3 DIENOMS:")
        prog = report['prognozė_3_dienoms']
        print(f"  Temperatūra: {prog['minimali_temperatūra']}°C - {prog['maksimali_temperatūra']}°C")
        print(f"  Lietaus: {prog['lietaus_tikimybė']} ({prog['kritulių_suma']} mm)")
    
    # Išsaugoti į failą
    if save_to_file:
        filename = f"data/daily_report_{city}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        print(f"\nAtaskaita išsaugota: {filename}")
    
    return report

# Paleisti kasdienę ataskaitą
daily_report = daily_weather_report('vilnius')
```

## Pažengusiems naudotojams

### Custom analizės funkcijos

```python
def custom_temperature_analysis(data, threshold_hot=25, threshold_cold=0):
    """Pasirinktinė temperatūros analizė su slenksčiais"""
    
    if 'temperatura' not in data.columns:
        return {}
        
    hot_periods = data[data['temperatura'] > threshold_hot]
    cold_periods = data[data['temperatura'] < threshold_cold]
    comfortable_periods = data[
        (data['temperatura'] >= threshold_cold) & 
        (data['temperatura'] <= threshold_hot)
    ]
    
    total_hours = len(data)
    
    analysis = {
        'karšti_periodai': {
            'valandos': len(hot_periods),
            'procentas': (len(hot_periods) / total_hours) * 100,
            'vidutinė_temperatūra': hot_periods['temperatura'].mean() if not hot_periods.empty else 0
        },
        'šalti_periodai': {
            'valandos': len(cold_periods),
            'procentas': (len(cold_periods) / total_hours) * 100,
            'vidutinė_temperatūra': cold_periods['temperatura'].mean() if not cold_periods.empty else 0
        },
        'komfortingi_periodai': {
            'valandos': len(comfortable_periods),
            'procentas': (len(comfortable_periods) / total_hours) * 100,
            'vidutinė_temperatūra': comfortable_periods['temperatura'].mean() if not comfortable_periods.empty else 0
        }
    }
    
    return analysis

# Naudojimo pavyzdys
api = WeatherAPI('vilnius')
data = api.get_historical_data('2024-01-01', '2024-01-31')

if data is not None:
    custom_analysis = custom_temperature_analysis(data, threshold_hot=20, threshold_cold=5)
    
    print("PASIRINKTINĖ TEMPERATŪROS ANALIZĖ:")
    for category, stats in custom_analysis.items():
        print(f"  {category.upper()}:")
        print(f"    Valandų: {stats['valandos']}")
        print(f"    Procentas: {stats['procentas']:.1f}%")
        if stats['vidutinė_temperatūra']:
            print(f"    Vid. temp.: {stats['vidutinė_temperatūra']:.1f}°C")
```

### Batch duomenų nuskaitymas

```python
def download_yearly_data(city, year):
    """Parsisiunčia visų meti duomenis po mėnesį"""
    
    api = WeatherAPI(city)
    all_data = []
    
    for month in range(1, 13):
        try:
            # Apskaičiuoti mėnesio pradžią ir pabaigą
            start_date = f"{year}-{month:02d}-01"
            
            if month == 12:
                end_date = f"{year}-12-31"
            else:
                next_month = datetime(year, month + 1, 1)
                end_date = (next_month - timedelta(days=1)).strftime('%Y-%m-%d')
            
            print(f"Nuskaitomas {year}-{month:02d}...")
            
            monthly_data = api.get_historical_data(start_date, end_date)
            
            if monthly_data is not None and not monthly_data.empty:
                all_data.append(monthly_data)
                print(f"  Gauti {len(monthly_data)} įrašai")
            else:
                print(f"  Nėra duomenų")
                
            # Trumpa pauzė tarp užklausų
            import time
            time.sleep(1)
            
        except Exception as e:
            print(f"  Klaida: {e}")
            continue
    
    if all_data:
        # Sujungti visus duomenis
        yearly_data = pd.concat(all_data, sort=False)
        yearly_data.sort_index(inplace=True)
        
        # Išsaugoti
        filename = f"data/{city}_yearly_{year}.csv"
        yearly_data.to_csv(filename, encoding='utf-8')
        
        print(f"\nMetin duomenys išsaugoti: {filename}")
        print(f"Iš viso įrašų: {len(yearly_data)}")
        
        return yearly_data
    
    return None

# Naudojimo pavyzdys (atsargiai su API apkrova!)
# yearly_data = download_yearly_data('vilnius', 2023)
```

### Pažengusi vizualizacija

```python
import matplotlib.pyplot as plt
import seaborn as sns

def create_advanced_temperature_plot(data, title="Temperatūros analizė"):
    """Pažengęs temperatūros grafikas su detalėmis"""
    
    if 'temperatura' not in data.columns:
        print("Nėra temperatūros duomenų")
        return
        
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    # 1. Temperatūros laike
    axes[0, 0].plot(data.index, data['temperatura'], color='red', alpha=0.7)
    axes[0, 0].set_title('Temperatūra laike')
    axes[0, 0].set_ylabel('Temperatūra (°C)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Temperatūros pasiskirstymas
    axes[0, 1].hist(data['temperatura'], bins=30, color='skyblue', alpha=0.7, edgecolor='black')
    axes[0, 1].set_title('Temperatūros pasiskirstymas')
    axes[0, 1].set_xlabel('Temperatūra (°C)')
    axes[0, 1].set_ylabel('Dažnis')
    
    # Pridedame vidurk ir mediana linijas
    mean_temp = data['temperatura'].mean()
    median_temp = data['temperatura'].median()
    axes[0, 1].axvline(mean_temp, color='red', linestyle='--', label=f'Vidurkis: {mean_temp:.1f}°C')
    axes[0, 1].axvline(median_temp, color='green', linestyle='--', label=f'Mediana: {median_temp:.1f}°C')
    axes[0, 1].legend()
    
    # 3. Temperatūra pagal valandas
    hourly_temps = data.groupby(data.index.hour)['temperatura'].mean()
    axes[1, 0].plot(hourly_temps.index, hourly_temps.values, marker='o')
    axes[1, 0].set_title('Vidutinė temperatūra pagal valandas')
    axes[1, 0].set_xlabel('Valanda')
    axes[1, 0].set_ylabel('Temperatūra (°C)')
    axes[1, 0].set_xticks(range(0, 24, 2))
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Box plot pagal savaitės dienas
    data_with_weekday = data.copy()
    weekday_names = ['Pirmadienis', 'Antradienis', 'Trečiadienis', 'Ketvirtadienis',
                     'Penktadienis', 'Šeštadienis', 'Sekmadienis']
    data_with_weekday['weekday'] = data.index.day_name()
    
    # Konvertuojame į lietuvių kalba
    weekday_mapping = {
        'Monday': 'Pirmadienis', 'Tuesday': 'Antradienis', 'Wednesday': 'Trečiadienis',
        'Thursday': 'Ketvirtadienis', 'Friday': 'Penktadienis', 'Saturday': 'Šeštadienis',
        'Sunday': 'Sekmadienis'
    }
    data_with_weekday['weekday_lt'] = data_with_weekday['weekday'].map(weekday_mapping)
    
    weekday_order = ['Pirmadienis', 'Antradienis', 'Trečiadienis', 'Ketvirtadienis',
                     'Penktadienis', 'Šeštadienis', 'Sekmadienis']
    
    sns.boxplot(data=data_with_weekday, x='weekday_lt', y='temperatura', 
                order=weekday_order, ax=axes[1, 1])
    axes[1, 1].set_title('Temperatūros pasiskirstymas pagal savaitės dienas')
    axes[1, 1].set_xlabel('Savaitės diena')
    axes[1, 1].set_ylabel('Temperatūra (°C)')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Išsaugoti grafiką
    filename = 'plots/advanced_temperature_analysis.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Pažengęs grafikas išsaugotas: {filename}")

# Naudojimo pavyzdys
api = WeatherAPI('vilnius')
data = api.get_historical_data('2024-01-01', '2024-01-31')

if data is not None:
    create_advanced_temperature_plot(data, "Vilniaus temperatūros analizė - 2024 sausis")
```

## Dažniausi klausimai

### Q: Kaip dažnai galima daryti API užklausas?
**A:** meteo.lt API neturi aiškiai nurodyti limitų, bet rekomenduojama nedaryti daugiau nei 60 užklausų per minutę. Sistema turi integruotą retry logika.

### Q: Kokie duomenys yra prieinami?
**A:** 
- **Istoriniai duomenys**: Temperatūra, drėgmė, vėjo greitis, slėgimas, krituliai
- **Prognozės**: Iki 7 dienų į priekį
- **Dabartiniai**: Realaus laiko duomenys

### Q: Ar duomenys yra tikslūs?
**A:** Duomenys gaunami iš oficialių meteorologijos stočių, tačiau gali būti matavimo klaidų. Rekomenduojama naudoti vidurki ir tendencijas.

### Q: Kaip išsaugoti duomenis ilgalaikiam saugojimui?
**A:**
```python
# CSV formatas
data.to_csv('data/weather_data.csv', encoding='utf-8')

# Excel formatas  
data.to_excel('data/weather_data.xlsx')

# JSON formatas
data.to_json('data/weather_data.json', orient='index', date_format='iso')
```

### Q: Kaip naudoti programą serveri?
**A:** Galima automatizuoti paleidimą:

```bash
# Linux/macOS crontab - kasdien 6 ryto
0 6 * * * cd /path/to/weather-analysis && ./weather_env/bin/python main.py

# Windows Task Scheduler - naudokite GUI arba schtasks
```

### Q: Ar veiks su senesniais Python versijas?
**A:** Rekomenduojama Python 3.8+. Senesnės versijos neišbandytos ir gali neveikti.

### Q: Kaip pridėti naują miestą?
**A:** Redaguokite `src/weather_api.py` ir pridėkite naują miestą į `city_codes` žodyną:

```python
self.city_codes = {
    'vilnius': 'vilnius',
    'kaunas': 'kaunas',
    # ...
    'naujas_miestas': 'api_miestas_kodas'
}
```

### Q: Kaip keisti grafiko stilius?
**A:**
```python
import matplotlib.pyplot as plt

# Pasirinkti stilių
plt.style.use('seaborn')  # arba 'ggplot', 'classic' etc.

# Arba sukurti custom matplotlib rc paramet
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = [12, 8]
```

## Trikčių šalinimas

### Problema: "ModuleNotFoundError"

**Sprendimas:**
```bash
# Patikrinkite ar aktyvuotas virtual environment
source weather_env/bin/activate  # macOS/Linux
weather_env\Scripts\activate     # Windows

# Perkraukite priklausomybes
pip install -r requirements.txt
```

### Problema: API užklausos nepavyksta

**Patikrinkite:**
1. Internetinis ryšys
2. meteo.lt svetainė veikia
3. Braukimo arba VPN neblokuoja

**Debug kodas:**
```python
import requests

# Tiesioginis testas
response = requests.get('https://api.meteo.lt/v1/places')
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")
```

### Problema: Grafikai nerodomai

**Windows:**
```bash
pip install --upgrade matplotlib
# Arba bandykite skirtingą backend
```

**Linux:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install tcl-tk
```

### Problema: Encoding klaidos

**Windows PowerShell:**
```powershell
# Nustatykite UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

**Programoje:**
```python
import sys
import io

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

### Problema: Lėtas veikimas

**Optimizavimai:**
```python
# Sumažinkite duomenų kiekį
data = api.get_historical_data('2024-01-01', '2024-01-07')  # 7 dienos vietoj 30

# Naudokite tiesinę interpoliaciją
interpolated = interpolator.interpolate_to_5min('linear')  # greičiausia

# Sumažinkite grafikų DPI
plt.savefig('plot.png', dpi=150)  # vietoj 300
```

### Problema: Atmintis trūksta

**Sprendimai:**
```python
# Valo duomenis iš atminties
del large_dataframe
import gc
gc.collect()

# Naudokite chunks didiesius duomenis
for chunk in pd.read_csv('large_file.csv', chunksize=1000):
    process_chunk(chunk)
```

### Debug režimas

Įjunkite detalų logging:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Dabar visa veikla bus loginama detalizuotai
```

---

Ši sistema sukurta mokymosi ir analizės tikslais. Naudokite protingai ir gerbian meteo.lt API resursus!
