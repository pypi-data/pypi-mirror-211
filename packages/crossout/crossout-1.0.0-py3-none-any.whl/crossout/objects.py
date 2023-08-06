

__all__ = ['Entity', 'Item', 'Recipe', 'Resource', 'Workbenches']


class Entity:
    """Represents an entity with an ID and a name. Used for rarities, categories, factions and types.
    It is not necessary to instantiate an entity manually.
    """

    def __init__(self, __id: int, __name: str) -> None:
        """Builds an entity with the given ID and name

        Parameters
        ----------
        __id : `int`
            The entity's ID
        __name : `str`
            The entity's name
        """
        self.__id = __id
        self.__name = __name

    def __str__(self) -> str:
        return self.__name
    
    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Entity):
            return self.__id == other.__id and self.__name == other.__name
        else:
            return False
        
    @property
    def id(self) -> int:
        """The entity's ID
        """
        return self.__id
    
    @property
    def name(self) -> str:
        """The entity's name
        """
        return self.__name

class Item:
    """Represents an item in Crossout.
    """

    def __init__(self, data: dict) -> None:
        """Builds an item from the given data. 
        An item should not be built manually and rather be retrieved from the `CrossoutDB` class.
        """
        self.id = int(data['id'])
        """The item's ID"""
        self.name = str(data['name'])
        """The item's name"""
        self.description = str(d) if (d := data['description']) else "Not provided."
        """The item's description"""

        self.rarity = Entity(data['rarityId'], data['rarityName'])
        """The item's rarity"""
        self.category = Entity(data['categoryId'], data['categoryName'])
        """The category to which the item belongs"""
        self.type = Entity(data['typeId'], data['typeName'])
        """The type of the item"""
        self.faction = Entity(data['factionNumber'], data['faction'])
        """The faction to which the item belongs"""

        self.img = str(data['imagePath'])
        """Path to the item's image"""

    def __eq__(self, other) -> bool:
        if isinstance(other, Item):
            return self.id == other.id
        else:
            return False

class Resource:
    """Represents a resource in Crossout.
    """

    def __init__(self, data: dict) -> None:
        self.id = int(data['id'])
        """The resource's ID"""
        self.name = str(data['name']).replace(' x100', '')
        """The resource's name without the 'x100' suffix"""
        self.description = str(d) if (d := data['description']) else "Not provided."
        """The resource's description"""

        self.img = str(data['imagePath'])
        """Path to the resource's image"""

    def __eq__(self, other) -> bool:
        if isinstance(other, Resource):
            return self.id == other.id
        else:
            return False

class Workbench:
    """Represents a workbench in Crossout. A workbench is defined independently of any faction.
    It is not necessary to instantiate a workbench manually as
    all base workbenches are already defined as class attributes of the `Workbenches` class.
    """

    def __init__(self, price: int, name: str) -> None:
        """Instantiates a workbench with the given price and name.

        Parameters
        ----------
        price : `int`
            The workbench's fee required to use the workbench, namely to craft an item
        name : `str`
            The workbench's name
        """
        self.price = price
        """Amount of coins required to use the workbench"""
        self.name = name
        """The workbench's name"""

    @property
    def fullName(self) -> str:
        """The workbench's full name
        """
        return f'{self.name} Workbench'

class Workbenches:
    """Represents all workbenches in Crossout. All workbenches types are defined as class attributes."""

    COMMON = Workbench(0, 'Common')
    """The common workbench, unique to Enginneers faction"""
    RARE = Workbench(3, 'Rare')
    """The rare workbench"""
    SPECIAL = Workbench(6, 'Special')
    """The special workbench"""
    EPIC = Workbench(15, 'Epic')
    """The epic workbench"""
    LEGENDARY = Workbench(75, 'Legendary')
    """The legendary workbench"""
    RELIC = Workbench(0, 'Relic')
    """The relic workbench"""

    @staticmethod
    def fromRarityName(rarity_name: str) -> Workbench:
        """Returns the base workbench that matches the given rarity name

        Parameters
        ----------
        rarity_name : `str`
            The rarity name of the workbench to return

        Returns
        -------
        `Workbench`
            The base workbench that matches the given rarity name

        Raises
        ------
        `ValueError`
            If no workbench matches the given rarity name
        """
        wbs = [
            Workbenches.COMMON,
            Workbenches.RARE,
            Workbenches.SPECIAL,
            Workbenches.EPIC,
            Workbenches.LEGENDARY,
            Workbenches.RELIC
        ]
        for w in wbs:
            if w.name == rarity_name:
                return w
        raise ValueError(f'No workbench with name {rarity_name}')

class Recipe:
    """Represents a recipe in Crossout, that is, a list of the objects required to craft an item.
    
    Recipes can be obtained from the `CrossoutDB` class and thus, should not be instantiated manually.
    
    A recipe is never linked to the item that can be crafted with it nor has any identifier,
    and as such it is not possible to know which item can be crafted knowing only the recipe.
    It should be linked to the item it crafts by the user of the library.
    """

    def __init__(self,
                 items: list[tuple[Item, int]],
                 resources: list[tuple[Resource, int]],
                 workbench: Workbench,
                 faction: Entity
                ) -> None:
        """Builds a recipe that requires the given items and resources to be crafted
        at the given workbench of the given faction.

        Parameters
        ----------
        items : `list[tuple[Item, int]]`
            A list of tuples of items and their respective quantities required to craft the item
        resources : `list[tuple[Resource, int]]`
            A list of tuples of resources and their respective quantities required to craft the item
        workbench : `Workbench`
            The workbench at which the item can be crafted
        faction : `Entity`
            The faction of the used workbench
        """
        self.items = items
        """A list of tuples of items and their respective quantities required to craft the item"""
        self.resources = resources
        """A list of tuples of resources and their respective quantities required to craft the item"""
        self.workbench = workbench
        """The workbench at which the item can be crafted"""
        self.faction = faction
        """The faction of the used workbench"""