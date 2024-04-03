import requests

def get_evolution_chain(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        evolution_chain_url = data['evolution_chain']['url']
        return evolution_chain_url
    else:
        print("Error:", response.status_code)
        return None

def get_evolution_details(evolution_chain_url):
    response = requests.get(evolution_chain_url)
    if response.status_code == 200:
        data = response.json()
        return data['chain']
    else:
        print("Error:", response.status_code)
        return None

def get_evolution_methods(chain):
    evolution_methods = {}
    while chain:
        evolution_details = chain['evolution_details'][0]
        if evolution_details.get('trigger').get('name') == 'level-up':
            if 'item' in evolution_details:
                evolution_methods[chain['species']['name']] = f"using a {evolution_details['item']['name'].replace('-', ' ').title()}"

            elif 'held_item' in evolution_details:
                if evolution_details['held_item']['name'] == 'friendship-bracelet':
                    if evolution_details.get('time_of_day') == 'night':
                        evolution_methods[chain['species']['name']] = "when leveled up while holding a Friendship Bracelet in the nighttime"
                    else:
                        evolution_methods[chain['species']['name']] = "when leveled up while holding a Friendship Bracelet in the daytime"

            elif 'known_move_type' in evolution_details:
                move_type = evolution_details['known_move_type']['name']
                evolution_methods[chain['species']['name']] = f"when leveled up while knowing a {move_type.replace('-', ' ').title()} move"

        if chain.get('evolves_to'):
            chain = chain['evolves_to'][0]
        else:
            chain = None
    return evolution_methods

def main(pokemon_name):
    evolution_chain_url = get_evolution_chain(pokemon_name)
    if evolution_chain_url:
        chain = get_evolution_details(evolution_chain_url)
        if chain:
            evolution_methods = get_evolution_methods(chain)
            for pokemon, method in evolution_methods.items():
                print(f"{pokemon.title()} evolves {method}.")

if __name__ == "__main__":
    pokemon_name = input("Enter the Pokémon name: ")
    main(pokemon_name)
