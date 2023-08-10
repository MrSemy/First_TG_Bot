import json
import requests
from config import exchanges, API_KEY


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        if amount <= 0:
            raise APIException(f'Не удалось обработать количество {amount}!')

        # проверка переменной API_KEY на валидность
        if API_KEY == "введите сюда свой API KEY" or not API_KEY.isalnum():
            raise APIException("не валидный API KEY, проверьте файл config.py!")

        payload = {}
        headers = {
            "apikey": API_KEY
        }

        r = requests.request("GET", f"https://api.apilayer.com/fixer/convert?to={sym_key}&from={base_key}&amount={amount}", headers=headers, data=payload)
        if r.status_code != 200:
            raise APIException(f"Не удалось обработать запрос: {r.status_code}")

        resp = json.loads(r.content)


        new_price = resp['result']
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return message
