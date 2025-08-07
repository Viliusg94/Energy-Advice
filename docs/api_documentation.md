# API dokumentacija - Lietuvos oro duomenų analizės sistema

## Bendros informacijos

Šis dokumentas aprašo sistemą klasių API, metodų ir funkcijų naudojimą Lietuvos oro duomenų analizės sistemoje. Sistema naudoja meteo.lt API duomenų gavimui ir pateikia išsamius analizės bei vizualizacijos įrankius.

## Modulių struktūra

### src.weather_api - WeatherAPI klasė

Atsakingas už komunikaciją su meteo.lt API.

#### Konstruktorius

```python
WeatherAPI(location_code: str = "vilnius")
```

**Parametrai:**
- `location_code` (str): Miesto kodas. Palaikomi: 'vilnius', 'kaunas', 'klaipeda', 'siauliai', 'panevezys'

**Klaidos:**
- `ValueError`: Kai location_code nepalaiko

**Pavyzdys:**
```python
from src.weather_api import WeatherAPI

# Sukuriamas API objektas Vilniui
api = WeatherAPI('vilnius')

# Kitam miestui
api_kaunas = WeatherAPI('kaunas')
```

#### get_historical_data()

```python
get_historical_data(start_date: str, end_date: str) -> Optional[pd.DataFrame]
```

Gauna istorinius oro duomenis nurodytam laikotarpiui.

**Parametrai:**
- `start_date` (str): Pradžios data YYYY-MM-DD formatu
- `end_date` (str): Pabaigos data YYYY-MM-DD formatu

**Grąžina:**
- `pd.DataFrame`: Istoriniai oro duomenys su lietuviškais stulpelių pavadinimais
- `None`: Klaidos atveju

**Stulpeliai:**
- `temperatura` (float): Oro temperatūra (°C)
- `dregme` (float): Santykine drėgmė (%)
- `vejo_greitis` (float): Vėjo greitis (m/s)
- `slegimasJuros` (float): Slėgimas jūros lygyje (hPa)
- `krituliai` (float): Kritulių kiekis (mm)

**Pavyzdys:**
```python
# Gauti paskutinių 7 dienų duomenis
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=7)

data = api.get_historical_data(
    start_date.strftime('%Y-%m-%d'),
    end_date.strftime('%Y-%m-%d')
)

if data is not None:
    print(f"Gauti duomenys: {len(data)} įrašų")
    print(f"Vidutinė temperatūra: {data['temperatura'].mean():.1f}°C")
```

#### get_forecast_data()

```python
get_forecast_data(days: int = 7) -> Optional[pd.DataFrame]
```

Gauna oro prognozės duomenis.

**Parametrai:**
- `days` (int): Dienų skaičius prognozei (numatytasis: 7)

**Grąžina:**
- `pd.DataFrame`: Prognozės duomenys
- `None`: Klaidos atveju

**Pavyzdys:**
```python
# Gauti 5 dienų prognozę
forecast = api.get_forecast_data(days=5)

if forecast is not None:
    print("Temperatūros prognozė:")
    print(forecast[['temperatura']].head())
```

#### get_current_weather()

```python
get_current_weather() -> Optional[Dict[str, Any]]
```

Gauna dabartinius oro duomenis.

**Grąžina:**
- `Dict`: Dabartiniai oro duomenys
- `None`: Klaidos atveju

**Pavyzdys:**
```python
current = api.get_current_weather()
if current:
    print(f"Dabartinė temperatūra: {current.get('airTemperature')}°C")
```

### src.data_analysis - WeatherAnalyzer klasė

Atsakingas už oro duomenų statistinę analizę.

#### Konstruktorius

```python
WeatherAnalyzer(historical_data: Optional[pd.DataFrame] = None, 
                forecast_data: Optional[pd.DataFrame] = None)
```

**Parametrai:**
- `historical_data` (pd.DataFrame, optional): Istoriniai oro duomenys
- `forecast_data` (pd.DataFrame, optional): Prognozės duomenys

**Pavyzdys:**
```python
from src.data_analysis import WeatherAnalyzer

# Sukuriamas analyzer objektas
analyzer = WeatherAnalyzer(historical_data, forecast_data)
```

#### calculate_yearly_averages()

```python
calculate_yearly_averages() -> Dict[str, float]
```

Apskaičiuoja metinius oro parametrų vidurkius (paskutinių 365 dienų).

**Grąžina:**
- `Dict[str, float]`: Metinių vidurkių žodynas

**Pavyzdys:**
```python
averages = analyzer.calculate_yearly_averages()
print("Metiniai vidurkiai:")
for key, value in averages.items():
    print(f"  {key}: {value}")
```

#### analyze_day_night_temperature()

```python
analyze_day_night_temperature() -> Dict[str, float]
```

Analizuoja dienos (8:00-20:00) ir nakties temperatūros skirtumus.

**Grąžina:**
- `Dict[str, float]`: Dienos/nakties temperatūros analizė

**Grąžinami raktai:**
- `vidutinė_dienos_temperatūra`
- `vidutinė_nakties_temperatūra` 
- `maksimali_dienos_temperatūra`
- `minimali_dienos_temperatūra`
- `maksimali_nakties_temperatūra`
- `minimali_nakties_temperatūra`
- `dienos_nakties_skirtumas`

**Pavyzdys:**
```python
day_night = analyzer.analyze_day_night_temperature()
if day_night:
    print(f"Dienos temperatūra: {day_night['vidutinė_dienos_temperatūra']:.1f}°C")
    print(f"Nakties temperatūra: {day_night['vidutinė_nakties_temperatūra']:.1f}°C")
```

#### analyze_weekend_rain_forecast()

```python
analyze_weekend_rain_forecast() -> Dict[str, Any]
```

Analizuoja savaitgalių lietaus prognozes.

**Grąžina:**
- `Dict[str, Any]`: Savaitgalių lietaus prognozės analizė

**Grąžinami raktai:**
- `savaitgalių_skaičius` (int)
- `savaitgaliai_su_lietumi` (int)
- `lietaus_tikimybė_procentais` (float)
- `savaitgalių_detalizacija` (List[Dict])

**Pavyzdys:**
```python
weekend_rain = analyzer.analyze_weekend_rain_forecast()
print(f"Savaitgaliai su lietumi: {weekend_rain['savaitgaliai_su_lietumi']}")
print(f"Lietaus tikimybė: {weekend_rain['lietaus_tikimybė_procentais']}%")
```

#### calculate_correlations()

```python
calculate_correlations() -> Optional[pd.DataFrame]
```

Apskaičiuoja oro parametrų koreliacijas.

**Grąžina:**
- `pd.DataFrame`: Koreliacijos matrica
- `None`: Klaidos atveju

#### find_extremes()

```python
find_extremes() -> Dict[str, Any]
```

Suranda ekstremaliuosius oro rodiklius.

**Grąžina:**
- `Dict[str, Any]`: Ekstremumų žodynas su reikšmėmis ir datomis

#### generate_summary_report()

```python
generate_summary_report() -> Dict[str, Any]
```

Generuoja išsamią duomenų analizės ataskaitą.

**Grąžina:**
- `Dict[str, Any]`: Pilna ataskaita su visomis analizėmis

### src.visualization - WeatherVisualizer klasė

Atsakingas už oro duomenų vizualizavimą.

#### Konstruktorius

```python
WeatherVisualizer(historical_data: Optional[pd.DataFrame] = None, 
                  forecast_data: Optional[pd.DataFrame] = None,
                  plots_dir: str = "plots")
```

**Parametrai:**
- `historical_data` (pd.DataFrame, optional): Istoriniai duomenys
- `forecast_data` (pd.DataFrame, optional): Prognozės duomenys  
- `plots_dir` (str): Katalogo pavadinimas grafikams

#### plot_temperature_trend()

```python
plot_temperature_trend(days_back: int = 7, forecast_days: int = 7) -> str
```

Sukuria temperatūros tendencijų grafiką.

**Parametrai:**
- `days_back` (int): Istorinių dienų skaičius
- `forecast_days` (int): Prognozės dienų skaičius

**Grąžina:**
- `str`: Išsaugoto grafiko failo kelias

**Pavyzdys:**
```python
from src.visualization import WeatherVisualizer

visualizer = WeatherVisualizer(historical_data, forecast_data)
temp_plot = visualizer.plot_temperature_trend(days_back=14, forecast_days=5)
print(f"Grafikas išsaugotas: {temp_plot}")
```

#### create_weather_dashboard()

```python
create_weather_dashboard() -> str
```

Sukuria 4-in-1 oro sąlygų dashboard'ą su temperatura, drėgme, vėju ir slėgimu.

**Grąžina:**
- `str`: Dashboard grafiko failo kelias

#### plot_correlation_heatmap()

```python
plot_correlation_heatmap(correlation_matrix: Optional[pd.DataFrame] = None) -> str
```

Sukuria koreliacijos matricą heatmap formatu.

**Parametrai:**
- `correlation_matrix` (pd.DataFrame, optional): Koreliacijos matrica

**Grąžina:**
- `str`: Heatmap grafiko failo kelias

#### plot_precipitation_analysis()

```python
plot_precipitation_analysis() -> str
```

Sukuria kritulių analizės grafiką.

**Grąžina:**
- `str`: Kritulių grafiko failo kelias

#### create_summary_visualization()

```python
create_summary_visualization(analysis_results: Dict[str, Any]) -> str
```

Sukuria bendrą analizės rezultatų vizualizaciją.

**Parametrai:**
- `analysis_results` (Dict): Analizės rezultatų žodynas

**Grąžina:**
- `str`: Suvestinės grafiko failo kelias

### src.interpolation - TemperatureInterpolator klasė

Atsakingas už temperatūros duomenų interpoliaciją.

#### Konstruktorius

```python
TemperatureInterpolator(temperature_data: Optional[pd.Series] = None)
```

**Parametrai:**
- `temperature_data` (pd.Series, optional): Temperatūros duomenų seka

#### interpolate_to_5min()

```python
interpolate_to_5min(method: str = 'linear', polynomial_order: int = 2) -> Optional[pd.Series]
```

Interpoliuoja temperatūros duomenis iki 5 minučių dažnio.

**Parametrai:**
- `method` (str): Interpoliacijos metodas ('linear', 'time', 'polynomial', 'spline')
- `polynomial_order` (int): Polinomo eilė polynomial metodui

**Grąžina:**
- `pd.Series`: Interpoliuoti duomenys
- `None`: Klaidos atveju

**Pavyzdys:**
```python
from src.interpolation import TemperatureInterpolator

interpolator = TemperatureInterpolator(temperature_data)

# Tiesinė interpoliacija
linear_result = interpolator.interpolate_to_5min('linear')

# Polinominė interpoliacija
poly_result = interpolator.interpolate_to_5min('polynomial', polynomial_order=3)

print(f"Originalūs duomenys: {len(temperature_data)}")
print(f"Interpoliuoti duomenys: {len(linear_result)}")
```

#### compare_methods()

```python
compare_methods(methods: Optional[List[str]] = None) -> Dict[str, Any]
```

Palygina skirtingus interpoliacijos metodus.

**Parametrai:**
- `methods` (List[str], optional): Metodų sąrašas palyginimui

**Grąžina:**
- `Dict[str, Any]`: Palyginimo rezultatų žodynas

#### validate_interpolation()

```python
validate_interpolation(test_ratio: float = 0.1) -> Dict[str, Any]
```

Validuoja interpoliacijos tikslumą.

**Parametrai:**
- `test_ratio` (float): Testų duomenų dalis (0.0-1.0)

**Grąžina:**
- `Dict[str, Any]`: Validacijos rezultatų žodynas

#### export_interpolated_data()

```python
export_interpolated_data(filepath: str, format: str = 'csv') -> bool
```

Eksportuoja interpoliuotus duomenis į failą.

**Parametrai:**
- `filepath` (str): Failo kelias
- `format` (str): Failo formatas ('csv', 'excel', 'json')

**Grąžina:**
- `bool`: True jei sėkmingai eksportuota

## Klaidos valdymas

### Bendros klaidos

#### ValueError
Keliama kai pateikiami neteisingi parametrai.

```python
try:
    api = WeatherAPI('invalid_city')
except ValueError as e:
    print(f"Klaida: {e}")
```

#### API klaidos
API užklausos gali nepavykti dėl tinklo problemų arba serveri klaidų.

```python
data = api.get_historical_data('2024-01-01', '2024-01-31')
if data is None:
    print("Nepavyko gauti duomenų - patikrinkite internetinį ryšį")
```

### Logging sistema

Sistema naudoja Python logging modulį. Galite konfigūruoti logging lygį:

```python
import logging

# Nustatykite logging lygį
logging.basicConfig(level=logging.INFO)

# Arba konkretesnį log konfigūravimą
logger = logging.getLogger('weather_analysis')
logger.setLevel(logging.DEBUG)
```

## Duomenų formatai

### DataFrame struktūra

Istoriniai ir prognozės duomenys grąžinami kaip pandas DataFrame su:

- **Indeksas**: DatetimeIndex su Lietuvos laiko zona
- **Stulpeliai**: Lietuviški pavadinimai oro parametrams

### Laiko zonos

Visi datos/laiko duomenys konvertuojami į Lietuvos laiko zoną (`Europe/Vilnius`).

## Performance rekomendacijos

### Duomenų kiekio valdymas
- Istoriniams duomenis: rekomenduojama ne daugiau 90 dienų vienu metu
- Interpoliacija: gali suvartoti daug atminties didiems duomenų kiekiams

### API užklausos
- API turi rate limiting - naudokite su įmontuota retry logika
- Išsaugokite duomenis lokaliai kartotiniam naudojimui

### Vizualizacija
- Dideli grafikai (300+ DPI) gali užtrukti
- Naudokite `plots_dir` parametrą grafikų organizavimui

## Integravimo pavyzdžiai

### Pilnas darbo ciklas

```python
from src.weather_api import WeatherAPI
from src.data_analysis import WeatherAnalyzer
from src.visualization import WeatherVisualizer
from src.interpolation import TemperatureInterpolator
from datetime import datetime, timedelta

# 1. Gauti duomenis
api = WeatherAPI('vilnius')
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

historical = api.get_historical_data(
    start_date.strftime('%Y-%m-%d'),
    end_date.strftime('%Y-%m-%d')
)
forecast = api.get_forecast_data(7)

# 2. Analizuoti duomenis
analyzer = WeatherAnalyzer(historical, forecast)
report = analyzer.generate_summary_report()

# 3. Vizualizuoti
visualizer = WeatherVisualizer(historical, forecast)
dashboard = visualizer.create_weather_dashboard()
temp_plot = visualizer.plot_temperature_trend()

# 4. Interpoliuoti temperatūrą
if 'temperatura' in historical.columns:
    interpolator = TemperatureInterpolator(historical['temperatura'])
    interpolated = interpolator.interpolate_to_5min('linear')
    
    # Išsaugoti interpoliuotus duomenis
    interpolator.export_interpolated_data('interpolated_temps.csv')

print("Analizė užbaigta!")
```

### Keliems miestams

```python
cities = ['vilnius', 'kaunas', 'klaipeda']
city_data = {}

for city in cities:
    api = WeatherAPI(city)
    data = api.get_historical_data('2024-01-01', '2024-01-31')
    if data is not None:
        city_data[city] = data

# Palyginti miestus
visualizer = WeatherVisualizer()
comparison_plot = visualizer.plot_city_comparison(city_data)
```

## API limitas ir etika

- meteo.lt API yra nemokama viešoji tarnyba
- Naudokite protingai - nevykdykite per daug užklausų per trumpą laiką
- Sistema turi integruotą retry logiką ir timeout valdymą
- Rekomenduojama: maksimum 60 užklausų per minutę

## Versijų suderinamumas

Ši sistema sukurta su:
- Python 3.8+
- pandas 1.5.0+
- numpy 1.24.0+
- matplotlib 3.6.0+

Senesnės versijos gali neveikti tinkamai.
