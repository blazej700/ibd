### Teashop server

## Instalacja

Na ubuntu zamiast `python` to `python3`, `pip` to `pip3`.
Na windowsie `python3`, `python` albo `py` ale wydaje mi się że `python3` bd spoko. Z `pip` analogicznie.

Jeśli nie mamy venv:
```bash
$ python -m pip install --user virtualenv
```

W katologu servera:
```bash
$ python -m venv venv
```
Linux:
```bash
$ source venv/bin/activate
```

Windows:
```
venv\Scripts\activate
```


```bash
(venv) $ pip install -r requirements.txt 
```

Uruchomienie:
```bash
(venv) $ flask run
```


Swagger:
```http
http://localhost:5000/api/doc/
```
