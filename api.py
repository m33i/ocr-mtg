import requests

def autocomplete(text):
    endpoint = f'https://api.scryfall.com/cards/autocomplete?q={text}'
    response = requests.get(endpoint)

    if response.status_code == 200:
        cards_data = response.json().get('data', [])
        for card in cards_data:
            print(card)
            #return card
    else:
        print(f"error: {response.status_code}")
        return None

def multiverse(id):
    endpoint = f'https://api.scryfall.com/cards/multiverse/{id}'
    response = requests.get(endpoint)

    if response.status_code == 200:
        print(response.json())
    else:
        print(f"error: {response.status_code}")
        return None