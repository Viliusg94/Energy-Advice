# API Dokumentacija - Lietuvos oro duomenų analizės sistema

## Apžvalga

Ši dokumentacija aprašo Lietuvos oro duomenų analizės sistemos API funkcionalumą ir naudojimą. Sistema naudoja Lietuvos hidrometeorologijos tarnybos REST API (https://api.meteo.lt/) duomenų nuskaitymui ir analizei.

## Modulių struktūra

### 1. WeatherAPI klasė (`src/weather_api.py`)

Pagrindinė klasė darbui su meteo.lt API.

#### Konstruktorius
```python
WeatherAPI(location_code: str = "vilnius")
```

**Parametrai:**
- `location_code` (str): Vietovės kodas (default: "vilnius")

**Galimi miestų kodai:**
- `vilnius` - Vilnius
- `kaunas` - Kaunas  
- `klaipeda` - Klaipėda
- `siauliai` - Šiauliai
- `panevezys` - Panevėžys

#### Metodai

##### `get_historical_data(start_date: str, end_date: str) -> Optional[pd.DataFrame]`

Nuskaito istorinius oro duomenis nurodytam laikotarpiui.

**Parametrai:**
- `start_date` (str): Pradžios data formatu YYYY-MM-DD
- `end_date` (str): Pabaigos data formatu YYYY-MM-DD

**Grąžina:**
- `pd.DataFrame`: Istoriniai duomenys su datetime indeksu
- `None`: Jei klaida arba nėra duomenų

**Pavyzdys:**
```python
api = WeatherAPI("vilnius")
data = api.get_historical_data("2024-01-01", "2024-01-31")
```

##### `get_forecast_data() -> Optional[pd.DataFrame]`

Nuskaito oro prognozės duomenis.

**Grąžina:**
- `pd.DataFrame`: Prognozės duomenys su datetime indeksu
- `None`: Jei klaida arba nėra duomenų

**Pavyzdys:**
```python
forecast = api.get_forecast_data()
```

##### `get_current_conditions() -> Optional[Dict]`

Nuskaito dabartinius oro sąlygas.

**Grąžina:**
- `Dict`: Dabartiniai oro duomenys
- `None`: Jei klaida

**Pavyzdys:**
```python
current = api.get_current_conditions()
```

### 2. WeatherAnalyzer klasė (`src/data_analysis.py`)

Klasė oro duomenų analizei ir statistikos skaičiavimui.

#### Konstruktorius
```python
WeatherAnalyzer(historical_data: Optional[pd.DataFrame] = None, 
                forecast_data: Optional[pd.DataFrame] = None)
```

#### Metodai

##### `calculate_annual_averages(data: Optional[pd.DataFrame] = None) -> Dict[str, float]`

Apskaičiuoja metinius oro parametrų vidurkius.

**Grąžina:**
- `average_temperature`: Vidutinė temperatūra (°C)
- `average_humidity`: Vidutinė drėgmė (%)
- `average_wind_speed`: Vidutinis vėjo greitis (m/s)
- `average_pressure`: Vidutinis slėgis (hPa)

**Pavyzdys:**
```python
analyzer = WeatherAnalyzer(historical_data)
averages = analyzer.calculate_annual_averages()
print(f"Vidutinė temperatūra: {averages['average_temperature']:.1f}°C")
```

##### `analyze_day_night_temperature(data: Optional[pd.DataFrame] = None) -> Dict[str, float]`

Analizuoja dienos ir nakties temperatūros skirtumus.

**Laiko intervalai:**
- Diena: 08:00-20:00
- Naktis: 20:00-08:00

**Grąžina:**
- `average_day_temperature`: Vidutinė dienos temperatūra (°C)
- `average_night_temperature`: Vidutinė nakties temperatūra (°C)
- `day_night_difference`: Temperatūros skirtumas (°C)

**Pavyzdys:**
```python
day_night = analyzer.analyze_day_night_temperature()
print(f"Dienos/nakties skirtumas: {day_night['day_night_difference']:.1f}°C")
```

##### `analyze_weekend_rain_forecast(data: Optional[pd.DataFrame] = None) -> Dict[str, Any]`

Analizuoja savaitgalių lietaus prognozes.

**Grąžina:**
- `weekend_rain_days`: Lietingų savaitgalių dienų skaičius
- `total_weekend_days`: Bendras savaitgalių dienų skaičius
- `rain_probability`: Lietaus tikimybė savaitgaliais (%)

**Pavyzdys:**
```python
weekend_rain = analyzer.analyze_weekend_rain_forecast()
print(f"Lietaus tikimybė savaitgaliais: {weekend_rain['rain_probability']:.1f}%")
```

##### `combine_data() -> pd.DataFrame`

Sujungia istorinius ir prognozės duomenis.

**Grąžina:**
- `pd.DataFrame`: Sujungti duomenys chronologine tvarka

### 3. WeatherVisualizer klasė (`src/visualization.py`)

Klasė oro duomenų vizualizacijai.

#### Konstruktorius
```python
WeatherVisualizer(output_dir: str = "plots")
```

#### Metodai

##### `plot_temperature_trend(historical_data: Optional[pd.DataFrame] = None, forecast_data: Optional[pd.DataFrame] = None, title: str = "Temperatūros kaita", save_file: str = "temperature_trend.png") -> str`

Sukuria temperatūros kaitos grafiką.

**Parametrai:**
- `historical_data`: Istoriniai duomenys
- `forecast_data`: Prognozės duomenys
- `title`: Grafiko pavadinimas
- `save_file`: Failo pavadinimas išsaugojimui

**Grąžina:**
- `str`: Išsaugoto failo kelias

**Pavyzdys:**
```python
visualizer = WeatherVisualizer("plots")
path = visualizer.plot_temperature_trend(historical_data, forecast_data)
```

##### `plot_weather_dashboard(data: pd.DataFrame, title: str = "Oro sąlygų suvestinė", save_file: str = "weather_dashboard.png") -> str`

Sukuria visapusišką oro sąlygų grafiką (2x2 subplot'ai).

**Grafikų tipai:**
- Temperatūros kaita
- Drėgmės kaita
- Vėjo greičio kaita
- Slėgio kaita

##### `plot_correlation_matrix(data: pd.DataFrame, title: str = "Oro parametrų koreliacijos matrica", save_file: str = "correlation_matrix.png") -> str`

Sukuria oro parametrų koreliacijos matricos heatmap.

### 4. TemperatureInterpolator klasė (`src/interpolation.py`)

Klasė temperatūros duomenų interpoliacijai.

#### Konstruktorius
```python
TemperatureInterpolator()
```

**Palaikomi metodai:**
- `linear` - Tiesinė interpoliacija
- `time` - Laiko pagrįsta interpoliacija
- `polynomial` - Polinominė interpoliacija
- `spline` - Spline interpoliacija

#### Metodai

##### `interpolate_temperature(temperature_series: pd.Series, target_frequency: str = '5T', method: str = 'linear') -> Optional[pd.Series]`

Interpoliuoja temperatūros duomenis iki nurodyto dažnio.

**Parametrai:**
- `temperature_series`: Temperatūros duomenų serija su datetime indeksu
- `target_frequency`: Tikslo dažnis (pvz., '5T' = 5 minutės)
- `method`: Interpoliacijos metodas

**Grąžina:**
- `pd.Series`: Interpoliuoti duomenys
- `None`: Jei klaida

**Pavyzdys:**
```python
interpolator = TemperatureInterpolator()
interpolated = interpolator.interpolate_temperature(
    temp_series, 
    target_frequency='5T', 
    method='linear'
)
```

##### `interpolate_with_statistics(temperature_series: pd.Series, target_frequency: str = '5T', method: str = 'linear') -> dict`

Interpoliuoja duomenis ir grąžina detalią statistiką.

**Grąžina:**
```python
{
    'interpolated_data': pd.Series,
    'original_points': int,
    'interpolated_points': int,
    'improvement_ratio': float,
    'method': str,
    'frequency': str,
    'original_min': float,
    'original_max': float,
    'original_mean': float,
    'interpolated_min': float,
    'interpolated_max': float,
    'interpolated_mean': float
}
```

##### `compare_interpolation_methods(temperature_series: pd.Series, target_frequency: str = '5T') -> dict`

Palygina visus interpoliacijos metodus ir rekomenduoja geriausią.

##### `validate_interpolation(original: pd.Series, interpolated: pd.Series) -> dict`

Validuoja interpoliacijos kokybę.

**Grąžina:**
```python
{
    'valid': bool,
    'valid_range': bool,
    'valid_mean': bool,
    'original_range': tuple,
    'interpolated_range': tuple,
    'mean_difference': float,
    'tolerance': float
}
```

## Dažnio formatai

Pandas dažnio koodai interpoliacijai:

| Kodas | Aprašymas |
|-------|-----------|
| `T` arba `min` | Minutė |
| `5T` | 5 minutės |
| `10T` | 10 minučių |
| `15T` | 15 minučių |
| `30T` | 30 minučių |
| `H` | Valanda |
| `D` | Diena |

## Klaidos ir išimtys

Visos klasės naudoja Python logging sistemą klaidų registravimui:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

**Pagrindinės išimtys:**
- `requests.exceptions.RequestException` - API užklausų klaidos
- `ValueError` - Neteisingi parametrai (datos, formatai)
- `KeyError` - Trūkstami duomenų stulpeliai
- `pandas.errors.EmptyDataError` - Tušti duomenys

## Pavyzdžiai

### Pilnas darbo ciklas

```python
from src.weather_api import WeatherAPI
from src.data_analysis import WeatherAnalyzer
from src.visualization import WeatherVisualizer
from src.interpolation import TemperatureInterpolator

# 1. Duomenų nuskaitymas
api = WeatherAPI("vilnius")
historical = api.get_historical_data("2024-01-01", "2024-01-31")
forecast = api.get_forecast_data()

# 2. Analizė
analyzer = WeatherAnalyzer(historical, forecast)
annual_avg = analyzer.calculate_annual_averages()
day_night = analyzer.analyze_day_night_temperature()

# 3. Vizualizacija
visualizer = WeatherVisualizer("plots")
visualizer.plot_temperature_trend(historical, forecast)
visualizer.plot_weather_dashboard(historical)

# 4. Interpoliacija
interpolator = TemperatureInterpolator()
temp_series = historical['airTemperature']
interpolated = interpolator.interpolate_temperature(temp_series, '5T')

# 5. Rezultatų spausdinimas
analyzer.print_analysis_results(annual_avg, day_night, {})
```

### Klaidų apdorojimas

```python
try:
    data = api.get_historical_data("2024-01-01", "2024-01-31")
    if data is None or data.empty:
        print("Nėra duomenų")
        return
    
    # Tęsti su analize...
    
except Exception as e:
    print(f"Klaida: {e}")
    # Logging
    import logging
    logging.error(f"API klaida: {e}")
```

## Performance ir limitai

### API limitai
- meteo.lt API neturi oficialių rate limit'ų, bet rekomenduojama nesiųsti per dažnai užklausų
- Istoriniai duomenys prieinami ribotas laikotarpis
- Prognozės paprastai iki 7-10 dienų

### Atminties naudojimas
- Didelių duomenų rinkinių interpoliacija gali sunaudoti daug atminties
- Rekomenduojama dalinti didelius duomenis į mažesnius blokus

### Optimizacijos patarimai
```python
# Naudoti chunk'us dideliems duomenims
chunk_size = 1000
for chunk in pd.read_csv('large_data.csv', chunksize=chunk_size):
    # Apdoroti po dalis
    pass

# Cache API užklausas
from functools import lru_cache

@lru_cache(maxsize=32)
def cached_api_call(start_date, end_date):
    return api.get_historical_data(start_date, end_date)
```
