# ArkToolsNom

Herramienta de gestión para a2Nómina.

**Versión:** 0.00.01
**Desarrollador:** Juan E. Páez M. - JUEPAE

## Requisitos

- Python 3.14.4 (32 bits) — requerido para ODBC DBISAM
- Dependencias: ver `requirements.txt`

## Instalación

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt

cd src
python main.py

ArkToolsNom/
├── config/          Configuración de conexiones
├── data/            Archivos de entrada (Excel, CSV)
├── logs/            Archivos de log
└── src/             Código fuente
    └── modules/     Módulos específicos de nómina

