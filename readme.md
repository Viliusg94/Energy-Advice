# Energy Advice - Lietuvos oro duomenų analizės sistema

**Programavimo kalba:** Python 3.12+  
**Duomenų šaltinis:** api.meteo.lt (Lietuvos hidrometeorologijos tarnyba)  


##  Projekto apžvalga

 Lietuvos oro duomenų analizės sistema, kuri naudoja tikrus duomenis iš Lietuvos hidrometeorologijos tarnybos API. Sistema skirta duomenų analizės mokymui ir tyrimams.

###  Pagrindinės funkcijos
-  Realūs oro duomenys iš meteo.lt API (83 įrašai)
-  4  vizualizacijų grafikai 
-  Statistinė duomenų analizė
-  Temperatūros duomenų interpoliacija
-  69 automatiniai unit testai (100% veikia)
-  Interaktyvus Jupyter notebook
-  Modulinė ir plėtojama architektūra

##  Projekto struktūra

```
Energy Advice/
├── src/                                # Pagrindinis kodas (1,531 eilutė)
│   ├── weather_api.py                  # API ryšio modulis (231 eilutė)
│   ├── data_analysis.py                # Duomenų analizės modulis (357 eilutės)  
│   ├── visualization.py                # Grafikų kūrimo modulis (512 eilučių)
│   ├── interpolation.py                # Interpoliacijos modulis (421 eilutė)
│   └── __init__.py
├── data/                               # Duomenų failai
│   ├── forecast_data.csv               # 83 oro prognozės įrašai
│   ├── analysis_results.json           # Analizės rezultatai
│   ├── analysis_summary_notebook.json  # Notebook suvestinė
│   ├── historical_data.csv             # Istoriniai duomenys
│   └── interpolated_temperature.csv    # Interpoliuoti duomenys
├── plots/                              # Sukurti grafikai (1.4MB)
│   ├── weather_dashboard.png           # Pagrindinė suvestinė (505KB)
│   ├── correlation_heatmap.png         # Koreliacijos matrica (324KB)
│   ├── temperature_trend.png           # Temperatūros tendencijos (323KB)
│   └── temperature_humidity_scatter.png # Sklaidos grafikas (266KB)
├── tests/                              # Testų sistema (69 testai)
│   ├── test_weather_api.py             # API testai (16 testų)
│   ├── test_data_analysis.py           # Analizės testai (23 testai)
│   ├── test_interpolation.py           # Interpoliacijos testai (30 testų)
│   └── __init__.py
├── notebooks/                          # Jupyter failai
│   └── weather_analysis.ipynb          # Interaktyvus notebook (25 celės)
├── docs/                               # Dokumentacija
│   ├── usage_guide.md                  # Naudojimo vadovas (833 eilutės)
│   ├── installation_guide.md           # Instaliavimo vadovas (351 eilutė)
│   └── api_documentation.md            # API dokumentacija (280 eilučių)
├── requirements.txt                    # Priklausomybės (10 bibliotekų)
├── main.py                             # Pagrindinė programa
├── readme.md                           # Šis failas
└── report.md                           # Išsamus projekto ataskaita
```

##  Paleidimas

### 1. Reikalavimų įdiegimas
```bash
pip install -r requirements.txt
```

### 2. Pagrindinės programos paleidimas
```bash
python main.py
```

### 3. Jupyter notebook paleidimas
```bash
jupyter notebook notebooks/weather_analysis.ipynb
```

### 4. Testų paleidimas
```bash
python -m pytest tests/ -v
```

##  Sistemos reikalavimai

### Python bibliotekos:
```
pandas>=1.5.0       # Duomenų apdorojimui
numpy>=1.24.0       # Matematinėms operacijoms
requests>=2.28.0    # API užklausoms  
matplotlib>=3.6.0   # Grafikų kūrimui
seaborn>=0.12.0     # Statistinių grafikų kūrimui
pytz>=2023.3        # Laiko zonų tvarkymui
jupyter>=1.0.0      # Interaktyviems notebook'ams
pytest>=7.0.0       # Testavimui
scipy>=1.9.0        # Mokslinėms funkcijoms
requests-mock>=1.9.0 # Testų mock objektams
```

### Python versija:
-  Python 3.12+ 


##  Pagrindinės funkcijos

### WeatherAPI klasė (weather_api.py)
```python
from src.weather_api import WeatherAPI

# Sukuriame API objektą
api = WeatherAPI('vilnius')

# Gaunami prognozės duomenys
forecast_data = api.get_forecast_data()

# Gaunami dabartiniai oro duomenys  
current_weather = api.get_current_weather()
```

### Duomenų analizė (data_analysis.py)
```python
from src.data_analysis import WeatherAnalyzer

# Sukuriame analizės objektą
analyzer = WeatherAnalyzer(forecast_data)

# Skaičiuojami metiniai vidurkiai
yearly_avg = analyzer.calculate_yearly_averages()

# Analizuojami dienos/nakties temperatūros skirtumai
day_night = analyzer.analyze_day_night_temperature()
```

### Vizualizacijos (visualization.py)
```python
from src.visualization import WeatherVisualizer

# Sukuriame vizualizacijos objektą
visualizer = WeatherVisualizer(forecast_data)

# Kuriame pagrindinį dashboard
visualizer.create_weather_dashboard()

# Kuriame temperatūros tendencijų grafiką
visualizer.plot_temperature_trend()
```

### Interpoliacija (interpolation.py)
```python
from src.interpolation import TemperatureInterpolator

# Sukuriame interpoliacijos objektą
interpolator = TemperatureInterpolator(temperature_data)

# Interpoliuojami duomenys iki 5 min dažnio
interpolated = interpolator.interpolate_to_5min('linear')
```

##  Realūs rezultatai

### Duomenų kiekis:
- **83 oro prognozės įrašai** už 7 dienų periodą
- **4 grafikai** (bendras dydis: 1.4MB)
- **Duomenų laikotarpis:** 2025-08-07 iki 2025-08-14
- **Geografinis plotas:** Vilnius

### Svarbiausias atradimas:
**-89.6% koreliacija** tarp temperatūros ir drėgmės - kuo aukštesnė temperatūra, tuo mažesnė drėgmė.

### Testavimo aprėptis:
- **69 unit testai** (100% veikia)
- **Modulių testavimas:** API (16), Analizė (23), Interpoliacija (30)
- **Funkcinis testavimas** su realiais duomenimis

## 🚀 Palaikomų miestų sąrašas

| Miestas    | Kodas     | API būklė |
|------------|-----------|-----------|
| Vilnius    | vilnius   |  Veikia   |
| Kaunas     | kaunas    |  Veikia   |
| Klaipėda   | klaipeda  |  Veikia   |
| Šiauliai   | siauliai  |  Ribotas  |
| Panevėžys  | panevezys |  Ribotas  |

**Pastaba:** Pilnai veikia tik Vilnius. Kiti miestai dėl API apribojimų gali grąžinti tuščius duomenis.

##  Dokumentacija

- **[usage_guide.md](docs/usage_guide.md)** - Išsamus naudojimo vadovas
- **[installation_guide.md](docs/installation_guide.md)** - Žingsnis po žingsnio instaliavimo instrukcijos
- **[api_documentation.md](docs/api_documentation.md)** - API metodų dokumentacija
- **[report.md](report.md)** - Išsamus projekto analizės ataskaita

##  Testų paleidimas

### Visų testų paleidimas:
```bash
python -m pytest tests/ -v
```

### Konkretaus modulio testavimas:
```bash
python -m pytest tests/test_weather_api.py -v        # API testai
python -m pytest tests/test_data_analysis.py -v     # Analizės testai  
python -m pytest tests/test_interpolation.py -v     # Interpoliacijos testai
```

### Testavimo aprėptis:
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

##  Plėtros galimybės

### Artimiausi pagerinai (1-2 mėn.):
1. **Kelių miestų palaikymas** - pilnai veikianti multi-city analizė
2. **Istorinių duomenų integravimas** - alternatyvūs API šaltiniai
3. **Performance optimizavimas** - async API calls ir caching
4. **Grafikai** - Plotly integravimas

### Vidutinio periodo plėtra (3-6 mėn.):
1. **Web aplikacijos kūrimas** - Flask dashboard
2. **Duomenų bazės integravimas** - PostgreSQL
3. **Machine Learning modeliai** - oro prognozavimas
4. **Real-time monitoring** - automatinis duomenų atnaujinimas

### Ilgalaikės perspektyvos (6+ mėn.):
1. **Production deployment** - Docker konteineriai
2. **REST API endpoints** - komercinis API
3. **Mobili aplikacija** - cross-platform app
4. **AI-powered insights** - pažangūs algoritmai

##  Žinomi apribojimai

1. **API priklausomybė** - sistema priklauso nuo meteo.lt API prieinamumo
2. **Duomenų kiekis** - ribotas istorinių duomenų kiekis
3. **Miestų palaikymas** - tik Vilnius veikia stabiliai
4. **Rate limiting** - API užklausų dažnio apribojimai


**Paskutinis atnaujinimas:** 2025-08-08  
**Testavimo būklė:** 69/69 testai veikia (100% success rate)
