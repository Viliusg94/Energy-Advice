# Lietuvos oro duomenÅ³ analizÄ—s sistema

[![Python 3.8+](https://img.shields.io/badge/Python3.8+blue.svg)](https://www.python.org/downloads/)
[![API](https://img.shields.io/badge/APImeteo.ltgreen.svg)](https://api.meteo.lt/)
[![License](https://img.shields.io/badge/LicenseMITyellow.svg)](LICENSE)

## Projekto tikslas

Sukurti iÅsamiÄ… Python programÄ…, kuri naudodama Lietuvos hidrometeorologijos tarnybos REST API (https://api.meteo.lt/) atliks oro duomenÅ³ nuskaitymÄ…, analizÄ™ ir vizualizacijÄ….

## PagrindinÄ—s funkcijos

 **IstoriniÅ³ oro duomenÅ³ nuskaitymas**  temperatÅ«ra, drÄ—gmÄ—, vÄ—jo greitis, slÄ—gis
 **Oro prognoziÅ³ gavimas**  ateities oro sÄ…lygÅ³ duomenys
 **IÅsami statistinÄ— analizÄ—**  vidurkiai, ekstremumÅ³ paieÅka, tendencijos
 **DuomenÅ³ vizualizacija**  grafikai, dashboard'ai, koreliacijos matricos
 **TemperatÅ«ros interpoliacija**  duomenÅ³ tankumo didinimas
 **KeliÅ³ miestÅ³ palaikymas**  Vilnius, Kaunas, KlaipÄ—da, Å iauliai, PanevÄ—Å¾ys
 **Jupyter Notebook**  interaktyvus duomenÅ³ tyrinÄ—jimas
 **IÅsamÅ«s testai**  unit testai visiems komponentams

## Greitas startas

### 1. Instaliavimas

```bash
# Klonuokite repozitorijÄ…
git clone https://github.com/yourusername/weatheranalysis.git
cd weatheranalysis

# Sukurkite virtual environment
python m venv weather_env
source weather_env/bin/activate  # Linux/macOS
# arba
weather_env\Scripts\activate     # Windows

# Ä®diekite priklausomybes
pip install r requirements.txt
```

### 2. Paleidimas

```bash
# PagrindinÄ— programa
python main.py

# Arba Jupyter Notebook
jupyter notebook notebooks/weather_analysis.ipynb
```

### 3. TestÅ³ paleidimas

```bash
python m pytest tests/ v
```

## Projekto struktÅ«ra

```
weatheranalysis/
ā”ā”€ā”€ src/                     # Pagrindiniai moduliai
ā”‚   ā”ā”€ā”€ weather_api.py       # API integracija
ā”‚   ā”ā”€ā”€ data_analysis.py     # DuomenÅ³ analizÄ—
ā”‚   ā”ā”€ā”€ visualization.py     # Grafikai
ā”‚   ā””ā”€ā”€ interpolation.py     # Interpoliacija
ā”ā”€ā”€ notebooks/               # Jupyter notebook'ai
ā”‚   ā””ā”€ā”€ weather_analysis.ipynb
ā”ā”€ā”€ tests/                   # Unit testai
ā”‚   ā”ā”€ā”€ test_weather_api.py
ā”‚   ā”ā”€ā”€ test_data_analysis.py
ā”‚   ā””ā”€ā”€ test_interpolation.py
ā”ā”€ā”€ docs/                    # Dokumentacija
ā”‚   ā”ā”€ā”€ š“– api_documentation.md
ā”‚   ā”ā”€ā”€ š”§ installation_guide.md
ā”‚   ā””ā”€ā”€ š“ usage_guide.md
ā”ā”€ā”€ š“‚ data/                    # DuomenÅ³ katalogs
ā”ā”€ā”€ š“‚ plots/                   # Generuoti grafikai
ā”ā”€ā”€ š¨ main.py                  # PagrindinÄ— programa
ā”ā”€ā”€ š“‹ requirements.txt         # Python priklausomybÄ—s
ā””ā”€ā”€ š“– README.md               # Å is failas
```
## š“– Dokumentacija

### PradÅ¾iamokslis
 š“ [Instaliavimo instrukcijos](docs/installation_guide.md)
 š“ [Naudojimo vadovas](docs/usage_guide.md)
 š”§ [API dokumentacija](docs/api_documentation.md)

### PavyzdÅ¾iai

#### Paprastas naudojimas

```python
from src.weather_api import WeatherAPI
from src.data_analysis import WeatherAnalyzer

# Inicializuojame API
api = WeatherAPI("vilnius")

# Nuskaitome duomenis
data = api.get_historical_data("20240101", "20240131")

# Analizuojame
analyzer = WeatherAnalyzer(data)
averages = analyzer.calculate_annual_averages()

print(f"VidutinÄ— temperatÅ«ra: {averages['average_temperature']:.1f}Ā°C")
```

#### Grafiko kÅ«rimas

```python
from src.visualization import WeatherVisualizer

visualizer = WeatherVisualizer("my_plots")
visualizer.plot_temperature_trend(data, title="Vilniaus temperatÅ«ra")
```

#### TemperatÅ«ros interpoliacija

```python
from src.interpolation import TemperatureInterpolator

interpolator = TemperatureInterpolator()
interpolated = interpolator.interpolate_temperature(
    temp_series, 
    target_frequency='5T',  # 5 minutÄ—s
    method='linear'
)
```

## š› ļø¸ Reikalavimai

### Sistemos reikalavimai
 Python 3.8 ar naujesnÄ— versija
 2GB laisvos disko vietos
 Internetinis ryÅys (API uÅ¾klausoms)

### Python bibliotekos
```
pandas>=1.5.0
numpy>=1.24.0
requests>=2.28.0
matplotlib>=3.6.0
seaborn>=0.12.0
pytz>=2023.3
jupyter>=1.0.0
pytest>=7.0.0
```

## š”§ KonfigÅ«racija

### MiestÅ³ kodai
 `vilnius`  Vilnius
 `kaunas`  Kaunas
 `klaipeda`  KlaipÄ—da
 `siauliai`  Å iauliai
 `panevezys`  PanevÄ—Å¾ys

### API nustatymai
 **Base URL**: https://api.meteo.lt/
 **Rate limit**: 12 sekundÄ—s tarp uÅ¾klausÅ³
 **Timeout**: 30 sekundÅ¾iÅ³

## š“ AnalizÄ—s galimybÄ—s

### StatistinÄ— analizÄ—
 ā… Metiniai/mÄ—nesiniai vidurkiai
 ā… Dienos/nakties temperatÅ«ros skirtumai
 ā… EkstremumÅ³ paieÅka
 ā… SavaitgaliÅ³ lietaus prognozÄ—s
 ā… Oro parametrÅ³ koreliacijos

### Vizualizacija
 ā… TemperatÅ«ros tendencijos grafikai
 ā… Oro sÄ…lygÅ³ dashboard'ai (4in1)
 ā… Koreliacijos matricos heatmap
 ā… KrituliÅ³ analizÄ—s grafikai
 ā… MiestÅ³ palyginimo grafikai

### Interpoliacija
 ā… TiesinÄ— interpoliacija
 ā… Laiko pagrÄÆsta interpoliacija
 ā… PolinominÄ— interpoliacija
 ā… Spline interpoliacija
 ā… MetodÅ³ palyginimas ir validacija

## š§Ŗ Testai

```bash
# Paleisti visus testus
pytest tests/ v

# Su coverage report
pytest tests/ cov=src covreport=html

# Konkretus modulis
pytest tests/test_weather_api.py v
```

### TestÅ³ aprÄ—ptis
 ā… API integracija (mock testai)
 ā… DuomenÅ³ analizÄ—s algoritmai
 ā… Interpoliacijos metodai
 ā… KlaidÅ³ apdorojimas
 ā… Edge case scenarijai

## š“ Performance

### Optimizacijos
 š”„ API uÅ¾klausÅ³ cache'inimas
 š—ļø¸ DuomenÅ³ tipo optimizacija (float32)
 š“¦ Chunk processing dideliems duomenims
 ā Vectorized operacijos su NumPy/Pandas

### Atminties naudojimas
 Tipinis duomenÅ³ rinkinys (30 dienÅ³): ~10MB
 Interpoliuoti duomenys (5min daÅ¾nis): ~50MB
 Grafikai (PNG): ~13MB kiekvienas

## š› Troubleshooting

### DaÅ¾nos problemos

#### API klaidos
```bash
# Patikrinti API prieinamumÄ…
curl I https://api.meteo.lt/

# 429 Too Many Requests  palaukti tarp uÅ¾klausÅ³
```

#### Import klaidos
```python
import sys
sys.path.append('./src')  # PridÄ—ti src ÄÆ Python path
```

#### SSL klaidos
```bash
pip install trustedhost pypi.org requests
```

### Diagnostic script
```bash
python diagnostic.py  # Patikrina sistemos bÅ«senÄ…
```

## š¤¯ PrisidÄ—jimas

### Development setup
```bash
# Fork repozitorijos
git clone https://github.com/yourfork/weatheranalysis.git

# Sukurti feature branch
git checkout b feature/newanalysis

# Commit ir push
git commit m "Add new analysis feature"
git push origin feature/newanalysis
```

### Code style
 PEP 8 standartai
 Type hints
 Docstrings visoms funkcijoms
 Unit testai naujoms funkcijoms

## š“ Licencija

Å is projektas yra licencijuotas pagal MIT licencijÄ…  Å¾r. [LICENSE](LICENSE) failÄ….

## š™¸ PadÄ—kos

 [Lietuvos hidrometeorologijos tarnyba](https://www.meteo.lt/) uÅ¾ vieÅÄ… API
 [Pandas](https://pandas.pydata.org/) ir [Matplotlib](https://matplotlib.org/) komandos
 Open source bendruomenÄ—

## š“˛ Kontaktai

 š› **Bug reports**: [GitHub Issues](https://github.com/yourusername/weatheranalysis/issues)
 š’ **Feature requests**: [GitHub Discussions](https://github.com/yourusername/weatheranalysis/discussions)
 š“§ **Email**: youremail@example.com



## ā… Projekto ÄÆgyvendinimo statusas

### Pagrindas ā…
 [x] 1.1. Sukurti GitHub repozitorijÄ…
 [x] 1.2. Sukurti projektÅ³ katalogÅ³ struktÅ«rÄ…
 [x] 1.3. Parengti requirements.txt failÄ…
 [x] 1.4. Sukurti README.md failÄ…

### API modulis ā…
 [x] 2.1. IÅanalizuoti API dokumentacijÄ…
 [x] 2.2. Sukurti WeatherAPI klasÄ™
 [x] 2.3. Implementuoti konstruktoriÅ³
 [x] 2.4. PridÄ—ti error handling

### DuomenÅ³ gavimas ā…
 [x] 3.1. get_historical_data() metodas
 [x] 3.2. API uÅ¾klausÅ³ implementacija
 [x] 3.3. Pandas DataFrame konvertavimas
 [x] 3.4. Datetime indeksas su laiko zona
 [x] 3.5. DuomenÅ³ validavimas

### PrognozÄ—s ā…
 [x] 4.1. get_forecast_data() metodas
 [x] 4.2. PrognozÄ—s API implementacija
 [x] 4.3. DataFrame konvertavimas
 [x] 4.4. Laiko zonos nustatymas
 [x] 4.5. DuomenÅ³ validavimas

### MiestÅ³ palaikymas ā…
 [x] 5.1. MiestÅ³ kodÅ³ sÄ…raÅas
 [x] 5.2. Vilnius kaip default
 [x] 5.3. Konstantos miestÅ³ kodams

### AnalizÄ—s modulis ā…
 [x] 6.1. MetiniÅ³ duomenÅ³ nuskaitymas
 [x] 6.2. VidutinÄ—s temperatÅ«ros skaiÄ¨iavimas
 [x] 6.3. VidutinÄ—s drÄ—gmÄ—s skaiÄ¨iavimas
 [x] 6.4. RezultatÅ³ spausdinimas

### Dienos/nakties analizÄ— ā…
 [x] 7.1. Laiko intervalÅ³ filtravimas
 [x] 7.2. Dienos temperatÅ«ros skaiÄ¨iavimas
 [x] 7.3. Nakties temperatÅ«ros skaiÄ¨iavimas
 [x] 7.4. Laiko zonos atsiÅ¾velgimas

### SavaitgaliÅ³ analizÄ— ā…
 [x] 8.1. SavaitgaliÅ³ identifikavimas
 [x] 8.2. Lietaus nustatymo logika
 [x] 8.3. SavaitgaliÅ³ su lietumi skaiÄ¨iavimas
 [x] 8.4. RezultatÅ³ pateikimas

### DuomenÅ³ sujungimas ā…
 [x] 9.1. PrognozÄ—s duomenÅ³ nuskaitymas
 [x] 9.2. IstoriniÅ³ ir prognozÄ—s duomenÅ³ apjungimas
 [x] 9.3. DuomenÅ³ suderinamumo uÅ¾tikrinimas

### Vizualizacija ā…
 [x] 10.1. PaskutinÄ—s savaitÄ—s duomenÅ³ filtravimas
 [x] 10.2. PrognozÄ—s duomenÅ³ filtravimas
 [x] 10.3. Matplotlib/seaborn grafiko kÅ«rimas
 [x] 10.4. Grafiko apraÅymas ir legenda
 [x] 10.5. Grafiko iÅsaugojimas

### Interpoliacija ā…
 [x] 11.1. interpolate_temperature() funkcija
 [x] 11.2. 5 minuÄ¨iÅ³ daÅ¾nio implementacija
 [x] 11.3. Pandas interpolate() metodas
 [x] 11.4. Pandas Series grÄ…Å¾inimas
 [x] 11.5. Funkcijos testai

### Kodo kokybÄ— ā…
 [x] 12.1. PEP 8 standartÅ³ taikymas
 [x] 12.2. Docstrings klasÄ—ms ir metodams
 [x] 12.3. Type hints pridÄ—jimas
 [x] 12.4. Unit testÅ³ sukÅ«rimas
 [x] 12.5. Logging sistemos naudojimas

### Dokumentacija ā…
 [x] 13.1. IÅsamus README.md
 [x] 13.2. Naudojimo pavyzdÅ¾iai
 [x] 13.3. API metodÅ³ dokumentavimas
 [x] 13.4. Instaliavimo instrukcijos

### FailÅ³ formatai ā…
 [x] 14.1. .py failas su visomis funkcijomis
 [x] 14.2. .ipynb Jupyter notebook failas
 [x] 14.3. AbiejÅ³ formatÅ³ nepriklausomumas

### Projekto uÅ¾baigimas ā…
 [x] 15.1. VisÅ³ funkcijÅ³ veikimo patikrinimas
 [x] 15.2. Projekto struktÅ«ros uÅ¾baigimas
 [x] 15.3. Dokumentacijos uÅ¾baigimas
 [x] 15.4. README su instrukcijomis

**šˇ‰ PROJEKTAS 100% Ä®GYVENDINTAS!**



*Sukurta su ā¯¤ļø¸ naudojant Python ir open source bibliotekas* 
