import urllib.parse

import requests


__all__ = ['CrossoutDBAPI']


class CrossoutDBAPI:
    """
    Low-level class that retrieves raw data as JSON from the CrossoutDB API.
    
    Requires an internet connection.
    """

    def __init__(self, website_url: str = 'https://crossoutdb.com', api_endpoint: str = '/api/v1/') -> None:
        """Builds a `CrossoutDBAPI` object.

        Parameters
        ----------
        website_url : `str`, optional
            The URL of the CrossoutDB website. It should not be changed unless the website URL changes
        api_endpoint : `str`, optional
            The API's endpoint. Currently, the API version is in its first version
        """
        self.website_url = website_url
        """The URL of the CrossoutDB website"""
        self.__api_endpoint = api_endpoint

    @property
    def api_url(self) -> str:
        """The URL of the web API
        """
        return self.website_url + self.__api_endpoint

    def request(self, endpoint: str) -> list[dict]:
        """Makes a request to the CrossoutDB API and returns the result in JSON format.

        Parameters
        ----------
        endpoint : `str`
            Name of the endpoint to request

        Returns
        -------
        `list[dict]`
            A list of dicts retrieved from the CrossoutDB API. The list contains at least one dict.

        Raises
        ------
        `HTTPError`
            If the request failed
        `TypeError`
            If the response is not JSON
        """
        r = requests.get(self.api_url + endpoint)
        r.raise_for_status()
        
        s = list()
        if isinstance((resp := r.json()), dict):
            s.append(resp)
        elif isinstance(resp, list):
            s.extend(resp)
        else:
            raise TypeError(f'Invalid response : {resp}')
        return s

    def items(self,
            rarity: str | None = None,
            category: str | None = None,
            faction: str | None = None,
            query: str | None = None
        ) -> list[dict]:
        """Queries the CrossoutDB API for corresponding items

        Parameters
        ----------
        rarity : `str`, optional
            Filters by rarity name as listed in `rarities()`
        category : `str`, optional
            Filters by category name as listed in `categories()`
        faction : `str`, optional
            Filters by faction name as listed in `factions()`
        query : `str`, optional
            Filters items corresponding to the given query

        Returns
        -------
        `list[dict]`
            The list of items returned by the API
        """
        params = {}

        def addParameter(key: str, value: str | None, restrictedValues: set[str]) -> None:
            if value in restrictedValues:
                params[key] = value

        addParameter('rarity', rarity, {r['name'] for r in self.rarities()})
        addParameter('category', category, {c['name'] for c in self.categories()})
        addParameter('faction', faction, {f['name'] for f in self.factions()})

        if query:
            params['query'] = query

        return self.request('items?' + urllib.parse.urlencode(params))

    def item(self, item_id: int) -> dict:
        """Returns the item with the given ID.

        Parameters
        ----------
        item_id : `int`
            ID of the item to retrieve

        Returns
        -------
        `dict`
            A dict containing the item data

        Raises
        ------
        `ValueError`
            If the item with the given ID does not exist
        """
        data = self.request('item/' + str(item_id))
        assert (l := len(data)) <= 1
        if l == 0:
            raise ValueError('Item with ID '+ str(item_id) +' does not exist.')
        return data.pop()
    
    def rarities(self) -> list[dict]:
        """Queries the CrossoutDB API for all available rarities.

        Returns
        -------
        `list[dict]`
            The list of rarities
        """
        return self.request('rarities')
    
    def categories(self) -> list[dict]:
        """Queries the CrossoutDB API for all available item categories.

        Returns
        -------
        `list[dict]`
            The list of item categories
        """
        return self.request('categories')

    def factions(self) -> list[dict]:
        """Queries the CrossoutDB API for all available factions.

        Returns
        -------
        `list[dict]`
            The list of factions
        """
        return self.request('factions')
    
    def types(self) -> list[dict]:
        """Queries the CrossoutDB API for all available item types.

        Returns
        -------
        `list[dict]`
            The list of item types
        """
        return self.request('types')
    
    def recipe(self, item_id: int) -> dict:
        """Queries the CrossoutDB API for the given item's recipe.

        Parameters
        ----------
        item_id : `int`
            ID of the item's recipe to retrieve

        Returns
        -------
        `dict` 
            A dict containing the recipe data

        Raises
        ------
        `ValueError`
            If the recipe with the given ID does not exist
        """
        err = ValueError('Recipe with ID '+ str(item_id) +' does not exist.')

        # Empty JSON response
        if len(data := self.request('recipe/' + str(item_id))) <= 0:
            raise err
        
        data = data[0]["recipe"]
        
        # Recipe data with no ingredients
        if len(data["ingredients"]) <= 0:
            raise err
        
        return data