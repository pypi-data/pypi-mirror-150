import asyncio
import json
import os

from copy import deepcopy
from glob import glob
from random import choice, randint
from re import split
from time import sleep
from typing import Dict, List, Optional, Union
from urllib.parse import parse_qs, unquote, urlparse

from aiofiles import open as async_open
from aiohttp import ClientSession, ClientTimeout, request
from bs4 import BeautifulSoup as bs
from bs4.element import Tag

from .utils import create_path, data2hash, flatten, get_logger


class Ajum():
    """
    Tools for interacting with the AJuM database
    """

    # Request headers
    headers: dict = {'User-Agent': 'we-love-ajum'}


    # Maximum number of open files
    #
    # Check current limit with `ulimit -n`
    #
    # For more information,
    # see https://github.com/Tinche/aiofiles/issues/83#issuecomment-761208062
    file_limit: int = 1024


    # Request timeout
    timeout: float = 180.0


    # UA strings
    # For sample data, see https://developers.whatismybrowser.com/useragents/database/#sample-data
    user_agents: list = [
        'Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00',
        'Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 635; BOOST) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.87 Safari/537.36 Vivaldi/1.0.270.16',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_9_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B411 Safari/600.1.4',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 4.4.2; en-gb; SAMSUNG SM-T330 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Safari/537.36',
        'SAMSUNG-SGH-E250i/E250iJBKA1 Profile/MIDP-2.0 Configuration/CLDC-1.1 UP.Browser/6.2.3.3.c.1.101 (GUI) MMP/2.0',
    ]


    # Waiting time after each request
    wait: float = 5.0


    # CONSTRUCTOR

    def __init__(self, cache_dir: str = '.db') -> None:
        """
        Creates 'Ajum' instance

        :param cache_dir: dict Database directory
        :param file_limit: int Limit of open files

        :return: None
        """

        # Set data directory
        self.cache_dir = cache_dir

        # Enable logging
        # (1) Create path (if needed)
        log_dir = os.path.join(self.cache_dir, 'logs')
        create_path(log_dir)

        # (2) Initialize logger
        self.logger = get_logger(log_dir, 'ajum.log')


    # FiLE I/O

    async def load_html(self, html_file: str, lock: asyncio.locks.Semaphore) -> str:
        """
        Loads data from HTML

        :param html_file: str Path to HTML file
        :param lock: asyncio.locks.Semaphore Lock preventing too many open files

        :return: str HTML data
        """

        # Respect file limit when ..
        async with lock:
            # .. loading data
            async with async_open(html_file, 'r') as file:
                return await file.read()


    async def dump_html(self, data: str, html_file: str, lock: asyncio.locks.Semaphore) -> None:
        """
        Dumps HTML data to file

        :param data: str Data
        :param html_file: str Path to HTML file
        :param lock: asyncio.locks.Semaphore Lock preventing too many open files

        :return: None
        """

        # Create path (if needed)
        create_path(html_file)

        # Respect file limit when ..
        async with lock:
            # .. storing data
            async with async_open(html_file, 'w') as file:
                await file.write(data)


    async def load_json(self, json_file: str, lock: asyncio.locks.Semaphore) -> Union[dict, list]:
        """
        Loads data from JSON

        :param json_file: str Path to JSON file
        :param lock: asyncio.locks.Semaphore Lock preventing too many open files

        :return: dict|list Data
        :raises: Exception Decoding error
        """

        try:
            # Respect file limit when ..
            async with lock:
                # .. loading data
                async with async_open(json_file, 'r') as file:
                    return json.loads(await file.read())

        # If something goes wrong ..
        except json.decoder.JSONDecodeError as e:
            # .. report back
            raise Exception('Loading JSON file "{}" failed: "{}"'.format(json_file, e))


    async def dump_json(self, data: Union[dict, list], json_file: str, lock: asyncio.locks.Semaphore) -> None:
        """
        Dumps JSON data to file

        :param data: dict|list Data
        :param json_file: str Path to JSON file
        :param lock: asyncio.locks.Semaphore Lock preventing too many open files

        :return: None
        """

        # Create path (if needed)
        create_path(json_file)

        # Respect file limit when ..
        async with lock:
            # .. storing data
            async with async_open(json_file, 'w') as file:
                await file.write(json.dumps(data, ensure_ascii=False, indent=4))


    # GENERAL

    async def fetch(self, session: ClientSession, base_url: str = 'https://www.ajum.de/rezension-suche/', params: Optional[Dict[str, Dict[str, Union[list, str]]]] = None) -> str:
        """
        Fetches HTML content

        :param session: aiohttp.client.ClientSession Session object
        :param base_url: str Base URL
        :param params: dict<str,dict<str,list|str>> Query parameters

        :return: str HTML content
        """

        # Determine request headers & randomize UA string
        headers = deepcopy(self.headers)
        headers['User-Agent'] = choice(self.user_agents)

        # Wait some time before ..
        await asyncio.sleep(randint(self.wait, self.wait + 30))

        # .. attempting to ..
        try:
            # .. make API call
            timeout = ClientTimeout(total=self.timeout)

            async with session.request('GET', base_url, params=params, headers=headers, timeout=timeout) as response:
                # Store debugging information
                self.logger.info('Status: {}, URL: {}'.format(response.status, response.url))

                # Provide source code
                return await response.text('utf-8')

        # .. while handling timeouts ..
        except asyncio.exceptions.TimeoutError as e:
            # .. gracefully
            self.logger.info('Request timed out: "{}"'.format(e))

        # .. otherwise ..
        except Exception as e:
            # .. report back
            self.logger.info('Request failed: "{}"'.format(e))

        # If something goes wrong, get some sleep over it
        sleep(self.wait)


    def hash2file(self, path: str, data: Union[dict, str], extension: str) -> str:
        """
        Builds path to data file

        :param path: str Subpath ('results' or 'reviews')
        :param data: dict|str
        :param extension: str File extension

        :return: str Path to data file
        """

        # Build data path
        data_path = '{}/{}/{}.{}'.format(self.cache_dir, path, data2hash(data), extension)

        # Create directory (if needed)
        create_path(data_path)

        return data_path


    # RESULTS PAGES

    async def fetch_results(self, session: ClientSession, params: Dict[str, Dict[str, Union[list, str]]], lock: asyncio.locks.Semaphore) -> List[str]:
        """
        Fetches results page & caches slugs of its reviews

        :param session: aiohttp.client.ClientSession Session object
        :param params: dict<str,dict<str,list|str>> Query parameters
        :param lock: asyncio.locks.Semaphore Lock preventing too many open files

        :return: list<str> Review slugs
        """

        # Create data array
        data = []

        # Determine JSON file
        json_file = self.hash2file('results', params, 'json')

        try:
            # If cached ..
            if os.path.exists(json_file):
                # .. load review slugs
                data = await self.load_json(json_file, lock)

            # .. otherwise ..
            else:
                # .. determine HTML file
                html_file = self.hash2file('results', params, 'html')

                # If cached ..
                if os.path.exists(html_file):
                    # .. load HTML from file
                    html = await self.load_html(html_file, lock)

                # .. otherwise ..
                else:
                    # .. send request
                    html = await self.fetch(session, params=params)

                    # .. store response text
                    await self.dump_html(html, html_file, lock)

                # Attempt to ..
                try:
                    # .. extract review slugs
                    data = self.extract_slugs(html)

                    # .. store them
                    await self.dump_json(data, json_file, lock)

                # .. but if no reviews slugs are found ..
                except:
                    # .. remove stored HTML page
                    os.remove(html_file)

                    # .. raise again, man!
                    raise

        # .. otherwise ..
        except Exception as e:
            # .. report back
            raise
            self.logger.error('Results page for query "{}" failed: "{}"'.format(params, e))

        return data


    def extract_slugs(self, html: str) -> List[str]:
        """
        Extracts review slugs from single results page

        :param html: str HTML content

        :return: list<str> Extracted review slugs
        :raises: Exception Results page is empty
        """

        def extract_slug(card: Tag) -> str:
            """
            Extracts review slug from given 'card' element

            :param card: bs4.element.Tag Selected 'card' element

            :return: str Review slug
            """

            # Select first link & fetch its URL
            url = card.find('a')['href']

            # Extract review slug
            return os.path.split(url)[-1]


        # Fetch 'card' element
        cards = bs(html, 'lxml').find_all('div', {'class': 'card'})

        # If results page is empty ..
        if not cards:
            # .. throw exception
            raise Exception('Results page has no results!')

        # Extract review slugs
        return list((extract_slug(card) for card in cards))


    def get_slugs(self, params_list: List[dict]) -> List[str]:
        """
        Fetches multiple results pages at once & caches slugs of their reviews

        :param params_list: list<dict<str,list|str>> List of query parameters

        :return: list<str> Review slugs
        """

        async def helper(params_list: List[dict]) -> List[str]:
            """
            Fetches multiple results pages (async helper function)

            :param params_list: list<dict<str,list|str>> List of query parameters

            :return: list<str> Review slugs
            """

            # Impose file opening limit
            lock = asyncio.Semaphore(self.file_limit)

            async with ClientSession() as session:
                return await asyncio.gather(*[self.fetch_results(session, params, lock) for params in params_list])


        return flatten(asyncio.run(helper(params_list)))


    # REVIEW PAGE

    async def fetch_review(self, session: ClientSession, slug: str, lock: asyncio.locks.Semaphore) -> dict:
        """
        Fetches single review & caches its data

        :param session: aiohttp.client.ClientSession Session object
        :param slug: str Review slug
        :param lock: asyncio.locks.Semaphore Lock preventing too many open files

        :return: dict Review data
        """

        # Create data array
        data = {}

        # Determine JSON file
        json_file = self.hash2file('reviews', slug, 'json')

        try:
            # If cached ..
            if os.path.exists(json_file):
                # .. load review slugs
                data = await self.load_json(json_file, lock)

            # .. otherwise ..
            else:
                # .. determine HTML file
                html_file = self.hash2file('reviews', slug, 'html')

                # If cached ..
                if os.path.exists(html_file):
                    # .. load HTML from file
                    html = await self.load_html(html_file, lock)

                # .. otherwise ..
                else:
                    # .. send request
                    html = await self.fetch(session, 'https://www.ajum.de/rezension/' + slug)

                    # .. store response text
                    await self.dump_html(html, html_file, lock)

                # Get review slug
                data = {'URL': slug}

                # Attempt to ..
                try:
                    # .. extract review data
                    data.update(self.extract_review(html))

                    # .. store it
                    await self.dump_json(data, json_file, lock)

                # .. but if no review data present ..
                except:
                    # .. remove stored HTML page
                    os.remove(html_file)

                    # .. raise again, man!
                    raise

        # .. otherwise ..
        except Exception as e:
            # .. return empty result
            self.logger.error('Review page "{}" failed: "{}"'.format(slug, e))

        return data


    def extract_review(self, html: str) -> dict:
        """
        Extracts review data from single review page

        :param html: str HTML content

        :return: dict Extracted review data
        """

        def process(tag: Tag) -> Union[List[str], str]:
            """
            Processes tags representing review 'details' value

            :param tag: bs4.element.Tag Selected 'card' element

            :return: list<str>|str Processed output
            """

            # Strip text
            text = tag.text.strip()

            # If text equals 'empty' content ('–') ..
            if text in ['-', '\u2013']:
                # .. return empty string
                return ''

            # Check for link elements
            links = tag.find_all('a', {'class': 'btn-searchable'})

            # If no more than one available ..
            if len(links) < 2:
                # .. just return text
                return text

            return [link.text.strip() for link in links]


        # Create data array
        data = {}

        # Make HTML soup - mhh, soup!
        soup = bs(html.replace('<br>', '\n'), 'lxml')

        # Fetch book title
        data['Titel'] = soup.find('h1').text.strip()

        # Extract publishing date
        data['Datum'] = soup.find('div', {'class': 'author'}).find_all('strong')[-1].text

        # Extract bibliographic information
        # (1) Select 'details' element
        details = soup.find('section', {'class': 'details'})

        # (2) Process keys & values
        keys = [key.text.strip() for key in details.find_all('dt')]
        values = [process(value) for value in details.find_all('dd')]

        # (3) Merge & store them
        data.update(dict(zip(keys, values)))

        # Extract teaser, description & tags
        for card in soup.find_all('section', {'class': 'highlight-area'}):
            # Skip 'details' element
            if card == details:
                continue

            # Get title
            title = card.find('h3').text.strip()

            # Check for link elements
            links = card.find_all('a', {'class': 'btn-searchable'})

            # If links present ..
            if links:
                # .. store them
                data[title] = [link.text.strip() for link in links]

            # .. otherwise ..
            else:
                # .. split newlines & store text
                data[title] = [text.strip() for text in split('\n', card.find('p').text)]

        return data


    def get_reviews(self, slugs: Union[List[str], str]) -> List[dict]:
        """
        Fetches multiple reviews at once & caches their data

        :param slugs: list<str>|str Review slug(s)

        :return: list<dict> Review data
        """

        async def helper(slugs: List[str]) -> List[dict]:
            """
            Fetches multiple reviews (async helper function)

            :param slugs: list<str> Review slugs

            :return: list<dict> Review data
            """

            # Impose file opening limit
            lock = asyncio.Semaphore(self.file_limit)

            # Gather results
            async with ClientSession() as session:
                return await asyncio.gather(*[self.fetch_review(session, slug, lock) for slug in slugs])

        # Convert string to list (if needed)
        if isinstance(slugs, str):
            slugs = [slugs]

        return asyncio.run(helper(slugs))


    # HELPERS

    def max_page(self) -> int:
        """
        Fetches index of last results page

        :return: int Index
        """

        async def helper() -> str:
            """
            Fetches HTML of first results page (async helper function)

            :return: str Source code
            """

            # Fetch first results page ..
            async with request('GET', 'https://www.ajum.de/rezension-suche/', headers=self.headers) as response:
                # .. returning its source
                return await response.text('utf-8')


        # Make HTML soup - mhh, soup!
        soup = bs(asyncio.run(helper()), 'lxml')

        # Select pagination links
        links = soup.find('ul', {'class': 'pagination'}).find_all('a')

        # Determine index of last results page
        # (1) Select last pagination link
        # (2) Build URL through decoding its 'href' attribute
        # (3) Parse it & select its query string component
        # (4) Grab value of 'page' key & return as integer
        return int(parse_qs(urlparse(unquote(links[-1]['href'])).query)['tx_solr[page]'][0])


    # LOCAL DATABASE

    def load_db(self) -> List[dict]:
        """
        Loads review data from database (async helper function)

        :return: list<dict> Collected review data
        """

        async def helper() -> dict:
            """
            Loads review data from database (async helper function)

            :return: dict Review data
            """

            # Impose file opening limit
            lock = asyncio.Semaphore(self.file_limit)

            # Gather results
            return await asyncio.gather(*[self.load_json(file, lock) for file in glob(self.cache_dir + '/reviews/*.json')])


        return asyncio.run(helper())


    def clear_cache(self, reset: bool = False) -> None:
        """
        Removes cached index files

        :param reset: bool Whether to clear cached results pages

        :return: None
        """

        results = glob(self.cache_dir + '/results/*')
        reviews = glob(self.cache_dir + '/reviews/*')

        # Loop over all files
        for file in results + reviews:
            # If empty ..
            if os.path.getsize(file) == 0:
                # .. delete it
                os.remove(file)

        # If selected ..
        if reset:
            # .. loop over cached results pages ..
            for file in results:
                # .. deleting each one
                os.remove(file)


    def is_cached(self, data: Union[dict, str, List[dict], List[str]]) -> bool:
        """
        Checks whether given data exists in cache

        :param data: dict|str|list<dict>|list<str> Results page(s) OR review slug(s)

        :return: bool Cache status
        """

        if isinstance(data, list):
            for item in data:
                if not self.is_cached(item):
                    return False

            return True

        files = []

        # Check whether data represents ..
        if isinstance(data, dict):
            # (1) .. results page
            files = [
                self.hash2file('results', data, 'json'),
                self.hash2file('results', data, 'html'),
            ]

        if isinstance(data, str):
            # (2) .. review slug
            files = [
                self.hash2file('reviews', data, 'json'),
                self.hash2file('reviews', data, 'html')
            ]

        if not files:
            return False

        return all(os.path.exists(file) for file in files)


    def query(self,
        query: str = '*',
        search_field: Optional[str] = None,
        rating: Optional[Union[List[str], str]] = None,
        application: Optional[Union[List[str], str]] = None,
        media_type: Optional[Union[List[str], str]] = None,
        topics: Optional[Union[List[str], str]] = None,
        ages: Optional[Union[List[str], str]] = None,
        year: Optional[Union[List[str], str]] = None
    ) -> Dict[str, Dict[str, Union[list, str]]]:
        """
        Queries remote database for matching reviews

        :param query: str Search term ('Suchbegriff')
        :param title: str Book title ('Titel')
        :param author: str Author ('Autor:in')
        :param illustrator: str Illustrator ('Illustrator:in')
        :param translator: str Translator ('Übersetzer:in')
        :param rating: list<str>|str Rating ('Bewertung')
        :param application: list<str>|str Field of application ('Einsatzmöglichkeit')
        :param media_type: list<str>|str Media type ('Gattung/Medienart')
        :param topics: list<str>|str Topics ('Themen')
        :param ages: list<str>|str Recommendable age range(s) ('Alter')
        :param year: list<str>|str Publishing year ('Erscheinungsjahr')

        :return: dict<str,dict<str,list|str>>
        """

        async def helper(params: Dict[str, Dict[str, Union[list, str]]]) -> str:
            """
            Connects to database API (async helper function)

            :param params: dict<str,dict<str,list|str>> Query parameters

            :return: str HTML content
            """

            async with ClientSession() as session:
                return await self.fetch(session, params=params)


        def build_filter(data: Union[List[str], str], filters: list) -> list:
            """
            Validates query parameter for TYPO3 'Solr' search

            :param data: list<str>|str Filter value(s)
            :param filters: list Valid filters

            :return: list Validated filter values
            """

            if isinstance(data, list):
                return sorted([item for item in data if item in filters])

            if data in filters:
                return [data]

            return []


        # Prepare filters
        # (1) Rating ('Bewertung')
        rating = ['bewertung:' + value for value in build_filter(rating, [
            '0',  # 'nicht empfehlenswert'
            '1',  # 'eingeschränkt empfehlenswert'
            '2',  # 'empfehlenswert'
            '3',  # 'sehr empfehlenswert',
        ])]
            # TODO: Use colon!
            # TODO: Multiple at once!

        # (2) Field of application ('Einsatzmöglichkeit')
        application = ['application:' + value for value in build_filter(application, [
            'Bücherei',
            'Fachliteratur',
            'Klassenlektüre',
            'Vorlesen',
        ])]

        # (3) Media type ('Gattung/Medienart')
        media_type = ['genres:' + value for value in build_filter(media_type, [
            'Audio',
            'Bilderbuch',
            'Biografie',
            'Buch (gebunden)',
            'Comic',
            'Digitale Medien',
            'Dystopie',
            'eBook',
            'Erstlesebuch',
            'Erzählung/Roman',
            'Fantastik',
            'Film',
            'Krimi',
            'Lyrik',
            'Märchen/Fabel/Sage',
            'Sachliteratur',
            'Science Fiction',
            'Taschenbuch',
        ])]

        # (4) Topics ('Themen')
        topics = ['topics:' + value for value in build_filter(topics, [
            'Abenteuer',
            'Adoleszenz',
            'Angst',
            'Arbeitswelt',
            'Außenseiter',
            'Basteln/Anleiten',
            'Behinderung',
            'Diversität',
            'Emanzipation',
            'Essen',
            'Familie',
            'Feste',
            'Flucht',
            'Forschen',
            'Freundschaft',
            'Frieden',
            'Gefühle',
            'Gender/Geschlecht',
            'Geografie',
            'Gewalt',
            'Historisches',
            'Intertextualität',
            'Kindheit',
            'Komik/Humor',
            'Krankheit',
            'Krieg',
            'Kulturen',
            'Kunst',
            'Lernen',
            'Liebe',
            'Mehrsprachigkeit',
            'Musik',
            'Mut',
            'Nationalsozialismus',
            'Natur',
            'Naturwissenschaft',
            'Philosophie',
            'Politik',
            'Rassismus',
            'Rechtsextremismus',
            'Reisen',
            'Religion',
            'Schule',
            'Sexualität',
            'Spannung',
            'spielen',
            'Sport',
            'Sprachspiel',
            'Streit/Konflikt',
            'Sucht',
            'Technik',
            'Theater',
            'Tiere',
            'Tod/Sterben',
            'Typografische Gestaltung',
            'Umweltschutz/Klima',
            'Ungleichheit',
            'Zukunft',
        ])]

        # (5) Age ranges ('Alter')
        ages = ['ages:' + value for value in build_filter(ages, [
            '0-3',
            '4-5',
            '6-7',
            '8-9',
            '10-11',
            '12-13',
            '14-15',
            '16-17',
            'ab 18',
        ])]

        # (6) Publishing year ('Erscheinungsjahr')
        # TODO: Use range
        year = ['year:' + value for value in build_filter(year, [
            '0002',
            '0017',
            '0020',
            '0200',
            '0201',
            '0206',
            '0207',
            '0208',
            '0209',
            '0213',
            '0214',
            '1012',
            '1015',
            '1017',
            '1912',
            '1914',
            '1919',
            '1970',
            '1974',
            '1976',
            '1978',
            '1982',
            '1983',
            '1984',
            '1988',
            '1989',
            '1990',
            '1991',
            '1992',
            '1993',
            '1994',
            '1995',
            '1996',
            '1997',
            '1998',
            '1999',
            '2000',
            '2001',
            '2002',
            '2003',
            '2004',
            '2005',
            '2006',
            '2007',
            '2008',
            '2009',
            '2010',
            '2011',
            '2012',
            '2013',
            '2014',
            '2015',
            '2016',
            '2017',
            '2018',
            '2019',
            '2020',
            '2021',
            '2022',
            '2026',
            '2105',
            '2106',
            '2121',
            '2914',
            '2917',
        ])]

        # Build query parameters using ..
        # (1) .. filters
        filters = flatten([rating, application, media_type, topics, ages, year])
        params = {'tx_solr[filter][{}]'.format(i): data for i, data in enumerate(filters)}

        # (2) .. search field
        if search_field in [
            'titel',        # 'Titel'
            'author',       # 'Autor*in'
            'illustrator',  # 'Illustrator*in'
            'translator',   # 'Übersetzer*in'
        ]:
            params['tx_solr[searchfield]'] = search_field

        # (3) .. search term
        params['tx_solr[q]'] = query

        # Fetch results page
        html = asyncio.run(helper(params))

        # Extract review slugs
        slugs = self.extract_slugs(html)

        # Fetch review data
        return self.get_reviews(slugs)
