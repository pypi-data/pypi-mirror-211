# Validierung von Metadaten pro Portal 

Wir können eine Portal URL (DKAN oder CKAN Portale) übergeben und dann bekommen wir eine
JSON Datei mit der Validierung aller vorhandenen Datensätze.

![console screenshot](screenshot.png)


# Installation
Zur Installation des Packages mit pipx (pip geht auch):

```bash
pipx install dcat-ap-de-validator
```

## Verfügare Kommandos:

- `portal` für Portalvalidierung

## Parameter

- `url` der erste Parameter ist die URL des Portals oder einzelne Metadaten-URL
- `-p` Portal Typ: `ckan` oder `dkan`

# Aufruf

Wenn als Package installiert:

```bash
dcat_ap_de_validator portal https://opendata.heilbronn.de/ -p dkan
```

Direkter aufruf:

```bash
python -m dcat_ap_de_validator portal https://opendata.heilbronn.de/ -p dkan
```

# Rückgabe

Die Ausgabe ist ein json File im Root Ordern, der den Namen des Portales beinhaltet.

## Format

In dem JSON File ist auf der Root Ebene folgendes verfügbar:

```json
{
    "portal": "Name of the Portal title"
    "valid_datasets": 1,
    "errors": 2,
    "warnings": 5,
    "infos": 2,
    "results": [
        {
            "package": "idofthepackage",
            "url": "http://portal.gov/idofpakcage",
            "result": {
                "valid": true,
                "warning": 1,
                "error": 0,
                "info": 0
            }
        }
    ]

}
```
