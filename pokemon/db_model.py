import json
import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="db_pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def get_all_names():
    with connection.cursor() as cursor:
        query_own = f'select name from pokemon'
        cursor.execute(query_own)
        return json.dumps(cursor.fetchall())


def add_type(name="eevee", type="normal"):
    with connection.cursor() as cursor:
        query_own = f'insert into types (pokemon_name, pokemon_type) values({name}, {type})'
        cursor.execute(query_own)


def add_poke(item):
    with connection.cursor() as cursor:
        query_p = f'insert into pokemon values({item["id"]}, "{item["name"]}", {item["height"]}, {item["weight"]});'
        cursor.execute(query_p)
        for typ in item["type"]:
            query_t = f'insert into types values("{item["name"]}","{typ}")'
            cursor.execute(query_t)
        for owner in item["ownedBy"]:
            cursor.execute(f'select name, town from owner where name="{owner["name"]}"')
            if not cursor.fetchall():
                query_o = f'insert into owner values("{owner["name"]}", "{owner["town"]}");'
                cursor.execute(query_o)
            query_p_o = f'insert into ownedBy values("{item["name"]}", "{owner["name"]}")'
            cursor.execute(query_p_o)
        connection.commit()


# insert basic values from json file into db
def insert_json():
    with connection.cursor() as cursor:
        lines = json.loads(open('./pokemon_data.json', 'r').read())
        for item in lines:
            query_p = f'insert into pokemon values({item["id"]}, "{item["name"]}", {item["height"]}, {item["weight"]});'
            cursor.execute(query_p)
            query_t = f'insert into types values("{item["name"]}","{item["type"]}")'
            cursor.execute(query_t)
            for owner in item["ownedBy"]:
                cursor.execute(f'select name, town from owner where name="{owner["name"]}"')
                if not cursor.fetchall():
                    query_o = f'insert into owner values("{owner["name"]}", "{owner["town"]}");'
                    cursor.execute(query_o)
                query_p_o = f'insert into ownedBy values("{item["name"]}", "{owner["name"]}")'
                cursor.execute(query_p_o)
        connection.commit()


def heaviest_pokemon():
    with connection.cursor() as cursor:
        query_max = f'select MAX(pokemon.weight) AS max_val from pokemon;'
        cursor.execute(query_max)
        result = cursor.fetchall()
        return result[0]['max_val']


def find_by_type(typ):
    arr = []
    with connection.cursor() as cursor:
        query_type = f'select pokemon_name from types where pokemon_type="{typ}"'
        cursor.execute(query_type)
        result = cursor.fetchall()
        for item in result:
            arr += [item['pokemon_name']]
        return arr


def find_owners(p_name):
    arr = []
    with connection.cursor() as cursor:
        query_own = f'select ownedBy.owner_name from ownedBy where pokemon_name="{p_name}"'
        cursor.execute(query_own)
        result = cursor.fetchall()
        for item in result:
            arr += [item['owner_name']]
        return arr


def delete_pokemon(pokemon_name):
    with connection.cursor() as cursor:
        query_own1 = f'DELETE FROM types WHERE pokemon_name = "{pokemon_name}"'
        query_own2 = f'DELETE FROM ownedBy WHERE pokemon_name = "{pokemon_name}"'
        query_own3 = f'DELETE FROM pokemon WHERE name = "{pokemon_name}"'
        cursor.execute(query_own1)
        cursor.execute(query_own2)
        return cursor.execute(query_own3)


def find_roster(owner_name):
    arr = []
    with connection.cursor() as cursor:
        query_own = f'select pokemon_name from ownedBy where owner_name="{owner_name}"'
        cursor.execute(query_own)
        result = cursor.fetchall()
        for item in result:
            arr += [item['pokemon_name']]
        return arr


def finds_most_owned():
    arr, max_o = [], 0
    with connection.cursor() as cursor:
        query_own = 'select count(owner_name), pokemon_name from ownedBy group by pokemon_name'
        cursor.execute(query_own)
        result = cursor.fetchall()
        for item in result:
            if int(item['count(owner_name)']) > max_o:
                max_o = int(item['count(owner_name)'])
                arr = [item['pokemon_name']]
            elif int(item['count(owner_name)']) == max_o:
                arr += [item['pokemon_name']]
        if len(arr) > 1:
            return arr
        return arr[0]


# update the name of given pokemon and owner pair
def update_poke_own(p_name, o_name, new_name):
    with connection.cursor() as cursor:
        query_update = f'update ownedBy set pokemon_name="{new_name}" where pokemon_name="{p_name}" and ' \
                       f'owner_name="{o_name}"'
        cursor.execute(query_update)
        connection.commit()


# update at mySql the new types for given name of pokemon
def insert_types(types, name):
    with connection.cursor() as cursor:
        for i in range(len(types)):
            cursor.execute(
                f'select * from types where types.pokemon_name="{name}" and types.pokemon_type="{types[i]["type"]["name"]}"')
            if not cursor.fetchall():
                query_t = f'insert into types values("{name}","{types[i]["type"]["name"]}")'
                cursor.execute(query_t)
                connection.commit()


# return array of types of pokemon by its name
def get_type_by_name(name):
    arr = []
    with connection.cursor() as cursor:
        query_t = f'select * from types where pokemon_name="{name}"'
        cursor.execute(query_t)
        for item in cursor.fetchall():
            arr += [item["pokemon_type"]]
        return arr
