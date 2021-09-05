import json
import requests
from config import url_db
from access_to_data import get_type_by_name, find_by_type, find_roster, add_type, add_poke


def test_update_types():
    res = requests.put(url=url_db + 'update/venusaur')
    assert 'grass' in get_type_by_name('venusaur'), 'test failed'
    assert 'poison' in get_type_by_name('venusaur'), 'test failed'
    assert 'venusaur' in find_by_type('grass'), 'test failed'
    assert 'venusaur' in find_by_type('poison'), 'test failed'


def test_evolve():
    res = requests.put(url=url_db + 'evolve',
                       json={"pokemon_name": "pinsir", "owner_name": "Drake"})
    assert res.json() == {'error': 'no evolution'}, 'test failed'
    res = requests.put(url=url_db + 'evolve',
                       json={"pokemon_name": "spearow", "owner_name": "Archie"})
    assert res.json() == {
        'error': f'pair of pokemon and owner doesnt exist'}, 'test failed'
    res = requests.put(url=url_db + 'evolve',
                       json={"pokemon_name": "oddish", "owner_name": "Whitney"})
    assert res.json() == {'success': 'evolved successfully'}, 'test failed'
    res = requests.put(url=url_db + 'evolve',
                       json={"pokemon_name": "oddish", "owner_name": "Whitney"})
    assert res.json() == {
        'error': f'pair of pokemon and owner doesnt exist'}, 'test failed'
    assert 'gloom' in find_roster('Whitney'), 'test failed'
    poks = find_roster('raichu')
    if 'pikachu' in poks and 'raichu' in poks:
        res = requests.put(
            url=url_db + 'evolve', json={"pokemon_name": "pikachu", "owner_name": "Whitney"})



def test1_by_type(type="normal"):
    add_type()
    res = requests.get(url=url_db + 'get_by_type/' + type)
    assert "eevee" in res.text


def test2_by_type(name="eevee"):
    res = requests.get(url=url_db + 'update/' + name)
    assert res.status_code == 200


def test_add_pokemon(name="yanma"):
    poke = json.dumps({"id": 193, "name": name, "height": 12, "weight": 7, "type": ["bug", "flying"], "ownedBy": []})
    requests.post(url_db + 'add_pokemon/', poke)
    res = requests.get(url=url_db + 'get_by_type/' + "bug")
    assert name in res.text
    res = requests.get(url=url_db + 'get_by_type/' + "flying")
    assert name in res.text


def test_get_by_owner(name="Drasna"):
    res = requests.get(url_db + '/get_pokemon/' + name)
    assert res.text == json.dumps(
        ["wartortle", "caterpie", "beedrill", "arbok", "clefairy", "wigglytuff", "persian", "growlithe", "machamp",
         "golem", "dodrio", "hypno", "cubone", "eevee", "kabutops"])


def test_get_owners(name_poke="charmander"):
    res = requests.get(url_db + '/get_owners/' + name_poke)
    for owner in json.dumps(["Giovanni", "Jasmine", "Whitney"]):
        assert owner in res.text
    for owner in res.text:
        assert owner in json.dumps(["Giovanni", "Jasmine", "Whitney"])
