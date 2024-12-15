import requests

def autocomplete(text):
    p = {text}
    endpoint = f'https://api.scryfall.com/cards/autocomplete?q={p}'
    response = requests.get(endpoint)

    if response.status_code == 200:
        cards_data = response.json().get('data', [])
        for card in cards_data:
            print(card)
            #return card
    else:
        print(f"error: {response.status_code}")
        return None

# if __name__ == "__main__":
#     main()