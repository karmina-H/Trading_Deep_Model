import requests

def get_price(name):

    url = f"https://api.bithumb.com/v1/ticker?markets={name}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    print(response.text)
