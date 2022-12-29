from django.conf import settings
import requests
import random


def send_otp_to_phone(phone_number):
    try:
        otp = random.randint(1000, 9999)
        # api_key = settings.API_KEY
        # url = f'https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}'
        # response = requests.get(url)
        # print(response)
        # print(response)
        print(otp)
        return otp
    except Exception as e:
        print(e)
        return e
