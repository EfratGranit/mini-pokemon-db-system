from flask import Response, request
from access_to_data import *
import json, requests
from config import my_port
from flask import Flask, Response, request
from poke_api import get_types, get_chain

requests.packages.urllib3.disable_warnings()
app = Flask(__name__, static_url_path='')


@app.route('/update/<name>', methods=['PUT'])
def update_types(name):
    types = get_types(name)
    if not types:
        return Response(json.dumps({'error': 'name not found'}), 406)
    insert_types(types, name)
    return Response(json.dumps({"success": True}), 200)


@app.route('/get_pokemon/<owner_name>')
def get_pokemon(owner_name):
    return Response(json.dumps(find_roster(owner_name)), 200)


@app.route('/get_owners/<pokemon_name>')
def get_owners(pokemon_name):
    return Response(json.dumps(find_owners(pokemon_name)), 200)


@app.route('/add_pokemon/', methods=['POST'])
def add_pokemon():
    pokemon = request.get_json()
    if not pokemon["name"] in get_all_names():
        add_poke(pokemon)
        return Response(json.dumps(pokemon), 201)
    return Response('You can only update this pokemon', 406)


@app.route('/get_by_type/<type>')
def get_by_type(type):
    return Response(json.dumps(find_by_type(type)), 200)


@app.route('/delete_pokemon/<pokemon_name>', methods=['DELETE'])
def delete_pokemon(pokemon_name):
    if delete_pokemon(pokemon_name):
        return Response(json.dumps({"deleted": pokemon_name}), 200)
    return Response(json.dumps("{} not found".format(pokemon_name)), 404)


@app.route('/evolve', methods=['PUT'])
def update_evolve():
    owned_by = request.get_json()
    if owned_by["owner_name"] not in find_owners(owned_by["pokemon_name"]):  # case pair not exist
        return Response(json.dumps({'error': f'pair of pokemon and owner doesnt exist'}), 406)
    chain_item = get_chain(owned_by["pokemon_name"])
    if not len(chain_item):
        return Response(json.dumps({'error': 'no evolution'}), 406)
    update_poke_own(owned_by["pokemon_name"], owned_by["owner_name"], chain_item)
    return Response(json.dumps({'success': 'evolved successfully'}), 200)


if __name__ == '__main__':
    insert_json()
    app.run(port=my_port)
