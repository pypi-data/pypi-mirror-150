from glob import glob
from multiprocessing import Pool, Manager, cpu_count
from os.path import dirname, exists, join
from statistics import median
from time import sleep
from typing import Dict, List, Optional, Union

import click
import isbnlib

from .ajum import Ajum
from .utils import create_path, list2chunks
from .utils import load_json, dump_json


@click.group()
@click.pass_context
@click.option('-c', '--config', type=click.File(), help='Path to user settings file.')
@click.option('-u', '--ua', type=click.File(), help='Path to "UA" strings file.')
@click.option('-v', '--verbose', count=True, help='Enable verbose mode.')
@click.version_option('0.8.0')
def cli(ctx, config: Optional[click.File] = None, ua: Optional[click.File] = None, verbose: int = 0) -> None:
    """
    Tools for interacting with the 'AJuM' database.
    """

    # Initialize context object
    ctx.ensure_object(dict)

    # Assign verbose mode
    ctx.obj['verbose'] = verbose

    # Get caching directory
    cache_dir = click.get_app_dir('ajum')
    ctx.obj['cache_dir'] = cache_dir

    # If config file was passed ..
    if config:
        # .. load user settings
        ctx.obj['config'] = load_json(config)

    # .. otherwise ..
    else:
        # .. use default configuration
        config_file = join(cache_dir, 'config.json')

        # If it exists ..
        if exists(config_file):
            # .. load it
            ctx.obj['config'] = load_json(config_file)

        # .. otherwise ..
        else:
            # .. use sensible defaults
            ctx.obj['config'] = {
                'headers': {
                    'From': 'your@email.com',
                    'User-Agent': 'we-love-ajum',
                },
                'timeout': 180.0,
                'wait': 10,
            }

            # .. create it ..
            with open(config_file, 'w') as file:
                dump_json(ctx.obj['config'], file)

    # Load UA strings
    # (1) Determine file containing user agents
    ua_file = ua or join(cache_dir, 'user-agents.txt')

    # If UA file was passed ..
    if ua:
        # .. load UA strings
        ctx.obj['ua'] = [string.strip() for string in ua.readlines()]

    # .. otherwise ..
    else:
        # .. see whether predefined UA strings ..
        ua_file = join(cache_dir, 'user-agents.txt')

        # .. are installed, in which case ..
        if exists(ua_file):
            # .. load them
            with open(ua_file, 'r') as file:
                ctx.obj['ua'] = [ua.strip() for ua in file.readlines()]


@cli.command()
@click.pass_context
@click.option('-p', '--parallel', default=32, help='Number of parallel downloads.')
@click.option('-n', '--number', type=int, help='Number of results pages to be scraped.')
def backup(ctx: click.Context, parallel: int = 32, number: Optional[int] = None) -> None:
    """
    Backs up remote database
    """

    # Initialize object
    ajum = init(ctx.obj)

    # Create data array
    slugs = []

    # Loop over results pages in chunks ..
    for chunk in list2chunks(range(number or ajum.max_page()), parallel):
        # If already cached ..
        if ajum.is_cached(chunk):
            # .. move on to next chunk
            continue

        # .. reporting back
        if ctx.obj['verbose'] > 0: click.echo('Fetching results pages "{}" ..'.format(', '.join([str(i + 1) for i in chunk])))

        # .. fetching their data
        for slug in ajum.get_slugs([{'tx_solr[page]': str(page + 1), 'tx_solr[sort]': 'datum_desc+desc'} for page in chunk]):
            # .. extracting review slugs
            slugs.append(slug)

    # Loop over results pages in chunks ..
    for chunk in list2chunks(slugs, parallel):
        # If already cached ..
        if ajum.is_cached(chunk):
            # .. move on to next chunk
            continue

        # .. reporting back
        if ctx.obj['verbose'] > 0: click.echo('Fetching review pages "{}" ..'.format(', '.join(chunk)))

        # .. fetching their data
        ajum.get_reviews(chunk)

        # .. wait for it
        sleep(ajum.wait)


@cli.command()
@click.pass_context
@click.argument('file', default='index.json', type=click.File('w'))
@click.option('-s', '--strict', is_flag=True, help='Whether to skip invalid ISBNs.')
@click.option('-f', '--full', is_flag=True, help='Whether to export full database.')
def export(ctx, file: click.File, strict: bool = False, full: bool = False) -> None:
    """
    Exports review data to FILE
    """

    def group_isbns(data: List[dict]) -> Dict[str, Dict[str, Union[list, str]]]:
        """
        Groups & sorts review data by ISBN

        :param data: list<dict> Collected review data

        :return: dict Grouped & sorted review data
        """

        # Create data array
        isbns = {}

        # Loop over reviews
        for item in data:
            # If no store for ISBN ..
            if item['ISBN'] not in isbns:
                # .. create it
                isbns[item['ISBN']] = []

            isbns[item['ISBN']].append(item if full else item['URL'])

        return isbns


    # Initialize object
    ajum = init(ctx.obj)

    # Group review data by ISBN
    isbns = group_isbns(ajum.load_db())

    # If 'strict' mode is enabled ..
    if strict:
        # .. use helper functions in order to ..
        # (1) .. determine validity of each ISBN
        def is_valid(isbn: str) -> bool:
            """
            Checks whether ISBN is valid

            :param isbn: str ISBN

            :return: bool Validity
            """

            # If ISBN is invalid ..
            if isbnlib.notisbn(isbn):
                # .. report back
                if ctx.obj['verbose'] > 0: click.echo('Skipping invalid ISBN "{}" ..'.format(isbn))

                # .. skip it
                return False

            return True


        # (2) .. format ISBNs properly
        def format_isbn(isbn: str) -> str:
            """
            Formats ISBN (if needed)

            :param isbn: str ISBN to be formatted (= hyphenated)

            :return: str (Formatted) ISBN
            """

            # See https://github.com/xlcnd/isbnlib/issues/86
            if isbnlib.mask(isbn):
                # Hyphenate ISBN
                isbn = isbnlib.mask(isbn)

                # Report back
                if ctx.obj['verbose'] > 0: click.echo('Adding review for "{}" ..'.format(isbn))

            return isbn


        isbns = {format_isbn(isbn): data for isbn, data in isbns.items() if is_valid(isbn)}

    # Report file creation
    if ctx.obj['verbose'] > 0: click.echo('Creating file {} ..'.format(file.name))

    # Create path (if needed)
    create_path(file.name)

    if full:
        # Create database file
        # (1) Sort data by ISBN
        # (2) Dump data to JSON file
        dump_json(dict(sorted(isbns.items())), file)

    else:
        # Create index file
        # (1) Sort data by ISBN
        # (2) Sort lists of review slugs
        # (3) Dump data to JSON file
        dump_json(dict(sorted({k: sorted(v) for k, v in isbns.items()}.items())), file)


@cli.command()
@click.pass_context
@click.argument('isbn')
def show(ctx, isbn: str) -> None:
    """
    Shows data for given ISBN
    """

    # Initialize object
    ajum = init(ctx.obj)

    # Load index
    index = load_json('{}/data/index.json'.format(dirname(__file__)))

    # Create data array
    reviews = []

    # If review slug(s) indexed ..
    if isbn in index:
        # .. load their review(s)
        reviews = ajum.get_reviews(index[isbn])

    # .. otherwise ..
    else:
        # .. query database
        reviews = ajum.query(isbn)

    # If review(s) available ..
    if reviews:
        # .. show results
        show_reviews(reviews)

    # .. otherwise ..
    else:
        # .. report back
        click.echo('Für die ISBN "{}" wurde keine Rezension gefunden!'.format(isbn))


@cli.command()
@click.pass_context
@click.option('-q', '--query', type=str, help='Search term.')
@click.option('-t', '--search-field', type=str, help='Search field type.')
@click.option('-r', '--rating', type=str, help='Rating.')
@click.option('-f', '--application', type=str, help='Field of application.')
@click.option('-m', '--media-type', type=str, help='Media type.')
@click.option('-t', '--topics', type=str, help='Topics.')
@click.option('-a', '--ages', type=str, help='Recommendable age range(s).')
@click.option('-y', '--year', type=str, help='Publishing year.')
def query(ctx, query, search_field, rating, application, media_type, topics, ages, year) -> None:
    """
    Queries remote database
    """

    # Initialize object
    ajum = init(ctx.obj)

    # Query database
    reviews = ajum.query(query, search_field, rating, application, media_type, topics, ages, year)

    # Show results
    show_reviews(reviews)


@cli.command()
@click.pass_context
def stats(ctx) -> None:
    """
    Shows statistics
    """

    # Initialize object
    ajum = init(ctx.obj)

    # Count cached reviews
    review_count = len(glob(join(ajum.cache_dir, 'reviews', '*.json')))

    # Report it
    click.echo('There are currently ..')
    click.echo('.. {} reviews in cache.'.format(review_count))

    # Load index
    index = load_json('{}/data/index.json'.format(dirname(__file__)))
    index_count = len(index.keys())
    review_count = sum([len(item) for item in index.values()])

    # Report indexed reviews
    click.echo('.. {} reviews indexed.'.format(review_count))
    click.echo('.. {} ISBNs indexed.'.format(index_count))

    # Report average & median reviews per ISBN
    click.echo('--')
    click.echo('Reviews per ISBN ..')
    click.echo('.. median of {}'.format(int(median(sorted([len(value) for value in index.values()])))))
    click.echo('.. averaging {:.2f}'.format(review_count / index_count))


@cli.command()
@click.pass_context
@click.option('-r', '--reset', is_flag=True, help='Whether to remove cached results pages.')
def clear(ctx, reset: bool = False) -> None:
    """
    Removes cached results files
    """

    # Initialize object
    ajum = init(ctx.obj)

    if ctx.obj['verbose'] > 0: click.echo('Flushing cache ..')

    # Flush cache
    ajum.clear_cache(reset)


def init(config: dict) -> Ajum:
    """
    Initializes 'Ajum' instance

    :param config: dict User settings

    :return: 'Ajum' Instance
    """

    # Initialize object & set data directory
    ajum = Ajum(config['cache_dir'])

    # Configure options
    if 'config' in config:
        for key, value in config['config'].items():
            setattr(ajum, key, value)

    # Set UA strings
    if 'ua' in config:
        ajum.user_agents = config['ua']

    return ajum


def pretty_print(data: Dict[str, Union[list, str]]) -> None:
    """
    Prints data record (beautifully)

    :param data: dict<str,list|str> Data record

    :return: None
    """

    for key, value in data.items():
        if isinstance(value, list):
            click.echo('{}:'.format(key))

            for item in value:
                click.echo('-> {}'.format(item))

        else:
            click.echo('{}: {}'.format(key, value))


def show_reviews(reviews: List[Dict[str, Dict[str, Union[list, str]]]]) -> None:
    """
    Shows review data
    """

    if not reviews:
        click.echo('Die Suche ergab leider keine Ergebnisse.')

    # Count reviews
    count = len(reviews)

    click.echo('Die Suche ergab {} Ergebnisse.'.format(count))

    # If confirmed ..
    if click.confirm('Ergebnisse anzeigen?', True):
        # .. loop over reviews ..
        for i, review in enumerate(reviews):
            # Make numbering human-readable
            i += 1

            # Let user know where we are
            click.echo('Eintrag {}/{}:'.format(str(i), count))

            # Print review data
            pretty_print(review)

            # Exit script upon last entry
            if i == count:
                click.echo('Es gibt keine weiteren Einträge.')

                # Goodbye!
                break

            # Always remember this: If told to ..
            if not click.confirm('Weiterlesen?', True):
                # .. stop!
                break
