import requests
from exceptions import RateLimitExceededError, BINLookupError

API_BASE = 'https://lookup.binlist.net/'

class BANK_Information():
    """Class to store information about the bank."""
    def __init__(self, name):
        self.name = name

class COUNTRY_Information():
    """Class to store information about the country."""
    def __init__(self, numeric, alpha2, name, emoji, currency, latitude, longitude):
        self.numeric = numeric
        self.alpha2 = alpha2
        self.name = name
        self.emoji = emoji
        self.currency = currency
        self.latitude = latitude
        self.longitude = longitude

class BIN_Information():
    """Class to store information about the BIN (Bank Identification Number)."""
    def __init__(self, bin, scheme, type, brand, prepaid, country_info, bank_info):
        self.bin = bin
        self.scheme = scheme
        self.type = type
        self.brand = brand
        self.prepaid = prepaid
        self.country = country_info
        self.bank = bank_info

class BIN_Lookup():
    """Class to perform BIN lookups and fetch information from the API."""
    def __init__(self):
        self.info = None

    def fetch(self, bin, proxy=None):
        """
        Fetch information for a given BIN.

        Args:
            bin (str): The BIN to look up.
            proxy (str, optional): Proxy URL for the request. Defaults to None.

        Returns:
            BIN_Information: An instance containing information about the BIN.

        Raises:
            RateLimitExceededError: If the rate limit is exceeded.
            BINLookupError: If an error occurs during the lookup.
        """
        if proxy:
            proxies = {
                'http': proxy,
                'https': proxy
            }
        else:
            proxies = None
        
        response = requests.get(API_BASE + str(bin), proxies=proxies)
        if response.status_code == 200:
            data = response.json()
            country_info = COUNTRY_Information(
                numeric=data.get('country', {}).get('numeric'),
                alpha2=data.get('country', {}).get('alpha2'),
                name=data.get('country', {}).get('name'),
                emoji=data.get('country', {}).get('emoji'),
                currency=data.get('country', {}).get('currency'),
                latitude=data.get('country', {}).get('latitude'),
                longitude=data.get('country', {}).get('longitude')
            )
            bank_info = BANK_Information(
                name=data.get('bank', {}).get('name')
            )
            self.info = BIN_Information(
                bin=data.get('number', {}).get('length'),
                scheme=data.get('scheme'),
                type=data.get('type'),
                brand=data.get('brand'),
                prepaid=data.get('prepaid'),
                country_info=country_info,
                bank_info=bank_info
            )
            return self.info
        elif response.status_code == 429:
            raise RateLimitExceededError(response.status_code)
        else:
            raise BINLookupError(bin, response.status_code)

    def fetch_json(self, bin, proxy=None):
        """
        Fetch raw JSON data for a given BIN.

        Args:
            bin (str): The BIN to look up.
            proxy (str, optional): Proxy URL for the request. Defaults to None.

        Returns:
            dict: Raw JSON data from the API.

        Raises:
            RateLimitExceededError: If the rate limit is exceeded.
            BINLookupError: If an error occurs during the lookup.
        """
        if proxy:
            proxies = {
                'http': proxy,
                'https': proxy
            }
        else:
            proxies = None
        
        response = requests.get(API_BASE + str(bin), proxies=proxies)
        if response.status_code == 200:
            data = response.json()
            return data
        elif response.status_code == 429:
            raise RateLimitExceededError(response.status_code)
        else:
            raise BINLookupError(bin, response.status_code)