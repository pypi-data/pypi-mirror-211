import aiohttp, asyncio, requests
from econuker.Exceptions import Forbidden, Unauthorized, NotFound, InternalServerError, RateLimited, EconukerException, InvalidAuthToken


async def _handle_error(response):
    """
    Handles the error responses from API requests.

    Args:
        response (aiohttp.ClientResponse): The response object from the API request.

    Raises:
        Forbidden: If the response status code is 403.
        Unauthorized: If the response status code is 401.
        NotFound: If the response status code is 404.
        InternalServerError: If the response status code is 500.
        RateLimited: If the response status code is 429.
        EconukerException: If the response status code does not match any known error codes.
    """
    if response.status == 403:
        raise Forbidden(f"{await response.text()}")
    elif response.status == 401:
        raise Unauthorized(f"{await response.text()}")
    elif response.status == 404:
        raise NotFound(f"{await response.text()}")
    elif response.status == 500:
        raise InternalServerError(f"{await response.text()}")
    elif response.status == 429:
        raise RateLimited(f"{await response.text()}")
    elif 200 <= response.status < 300:
        return False
    else:
        raise EconukerException(f"{await response.text()}")

class Owner:
    """
    Owner object.

    Attributes:
        _raw (str): Raw owner data.
        name (str): Owner name.
        id (str): Owner ID.
        nick (str, None): Owner nickname.
        profile (str, None): Owner profile.
    """

    def __init__(self, data):
        self._raw: str = data
        self.name = data["name"]
        self.id = data["id"]
        self.nick = data.get("nick")
        self.profile = data.get("profile")

class ItemPrice:
    """
    ItemPrice object.

    Attributes:
        _raw (dict): Raw item price data, excluding worth.
        _price_parts (str): Raw item price data split.
        sell (str): The sell amount.
        buy (str): The buy amount.
        worth (str): The worth amount.
    """

    def __init__(self, price):
        self._raw: dict = price
        self._price_parts: list = price.split("|")
        self.sell: str = self._price_parts[0].strip()
        self.buy: str = self._price_parts[1].strip()
        self.worth: str = None

class Token:
    """
    Represents an authentication token.

    Args:
        authtoken (str): The authentication token.
        auth_level (str): The authentication level.
        raw_data (dict): The raw data associated with the token.

    Attributes:
        authtoken (str): The authentication token.
        authlevel (str): The authentication level.
        _raw (dict): The raw API return associated with the token.
    """

    def __init__(self, authtoken, auth_level, raw_data):
        self.authtoken: str = authtoken
        self.authlevel: str = auth_level
        self._raw: dict = raw_data

class AsyncClient:
    """
    Base AsyncClient class for interacting with the EcoNuker API.

    WARNING: Until June 1, 2023, the Main API cannot be used.

    Args:
        auth_token (str, optional): The authentication token. Can be None. Must be valid. Defaults to None.
        
        beta (bool, optional): Whether or not to use the BETA API. Defaults to False.
    """

    def __init__(self, auth_token: str = None, beta: bool = False):
        self.auth_token: str = auth_token
        self.base_url: str = "https://beta.econuker.xyz/api" if beta else "https://econuker.xyz/api"
        self.auth_level: str = None

        if not beta:
            raise EconukerException("Main API is not available at this moment.")

        def __check_verify(self) -> Token:
            """
            Verifies an authentication token.

            Args:
                auth_token (str): The authentication token to verify.

            Returns:
                Token: A Token object if the token is valid, False otherwise.
            """
            auth_token = self.auth_token
            url = self.base_url + f"/auth/verify/{auth_token}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data["token"]
                self.auth_level = data["authlevel"]
                return Token(self.auth_token, self.auth_level, data)
            elif response.status_code == 404:
                return False
            else:
                _handle_error(response)
    
        self.__check_verify = lambda: __check_verify(self)

        if self.auth_token is not None:
            token = self.__check_verify()
            if token is False:
                raise InvalidAuthToken("Invalid auth_token provided.")
            else:
                self.auth_level = token.authlevel


    async def ping(self) -> bool:
        """
        Checks if the API is online using the /ping route.
        
        Returns:
            bool: Whether the API is online or not.
        """
        url = self.base_url + "/ping"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return True
                else:
                    return False

    class StatusData:
        """
        StatusData object.

        Args:
            data (dict): Data containing the route information.

        Attributes:
            name (str): The name of the route.
            status (str): The status of the route.
            servers (int): The number of servers associated with the route.
            latency (float): The latency of the route.

        """
        def __init__(self, data):
            self.name:str = data["name"]
            self.status:str = data["status"]
            self.servers:int = data["servers"]
            self.latency:float = data["latency"]

    async def status(self) -> StatusData:
        """
        Retrieves the status of the EcoNuker bot (or beta depending if beta=True or False)

        Returns:
            StatusData: An object containing the status information of the EcoNuker bot.
        """
        url = self.base_url + "/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return self.StatusData(data)
                else:
                    await _handle_error(response)

    async def verify(self, auth_token) -> Token:
        """
        Verifies an authentication token.

        Args:
            auth_token (str): The authentication token to verify.

        Returns:
            Token: A Token object if the token is valid, False otherwise.
        """
        url = self.base_url + f"/auth/verify/{auth_token}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return Token(data)
                elif response.status == 404:
                    return False
                else:
                    await _handle_error(response)

    class ServersResult:
        """
        ServersResult object.

        Attributes:
            _raw (dict): Raw API JSON data.
            count (int): Server count.
            server_ids (list): List of server IDs.
        """

    class ServerResult:
        """
        ServerResult object.

        Attributes:
            _raw (dict): Raw API JSON data.
            name (str): Server name.
            id (str): Server ID.
            owner (Owner): Owner object.
            url (str, None): The vanity URL of the server, if it exists.
            verified (bool): Indicates whether the server is verified.
            created_at (int): Epoch timestamp.
            timezone (str): The raw timezone of the server.
            slug (str): The server's slug.
            about (str, None): The server's "about me" information.
        """

        def __init__(self, data):
            self._raw: dict = data
            self.id: str = data["id"]
            self.name: str = data["name"]
            self.owner: Owner = Owner(data["owner"])
            self.url: str = data["vanity_url"]
            self.verified: bool = data["verified"]
            self.created_at: int = data["created_at"]
            self.timezone: str = data["timezone"]
            self.slug: str = data["slug"]
            self.about: str = data["about"]

    async def fetch_servers(self) -> ServersResult:
        """
        Fetches a list of all servers.

        Returns:
            ServersResult
        """
        url = self.base_url + "/servers"
        headers = {"authorization": self.auth_token} if self.auth_token else {}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return self.ServersResult(data)
                else:
                    await _handle_error(response)
    
    async def fetch_server(self, id: str) -> ServerResult:
        """
        Fetches a single server that the bot is in.

        Requires a trusted authlevel token.

        Returns:
            ServerResult

        Raises:
            econuker.Exceptions.Forbidden - Insufficient authorization level to fetch server details.
        """
        if self.auth_level and self.auth_level.lower() not in ["trusted", "admin"]:
            raise Forbidden("Insufficient authorization level to fetch server details.")
        url = self.base_url + f"/server/{id}"
        headers = {"authorization": self.auth_token} if self.auth_token else {}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return self.ServerResult(data)
                else:
                    await _handle_error(response)

    class ItemsResult:
        """
        ItemsResult object.

        Attributes:
            _raw (dict): Raw item list.
        """

        def __init__(self, data):
            self._raw: dict = data

    class ItemResult:
        """
        ItemResult object.

        Attributes:
            _raw (dict): Full raw item data from the API.
            _data (list): Raw item data from the API.
            id (str): The item's ID.
            name (str): The item's name.
            rarity (str): The item's rarity.
            description (str): The item's description.
            desc (str): An alias for the description.
            aliases (list): A list of all item aliases.
            _extradata (str): The extradata of the item.
            price (ItemPrice): Price data of the item.
        """

        def __init__(self, data):
            self._raw: dict = data
            self._data: list = data.get(list(data.keys())[0])
            self.id: str = list(data.keys())[0]
            self.name: str = self._data[0]
            self.rarity: str = self._data[1]
            self.description: str = self._data[2]
            self.desc: str = self._data[2]
            self.aliases: list = self._data[3]
            self._extradata: str = self._data[4]
            self.price: ItemPrice = ItemPrice(self._data[5])
            self.price.worth: str = self._data[6]

    async def fetch_items(self, hidden: bool = True) -> ItemsResult:
        """
        Fetches all items.

        Args:
            hidden (bool): Whether to hide hidden items or not when using an admin level token. Defaults to True.

        Raises:
            econuker.Exceptions.Forbidden: If there is insufficient token authentication level to fetch hidden items.
        """
        if not hidden:
            if not self.auth_level == 'admin':
                raise Forbidden("You tried to see hidden items without an admin level token.")

        url = self.base_url + "/items"
        if not hidden:
            headers = {"authorization": self.auth_token} if self.auth_token else {}
        else:
            headers = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return self.ItemsResult(data)
                else:
                    await _handle_error(response)

    async def fetch_item(self, id: int | str = None, name: str = None) -> ItemResult:
        """
        Fetch an item with either an ID or a name. Must use one, not neither or both.

        Args:
            id (str|int): The ID of the item.
            name (str): The name of the item.

        Returns:
            ItemResult: The fetched item result.

        Raises:
            econuker.Exceptions.Forbidden: If there is insufficient token authentication level to fetch a hidden item.
        """
        if id is None and name is None:
            raise ValueError("Either 'id' or 'name' must be provided.")
        elif id is not None and name is not None:
            raise ValueError("Only one of 'id' or 'name' should be provided, not both.")

        url = self.base_url + "/item"
        params = {}
        if id is not None:
            params["id"] = id
        if name is not None:
            params["name"] = name

        headers = {"authorization": self.auth_token} if self.auth_token else {}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return self.ItemResult(data)
                else:
                    await _handle_error(response)