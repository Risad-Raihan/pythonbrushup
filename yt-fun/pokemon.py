import requests

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        return url, response.json()
    else:
        print(f"Failed to retrieve data {response.status_code}")
        return None, None

pokemon_name = "pikachu"
url, pokemon_info = get_pokemon_info(pokemon_name)

if pokemon_info:
    print("URL:", url)
    print(f"Name: {pokemon_info['name'].capitalize()}")
