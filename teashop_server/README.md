### Teashop server

## Instalacja

Na ubuntu zamiast `python` to `python3`, `pip` to `pip3`.
Na windowsie `python3`, `python` albo `py` niewiem xd. Z `pip` analogicznie.

Jeśli nie mamy venv:
```bash
python -m pip install --user virtualenv
```

W katologu servera:
```bash
python -m venv venv
```

```bash
pip install -r requirements.txt 
```

Uruchomienie:
```bash
flask run
```


Swagger:
```http
http://localhost:5000/api/doc/
```