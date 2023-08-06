from .CrossoutDBAPI import CrossoutDBAPI
from .objects import *


__all__ = ['CrossoutDB']


class CrossoutDB:
    """A wrapper for the `CrossoutDBAPI` class.
    
    Returns objects from the `objects` module instead of dicts.
    """

    def __init__(self):
        """Initializes a new `CrossoutDB` instance.
        """
        super().__init__()
        self.__api = CrossoutDBAPI()

    def items(self,
            rarity: str | None = None,
            category: str | None = None,
            faction: str | None = None,
            query: str | None = None
        ) -> list[Item]:
        """Returns a list of items matching the given parameters.

        Parameters
        ----------
        rarity : `str`, optional
            Filters by rarity name
        category : `str`, optional
            Filters by category name
        faction : `str`, optional
            Filters by faction name
        query : `str`, optional
            Filters items corresponding to the given query

        Returns
        -------
        `list[Item]`
            A list of items, can be empty if no items match the given parameters
        """        
        s = self.__api.items(
            rarity=rarity,
            category=category,
            faction=faction,
            query=query
        )
        # Add the website URL to the image path
        for i in s:
            i['imagePath'] = self.__api.website_url + i['imagePath']
        return list(Item(i) for i in s)
    
    def item(self, item_id: int) -> Item:
        """Returns the item matching the given ID.

        Parameters
        ----------
        item_id : `int`
            An item's ID

        Returns
        -------
        `Item`
            The item matching the given ID if it exists

        Raises
        ------
        `ValueError`
            If the API did not found the item with the given ID
        """
        try:
            i = self.__api.item(item_id)
        except ValueError as e:
            raise ValueError(f'API error : {e}')
        i['imagePath'] = self.__api.website_url + i['imagePath']
        return Item(i)
    
    def __buildEntityList(self, objects: list[dict]) -> list[Entity]:
        return list(Entity(o['id'], o['name']) for o in objects)

    def rarities(self) -> list[Entity]:
        """Returns a list of all item rarities.

        Returns
        -------
        `list[Entity]`
            A list of all rarities
        """
        return self.__buildEntityList(self.__api.rarities())
    
    def categories(self) -> list[Entity]:
        """Returns a list of all item categories.

        Returns
        -------
        `list[Entity]`
            A list of all categories
        """
        return self.__buildEntityList(self.__api.categories())

    def factions(self) -> list[Entity]:
        """Returns a list of all factions.

        Returns
        -------
        `list[Entity]`
            A list of all factions
        """
        return self.__buildEntityList(self.__api.factions())
    
    def types(self) -> list[Entity]:
        """Returns a list of all item types.

        Returns
        -------
        `list[Entity]`
            A list of all factions
        """
        return self.__buildEntityList(self.__api.types())
    
    def recipe(self, item: Item) -> Recipe:
        """Returns the recipe that can be used to craft the given item.

        Parameters
        ----------
        item : `Item`
            The item to craft

        Returns
        -------
        `Recipe`
            The recipe crafting the given item

        Raises
        ------
        `ValueError`
            If the API did not found the recipe
        """
        try:
            r = self.__api.recipe(item.id)
        except ValueError as e:
            raise ValueError(f'API error : {e}')
        assert r['item']['id'] == item.id

        items = []
        resources = []
        workbench = Workbenches.fromRarityName(item.rarity.name)
        
        for ing in r['ingredients']:
            if ing['item']['categoryName'] == 'Resources':
                resources.append(
                    (Resource(self.__api.item(ing['item']['id'])), ing['number'])
                )
            else:
                items.append(
                    (self.item(ing['item']['id']), ing['number'])
                )

        return Recipe(items, resources, workbench, item.faction)
