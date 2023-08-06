# we-love-ajum
[![Build](https://ci.codeberg.org/api/badges/S1SYPHOS/we-love-ajum/status.svg)](https://codeberg.org/S1SYPHOS/we-love-ajum/issues)

This small library is a Python wrapper for [ajum.de](https://www.ajum.de/rezension-suche), querying the book review database of the german working group for children's and youth literature and media ("Arbeitsgemeinschaft Jugendliteratur und Medien" or "AJuM"), which is part of the german Education and Science Worker's Union ("Gewerkschaft Erziehung und Wissenschaft" or "GEW").

We deem their work to be invaluable for kindergartens, (pre)schools, universities and other educational institutions. We are thankful for AJuM's commitment and want to give something back by spreading the word and provide an easy way to interact with their review database.

**Note:** Since we DO NOT UNDER ANY CIRCUMSTANCES want to disrupt their services, `asyncio.sleep()` is called after each API request.

The included `ajum/data/index.json` file contains URL slugs for each ISBN. It was created using `--strict` mode, skipping invalid ISBNs - currently totalling 46203 (valid) ISBNs with 87939 reviews (averaging 1.90 reviews per ISBN).


## Getting started

Simply install all dependencies inside a virtual environment to get started:

```bash
# Set up & activate virtualenv
virtualenv -p python3 venv

# shellcheck disable=SC1091
source venv/bin/activate

# Install dependencies, either ..
# (1) .. from PyPi (stable)
python -m pip install ajum

# (2) .. from repository (dev)
python -m pip install --editable .
```

From there, it's easy to roll out your own script:

```python
from ajum import Ajum

# Initialize object
ajum = Ajum()

# Fetch reviews from first page
slugs = ajum.get_slugs():

# Display their data:
print(ajum.get_reviews(slugs))
```

For more examples, have a look at `src/cli.py` and `src/ajum.py` to get you started - feedback appreciated, as always!


## Usage

The following commands are available:

```text
$ ajum --help
Usage: ajum [OPTIONS] COMMAND [ARGS]...

  Tools for interacting with the 'AJuM' database.

Options:
  -c, --config PATH  Path to user settings file.
  -u, --ua PATH      Path to "UA" strings file.
  -v, --verbose      Enable verbose mode.
  --version          Show the version and exit.
  --help             Show this message and exit.

Commands:
  backup  Backs up remote database
  clear   Removes cached results files
  export  Exports review data to FILE
  query   Queries remote database
  show    Shows data for given ISBN
  stats   Shows statistics
```


## Commands

### `backup`

.. remote database:

```text
$ ajum backup --help
Usage: ajum backup [OPTIONS]

  Backs up remote database

Options:
  -p, --parallel INTEGER  Number of parallel downloads.
  -n, --number INTEGER    Number of results pages to be scraped.
  --help                  Show this message and exit.
```


### `export`

.. review data as index (or full database):

```text
$ ajum export --help
Usage: ajum export [OPTIONS] [FILE]

  Exports review data to FILE

Options:
  -s, --strict        Whether to skip invalid ISBNs.
  -f, --full          Whether to export full database.
  -j, --jobs INTEGER  Number of jobs.
  --help              Show this message and exit.
```


### `show`

.. review data for given ISBN:

```text
$ ajum show --help
Usage: ajum show [OPTIONS] ISBN

  Shows data for given ISBN

Options:
  --help  Show this message and exit.
```


### `query`

.. remote database for given search terms:


```text
Usage: aj$ ajum query --help
um query [OPTIONS]

  Queries remote database

Options:
  -q, --query TEXT         Search term.
  -t, --search-field TEXT  Search field type.
  -r, --rating TEXT        Rating.
  -f, --application TEXT   Field of application.
  -m, --media-type TEXT    Media type.
  -t, --topics TEXT        Topics.
  -a, --ages TEXT          Recommendable age range(s).
  -y, --year TEXT          Publishing year.
  --help                   Show this message and exit.
```


### `stats`

.. about (cached) reviews:

```text
$ ajum stats --help
Usage: ajum stats [OPTIONS]

  Shows statistics

Options:
  --help  Show this message and exit.
```


### `clear`

.. cached results files:

```text
$ ajum clear --help
Usage: ajum clear [OPTIONS]

  Removes cached results files

Options:
  -r, --reset  Whether to remove cached results pages.
  --help       Show this message and exit.
```


# Disclaimer

For legal reasons we only provide you with the means to download reviews. We assume neither ownership nor intellectual property of any review - they are publically available on the [AJuM website](https://www.ajum.de) and are subject to their legal sphere alone.

**Happy coding!**


:copyright: Fundevogel Kinder- und Jugendbuchhandlung
