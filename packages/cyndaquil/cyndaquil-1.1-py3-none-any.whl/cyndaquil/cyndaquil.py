import requests
import argparse
from exceptions import *

parser = argparse.ArgumentParser()
URL = "https://pokeapi.co/api/v2/{category}/{search}"

class Pokemon():
    def __init__(self, name):
        self.name = name
        self.number = 0
        self.type_1 = None
        self.type_2 = None
        self.ability_1 = None
        self.ability_2 = None
        self.ability_hidden = None
        self.catch_rate = 0
        self.lvl_rate = None
        self.weight = 0
        self.height = 0
        self.stats = {
            "HP" : 0,
            "Attack" : 0,
            "Defense" : 0,
            "Sp Attack" : 0,
            "Sp Defense" : 0,
            "Speed" : 0
        }
        self.ev_yield = {
            "HP" : 0,
            "Attack" : 0,
            "Defense" : 0,
            "Sp. Attack" : 0,
            "Sp. Defense" : 0,
            "Speed" : 0
        }
        self.base_exp = 0
        self.base_friendship = 0
        self.color = None
        self.evolves_from = None
        self.egg_group_1 = None
        self.egg_group_2 = None

        self.lookup_pokemon()

    def lookup_pokemon(self):
        global URL

        pokemon_response = requests.get(URL.format(category="pokemon",search=self.name))
        species_response = requests.get(URL.format(category="pokemon-species",search=self.name))

        if "Not Found" in pokemon_response.text:
            raise PokemonNotFound(self.name)
        else:
            pokemon_data = pokemon_response.json()
            species_data = species_response.json()
        
        self.number = pokemon_data["game_indices"][0]["game_index"]
        self.type_1 = pokemon_data["types"][0]["type"]["name"]
        if len(pokemon_data["types"]) > 1:
            self.type_2 = pokemon_data["types"][1]["type"]["name"]
        self.ability = pokemon_data["abilities"][0]["ability"]["name"]
        if len(pokemon_data["abilities"]) == 2:
            if pokemon_data["abilities"][1]["is_hidden"] == True:
                self.ability_hidden = pokemon_data["abilities"][1]["ability"]["name"]
        if len(pokemon_data["abilities"]) == 3:
            self.ability_2 = pokemon_data["abilities"][1]["ability"]["name"]
            self.ability_hidden = pokemon_data["abilities"][2]["ability"]["name"]
        self.catch_rate = species_data["capture_rate"]
        self.lvl_rate = species_data["growth_rate"]["name"]
        self.weight = pokemon_data["weight"] / 100
        self.height = pokemon_data["height"] / 100
        self.stats["HP"] = pokemon_data["stats"][0]["base_stat"]
        self.stats["Attack"] = pokemon_data["stats"][1]["base_stat"]
        self.stats["Defense"] = pokemon_data["stats"][2]["base_stat"]
        self.stats["Sp Attack"] = pokemon_data["stats"][3]["base_stat"]
        self.stats["Sp Defense"] = pokemon_data["stats"][4]["base_stat"]
        self.stats["Speed"] = pokemon_data["stats"][0]["base_stat"]
        self.ev_yield["HP"] = pokemon_data["stats"][0]["effort"]
        self.ev_yield["Attack"] = pokemon_data["stats"][1]["effort"]
        self.ev_yield["Defense"] = pokemon_data["stats"][2]["effort"]
        self.ev_yield["Sp Attack"] = pokemon_data["stats"][3]["effort"]
        self.ev_yield["Sp Defense"] = pokemon_data["stats"][4]["effort"]
        self.ev_yield["Speed"] = pokemon_data["stats"][0]["effort"]
        self.base_exp = pokemon_data["base_experience"]
        self.base_friendship = species_data["base_happiness"]
        self.color = species_data["color"]["name"]
        self.evolves_from = species_data["evolves_from_species"]
        self.egg_group_1 = species_data["egg_groups"][0]["name"]
        if len(species_data["egg_groups"]) == 2:
            self.egg_group_2 = species_data["egg_groups"][1]["name"]

class Item():
    def __init__(self, name):

        if " " in name:
            raise ItemNameError(name)

        self.name = name
        self.id = None
        self.cost = 0
        self.attribute = []
        self.category = None
        self.effect = None
        self.short_effect = None
        self.fling_power = 0
        self.fling_effect = None
        self.held_by = None

        self.lookup_item()

    def lookup_item(self):
        global URL
        item_response = requests.get((URL.format(category="item",search=self.name)))

        if "Not Found" in item_response.text:
            raise ItemNotFound(self.name)
        else:
            item_data = item_response.json()

        self.id = item_data["id"]
        self.cost = item_data["cost"]
        for attribute in item_data["attributes"]:
            self.attribute.append(attribute["name"])
        self.category = item_data["category"]["name"]
        self.effect = item_data["effect_entries"][0]["effect"]
        self.short_effect = item_data["effect_entries"][0]["short_effect"]
        self.fling_power = item_data["fling_power"]
        self.fling_effect = item_data["fling_effect"]
        self.held_by = item_data["held_by_pokemon"]

class Berry():
    def __init__(self,name):
        self.name = name
        self.id = 0
        self.flavors = {
            "Spicy" : 0,
            "Dry" : 0,
            "Sweet" : 0,
            "Bitter" : 0,
            "Sour" : 0,
        }
        self.firmness = 0
        self.size = 0
        self.smoothness = 0
        self.natural_gift_power = 0
        self.natural_gift_type = None
        self.max_harvest = 0

        self.item_url = 0
        self.cost = 0
        self.attribute = []
        self.category = None
        self.baby_trigger_for = None
        self.effect = None
        self.short_effect = None
        self.fling_power = 0
        self.fling_effect = None
        self.held_by = None

        self.lookup_berry()
    
    def lookup_berry(self):
        global URL
        berry_response = requests.get((URL.format(category="berry",search=self.name)))
        

        if "Not Found" in berry_response.text:
            raise BerryNotFound(self.name)
        else:
            berry_data = berry_response.json()
            
        self.id = berry_data["id"]
        self.flavors["Spicy"] = berry_data["flavors"][0]["potency"]
        self.flavors["Dry"] = berry_data["flavors"][1]["potency"]
        self.flavors["Sweet"] = berry_data["flavors"][2]["potency"]
        self.flavors["Bitter"] = berry_data["flavors"][3]["potency"]
        self.flavors["Sour"] = berry_data["flavors"][4]["potency"]
        self.firmness = berry_data["firmness"]["name"]
        self.size = berry_data["size"]
        self.smoothness = berry_data["smoothness"]
        self.natural_gift_power = berry_data["natural_gift_power"]
        self.natural_gift_type = berry_data["natural_gift_type"]["name"]

        self.item_url = berry_data["item"]["url"]

        berry_item_response = requests.get(url=self.item_url)
        if "Not Found" in berry_item_response.text:
            raise BerryItemNotFound(self.name)
        else:
            berry_item_data = berry_item_response.json()

        self.cost = berry_item_data["cost"]
        for attribute in berry_item_data["attributes"]:
            self.attribute.append(attribute["name"])
        self.category = berry_item_data["category"]["name"]
        self.baby_trigger_for = berry_item_data["baby_trigger_for"]
        self.effect = berry_item_data["effect_entries"][0]["effect"]
        self.short_effect = berry_item_data["effect_entries"][0]["short_effect"]
        self.fling_power = berry_item_data["fling_power"]
        self.fling_effect = berry_item_data["fling_effect"]
        self.held_by = berry_item_data["held_by_pokemon"]




def main():
    #testing functions and classes
    cyndaquil = Pokemon('cyndaquil')
    print(cyndaquil.number)

    pokeball = Item('poke-ball')
    print(pokeball.cost)

    chesto = Berry('chesto')
    print(chesto.firmness)



if __name__ == "__main__":
    main()