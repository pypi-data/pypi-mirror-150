class PokemonNotFound(Exception):
    def __init__(self, pokemon, message="Pokemon not found"):
        self.pokemon = pokemon
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.pokemon} -> {self.message}'

class ItemNotFound(Exception):
    def __init__(self, item, message="Item not found"):
        self.item = item
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.item} -> {self.message}'

class BerryNotFound(Exception):
    def __init__(self, berry, message="Berry not found"):
        self.berry = berry
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.berry} -> {self.message}'

class BerryItemNotFound(Exception):
    def __init__(
        self,
        berry,
        message="Berry item not found\nThe item page for this berry might be missing"
    ):
        self.berry = berry
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.berry} -> {self.message}'

class ItemNameError(Exception):
    def __init__(
        self, 
        item,
        message="Item names must not contain spaces. Replace Spaces with -"
    ):
        self.item = item
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.item} -> {self.message}'