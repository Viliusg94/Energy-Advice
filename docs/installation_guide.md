# Instaliavimo instrukcijos

## Sistemos reikalavimai

### OperacinÄ—s sistemos
 Windows 10/11
 macOS 10.14+
 Linux (Ubuntu 18.04+, CentOS 7+)

### Python versija
 Python 3.8 arba naujesnÄ—
 pip package manager

### Internetinis ryÅys
 BÅ«tinas ryÅys su api.meteo.lt API

## 1. Python aplinkos paruoÅimas

### Windows

#### 1.1 Python instaliavimas
```powershell
# AtsisiÅ³skite Python iÅ python.org arba naudokite winget
winget install Python.Python.3.11

# Patikrinkite instaliacijÄ…
python version
pip version
```

#### 1.2 Virtual environment sukÅ«rimas
```powershell
# Sukurkite virtual environment
python m venv weather_env

# Aktyvuokite
weather_env\Scripts\activate

# Patikrinkite
where python
```

### macOS

#### 1.1 Python instaliavimas
```bash
# Naudojant Homebrew (rekomenduojama)
brew install python

# Arba naudojant pyenv
brew install pyenv
pyenv install 3.11.0
pyenv global 3.11.0

# Patikrinkite
python3 version
pip3 version
```

#### 1.2 Virtual environment sukÅ«rimas
```bash
# Sukurkite virtual environment
python3 m venv weather_env

# Aktyvuokite
source weather_env/bin/activate

# Patikrinkite
which python
```

### Linux (Ubuntu/Debian)

#### 1.1 Python instaliavimas
```bash
# Atnaujinkite package list
sudo apt update

# Ä®diekite Python ir pip
sudo apt install python3 python3pip python3venv

# Patikrinkite
python3 version
pip3 version
```

#### 1.2 Virtual environment sukÅ«rimas
```bash
# Sukurkite virtual environment
python3 m venv weather_env

# Aktyvuokite
source weather_env/bin/activate

# Patikrinkite
which python
```

## 2. Projekto atsisiuntimas

### Git metodu (rekomenduojama)
```bash
# Klonuokite repozitorijÄ…
git clone https://github.com/yourusername/weatheranalysis.git
cd weatheranalysis

# Arba jei turite SSH
git clone git@github.com:yourusername/weatheranalysis.git
cd weatheranalysis
```

### ZIP archyvo metodu
1. AtsisiÅ³skite ZIP failÄ… iÅ GitHub
2. IÅarchyvuokite ÄÆ norimÄ… katalogÄ…
3. Atidarykite terminalÄ…/komandinÄ™ eilutÄ™ kataloge

## 3. PriklausomybiÅ³ instaliavimas

### 3.1 PagrindinÄ—s bibliotekos
```bash
# Ä®sitikinkite kad virtual environment aktyvuotas
# Windows: weather_env\Scripts\activate
# macOS/Linux: source weather_env/bin/activate

# Ä®diekite priklausomybes
pip install r requirements.txt

# Arba rankiniu bÅ«du
pip install pandas>=1.5.0
pip install numpy>=1.24.0
pip install requests>=2.28.0
pip install matplotlib>=3.6.0
pip install seaborn>=0.12.0
pip install pytz>=2023.3
pip install jupyter>=1.0.0
pip install pytest>=7.0.0
```

### 3.2 Patikrinkite instaliacijÄ…
```python
# Paleiskite Python ir patikrinkite importus
python c "
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pytz
print('Visos bibliotekos sÄ—kmingai ÄÆdiegtos!')
print(f'Pandas: {pd.__version__}')
print(f'NumPy: {np.__version__}')
"
```

## 4. Projekto konfigÅ«racija

### 4.1 KatalogÅ³ struktÅ«ros patikrinimas
```bash
# Patikrinkite ar yra visi katalogai
ls la
# TurÄ—tumÄ—te matyti:
# src/
# notebooks/
# tests/
# data/
# plots/
# docs/
```

### 4.2 TestÅ³ paleidimas
```bash
# Paleiskite unit testus
python m pytest tests/ v

# Arba konkreÄ¨iÄ… testÅ³ klasÄ™
python m pytest tests/test_weather_api.py v

# Su coverage report
pip install pytestcov
python m pytest tests/ cov=src covreport=html
```

## 5. Programos paleidimas

### 5.1 Pagrindinis script'as
```bash
# Paleiskite pagrindinÄ™ programÄ…
python main.py
```

### 5.2 Jupyter Notebook
```bash
# Paleiskite Jupyter server
jupyter notebook

# Atidarykite notebooks/weather_analysis.ipynb
# Arba naudokite Jupyter Lab
jupyter lab
```

### 5.3 Interaktyvus reÅ¾imas
```python
# Paleiskite Python REPL
python

# Importuokite modulius
import sys
sys.path.append('src')

from weather_api import WeatherAPI
from data_analysis import WeatherAnalyzer

# Sukurkite API objektÄ…
api = WeatherAPI("vilnius")
print("API sÄ—kmingai inicializuotas!")
```

## 6. KonfigÅ«racijos nustatymai

### 6.1 Environment variables (Pasirinktinai)
```bash
# Linux/macOS
export WEATHER_API_URL="https://api.meteo.lt/"
export DEFAULT_CITY="vilnius"
export OUTPUT_DIR="./plots"

# Windows
set WEATHER_API_URL=https://api.meteo.lt/
set DEFAULT_CITY=vilnius
set OUTPUT_DIR=./plots
```

### 6.2 Logging konfigÅ«racija
```python
# Sukurkite logging.conf failÄ… (pasirinktinai)
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(name)s  %(levelname)s  %(message)s',
    handlers=[
        logging.FileHandler('weather_analysis.log'),
        logging.StreamHandler()
    ]
)
```

## 7. Troubleshooting

### 7.1 DaÅ¾nos problemos

#### Python versijos klaida
```bash
# Klaida: "Python 3.8+ required"
# Sprendimas: Atnaujinkite Python
python version  # Patikrinkite versijÄ…
```

#### SSL/HTTPS klaidos
```bash
# Klaida: SSL certificate verify failed
# Sprendimas:
pip install trustedhost pypi.org trustedhost pypi.python.org trustedhost files.pythonhosted.org requests
```

#### Import klaidos
```python
# Klaida: ModuleNotFoundError
# Sprendimas: Patikrinkite Python path
import sys
print(sys.path)
sys.path.append('./src')  # PridÄ—kite src katalogÄ…
```

#### API klaidos
```bash
# Klaida: Connection refused
# Patikrinkite internetinÄÆ ryÅÄÆ
curl I https://api.meteo.lt/

# Klaida: 429 Too Many Requests
# Palaukite kelias minutes tarp uÅ¾klausÅ³
```

### 7.2 Diagnostic script'as
```python
# diagnostic.py
import sys
import subprocess
import importlib

def check_python_version():
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"ā… Python versija OK: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"ā¯ Python versija per sena: {version.major}.{version.minor}.{version.micro}")
        return False

def check_packages():
    required_packages = [
        'pandas', 'numpy', 'requests', 
        'matplotlib', 'seaborn', 'pytz'
    ]
    
    missing = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"ā… {package}  OK")
        except ImportError:
            print(f"ā¯ {package}  TRÅŖKSTA")
            missing.append(package)
    
    return missing

def check_internet():
    try:
        import requests
        response = requests.get('https://api.meteo.lt/', timeout=5)
        print("ā… API prieinamumas  OK")
        return True
    except:
        print("ā¯ API neprieinamas")
        return False

if __name__ == "__main__":
    print("š”¨ SISTEMOS PATIKRINIMAS")
    print("=" * 30)
    
    python_ok = check_python_version()
    missing_packages = check_packages()
    api_ok = check_internet()
    
    print("\nš“‹ SUVESTINÄ–:")
    if python_ok and not missing_packages and api_ok:
        print("šˇ‰ Sistema paruoÅta naudojimui!")
    else:
        print("ā ļø¸ Reikia iÅsprÄ™sti problemas:")
        if not python_ok:
            print("    Atnaujinkite Python iki 3.8+")
        if missing_packages:
            print(f"    Ä®diekite: pip install {' '.join(missing_packages)}")
        if not api_ok:
            print("    Patikrinkite internetinÄÆ ryÅÄÆ")
```

### 7.3 Performance tikrinimas
```bash
# Atminties naudojimas
python c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Atminties naudojimas: {process.memory_info().rss / 1024 / 1024:.2f} MB')
"

# DuomenÅ³ apdorojimo greitis
python c "
import time
import pandas as pd
import numpy as np

start = time.time()
df = pd.DataFrame(np.random.randn(10000, 10))
df.describe()
end = time.time()

print(f'Pandas performance: {end  start:.4f} sekundÄ—s')
"
```

## 8. IDE setup (pasirinktinai)

### 8.1 VS Code
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./weather_env/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true
}
```

### 8.2 PyCharm
1. File ā†’ Settings ā†’ Project ā†’ Python Interpreter
2. Pasirinkite weather_env/bin/python
3. PridÄ—kite src/ prie PYTHONPATH

## 9. Atnaujinimas

### 9.1 Projekto atnaujinimas
```bash
# Git pull
git pull origin main

# Atnaujinkite priklausomybes
pip install r requirements.txt upgrade
```

### 9.2 BibliotekÅ³ atnaujinimas
```bash
# Atnaujinkite visas bibliotekas
pip list outdated
pip install upgrade pip
pip install upgrade pandas numpy matplotlib seaborn requests
```



## ā… SÄ—kmingo ÄÆdiegimo patikrinimas

Jei viskas ÄÆdiegta teisingai, turÄ—tumÄ—te galÄ—ti paleisti:

```bash
# 1. PagrindinÄÆ script'Ä…
python main.py

# 2. Testus
python m pytest tests/ v

# 3. Jupyter notebook
jupyter notebook notebooks/weather_analysis.ipynb
```

Ir matyti tokius rezultatus:
 ā… DuomenÅ³ nuskaitymas iÅ API
 ā… AnalizÄ—s rezultatÅ³ spausdinimas  
 ā… GrafikÅ³ kÅ«rimas plots/ kataloge
 ā… DuomenÅ³ iÅsaugojimas data/ kataloge

**Jei kyla problemÅ³, perÅ¾iÅ«rÄ—kite Troubleshooting skyriÅ³ arba susisiekite su projekto palaikymo komanda.**
