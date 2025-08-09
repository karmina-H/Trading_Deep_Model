import requests

def get_names():
    url = "https://api.bithumb.com/v1/market/all?isDetails=false"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    return response.text
