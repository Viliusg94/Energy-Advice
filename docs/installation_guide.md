# Instaliavimo vadovas - Lietuvos oro duomenų analizės sistema

## Sistemos reikalavimai

### Minimalūs reikalavimai
- **Python**: 3.8 ar naujesnė versija
- **Operacinė sistema**: Windows 10/11, macOS 10.14+, arba Linux (Ubuntu 18.04+)
- **Atmintis**: 4GB RAM (rekomenduojama 8GB)
- **Disko vieta**: 1GB laisvos vietos
- **Internetinis ryšys**: Reikalingas API užklausoms

### Rekomenduojami reikalavimai
- **Python**: 3.9 ar 3.10
- **Atmintis**: 8GB RAM ar daugiau
- **Disko vieta**: 2GB laisvos vietos
- **Internetinis ryšys**: Stabilus plačiajuostis ryšys

## Instaliavimo žingsniai

### 1. Python instaliavimas

#### Windows
1. Atsisiųskite Python iš [python.org](https://www.python.org/downloads/)
2. Paleiskite installer'į
3. **SVARBU**: Pažymėkite "Add Python to PATH"
4. Pasirinkite "Install Now"

#### macOS
```bash
# Naudojant Homebrew (rekomenduojama)
brew install python

# Arba atsisiųskite iš python.org
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 2. Projekto parsisiunčiamas

#### Git klonuojimas (rekomenduojama)
```bash
git clone https://github.com/your-username/weather-analysis.git
cd weather-analysis
```

#### Atsisiunčiamas ZIP failas
1. Eikite į GitHub projektą
2. Spauskite "Code" → "Download ZIP"
3. Išskleiskite archyvą
4. Atidarykite terminal'ą projekto kataloge

### 3. Virtual Environment sukūrimas

#### Windows
```powershell
# Sukuriame virtual environment
python -m venv weather_env

# Aktyvuojame
weather_env\Scripts\activate

# Patikrinamas aktyvavimas (turėtų rodoma (weather_env))
```

#### macOS/Linux
```bash
# Sukuriame virtual environment
python3 -m venv weather_env

# Aktyvuojame
source weather_env/bin/activate

# Patikrinamas aktyvavimas (turėtų rodoma (weather_env))
```

### 4. Priklausomybių instaliavimas

```bash
# Atnaujinamas pip
python -m pip install --upgrade pip

# Instaliuojame reikalingas bibliotekas
pip install -r requirements.txt
```

#### Priklausomybių sąrašas
- `pandas>=1.5.0` - Duomenų analizė
- `numpy>=1.24.0` - Matematiniai skaičiavimai
- `requests>=2.28.0` - HTTP užklausos
- `matplotlib>=3.6.0` - Grafikų kūrimas
- `seaborn>=0.12.0` - Statistinės vizualizacijos
- `pytz>=2023.3` - Laiko zonų valdymas
- `jupyter>=1.0.0` - Interaktyvūs notebook'ai
- `pytest>=7.0.0` - Testų sistema
- `scipy>=1.10.0` - Moksliniai skaičiavimai

### 5. Instaliavimo patikrinimas

```bash
# Paleidžiame testus
python -m pytest tests/ -v

# Jei testai praeina - instaliavimas sėkmingas
```

### 6. Pirmojo paleidimo testas

```bash
# Paleidžiame pagrindinę programą
python main.py

# Arba trumpa demo
python -c "from src.weather_api import WeatherAPI; print('Sėkmingai importuota!')"
```

## Galimos problemos ir sprendimai

### Problema: ModuleNotFoundError
**Sprendimas**:
```bash
# Patikrinkite ar active virtual environment
# Windows:
weather_env\Scripts\activate

# macOS/Linux:
source weather_env/bin/activate

# Perkraukite priklausomybes
pip install -r requirements.txt
```

### Problema: SSL Certificate errors
**Sprendimas**:
```bash
# Atnaujinamas certifikatų paketas
pip install --upgrade certifi

# Arba naudojant trusted host
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Problema: Permission denied (Linux/macOS)
**Sprendimas**:
```bash
# Naudokite --user flag
pip install --user -r requirements.txt

# Arba patikrinkite failo teises
chmod +x main.py
```

### Problema: Matplotlib nerodo grafikų
**Sprendimas**:
```bash
# Linux papildomas paketas
sudo apt install python3-tk

# macOS
brew install tcl-tk

# Windows - paprastai dirba iš karto
```

### Problema: Encoding klaidos (Windows)
**Sprendimas**:
- Įsitikinkite, kad terminal'as palaiko UTF-8
- Windows 10+: `chcp 65001`
- Naudokite PowerShell vietoj Command Prompt

## Konfigūracijos parinktys

### Environment variables (pasirinktinai)
Sukurkite `.env` failą projekto kataloge:

```bash
# API konfigūracija
WEATHER_API_TIMEOUT=30
WEATHER_API_RETRIES=3

# Logging lygis
LOG_LEVEL=INFO

# Grafikų konfigūracija
PLOT_DPI=300
PLOT_STYLE=seaborn
```

### Katalogų struktūra po instaliavimo
```
weather-analysis/
├── data/                    # Bus sukurta automatiškai
├── plots/                   # Bus sukurta automatiškai
├── logs/                    # Bus sukurta automatiškai
├── src/                     # Šaltinio kodas
├── tests/                   # Testai
├── docs/                    # Dokumentacija
├── weather_env/             # Virtual environment
├── main.py                  # Pagrindinė programa
├── requirements.txt         # Priklausomybės
└── README.md               # Projekto aprašymas
```

## Atnaujinimas

### Priklausomybių atnaujinimas
```bash
# Aktyvuokite virtual environment
source weather_env/bin/activate  # macOS/Linux
weather_env\Scripts\activate     # Windows

# Atnaujinkite visas priklausomybes
pip install --upgrade -r requirements.txt

# Arba atskiras paketas
pip install --upgrade pandas
```

### Projekto atnaujinimas iš Git
```bash
# Parsisiunčiame naujausius keitimus
git pull origin main

# Atnaujinamas priklausomybes jei reikia
pip install -r requirements.txt

# Paleidžiame testus
python -m pytest tests/ -v
```

## Pašalinimas

### Virtual environment pašalinimas
```bash
# Deaktyvuojame environment
deactivate

# Ištriname katalogą
# Windows:
rmdir /s weather_env

# macOS/Linux:
rm -rf weather_env
```

### Pilnas projekto pašalinimas
```bash
# Pašaliname visą projekto katalogą
# Windows:
rmdir /s weather-analysis

# macOS/Linux:
rm -rf weather-analysis
```

## Pagalba ir palaikymas

### Dokumentacija
- **API dokumentacija**: `docs/api_documentation.md`
- **Naudojimo vadovas**: `docs/usage_guide.md`
- **README failas**: `README.md`

### Problemų pranešimai
1. Patikrinkite ar problema aprašyta šiame vadove
2. Ieškokite panašių problemų GitHub Issues
3. Jei nerandu sprendimo, sukurkite naują Issue su:
   - Python versija (`python --version`)
   - OS informacija
   - Klaidos pranešimas
   - Žingsniai problemai atkurti

### Log failai
Sistema automatiškai kuria log failus:
- `weather_analysis.log` - Pagrindiniai sistema logai
- `data/` kataloge - Duomenų failai ir analizės rezultatai

### Performance optimizavimas
```bash
# Jei turite daug RAM, galite padidinti pandas atminties limitą
export PANDAS_MEMORY_LIMIT=8GB

# Multi-core apdorojimas
export NUMBA_NUM_THREADS=4
```

## Sėkmingo instaliavimo tikrinimo sąrašas

- [ ] Python 3.8+ įdiegtas ir prieinamas PATH
- [ ] Virtual environment sukurtas ir aktyvuotas
- [ ] Visos priklausomybės įdiegtos (`pip list` rodo visas)
- [ ] Testai praeina (`pytest tests/ -v`)
- [ ] Pagrindinė programa paleidžiasi (`python main.py`)
- [ ] Sukuriami grafikų ir duomenų katalogai
- [ ] API prisijungimas veikia (bandykite gauti current weather)

Sėkmingo instaliavimo atveju, sistema yra paruošta naudojimui!

## Dažniausiai užduodami klausimai

**Q: Ar reikia API rakto?**
A: Ne, meteo.lt API yra nemokama ir nereikalauja registracijos.

**Q: Kiek duomenų suvartoja programa?**  
A: Tipiškas 30 dienų duomenų rinkinys - apie 10MB, interpoliuoti duomenys - apie 50MB.

**Q: Ar veikia offline?**
A: Ne, programa reikalauja internetinio ryšio API užklausoms.

**Q: Ar galima naudoti kitą Python versiją?**
A: Rekomenduojama 3.8-3.11. Senesnes versijos nepalaikomos.

**Q: Ar Windows 7 palaikomas?**
A: Ne, rekomenduojama Windows 10 ar naujesnė dėl Python ir bibliotekų palaikymo.
