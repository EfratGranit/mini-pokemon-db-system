from config import poke_info
import requests


# reach the evolve and return it, if doesnt exist return empty string
def get_chain(name):
    res = requests.get(url=poke_info + name, verify=False)
    species_info = res.json()['species']['url']
    res = requests.get(url=species_info, verify=False)
    evo_info = res.json()['evolution_chain']['url']
    res = requests.get(url=evo_info, verify=False)
    chain_item = res.json()['chain']['evolves_to']
    if not len(chain_item):
        return ''
    return chain_item[0]['species']['name']


# do the request to get array of types from pokeApi and return it
def get_types(name):
    res = requests.get(url=poke_info + name, verify=False)
    if res.status_code == 404:
        return None
    return res.json()['types']
