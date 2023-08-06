# Transkribus API Client

`transkribus-client` provides a Python 3.6+ API client to interact with Transkribus.

## Authentication

Most of the API requires an authentication with a Transkribus account.
To authenticate, you can give your email and password to the client:

```python
from getpass import getpass
from transkribus import TranskribusAPI
api = TranskribusAPI()
TranskribusAPI.login('user@example.com', getpass())
```

Alternatively, you can use the `options_from_env` helper and some environment variables:

```python
from transkribus import TranskribusAPI, options_from_env
api = TranskribusAPI(**options_from_env())
```

You can define the following environment variables:

`TRANSKRIBUS_API_URL`
: Base URL of the Transkribus API. Defaults to `https://transkribus.eu/TrpServer/rest`.

`TRANSKRIBUS_EMAIL`
: Email address of the user to authenticate with.

`TRANSKRIBUS_PASSWORD`
: Password of the user to authenticate with.

## Usage

### Browsing from collections to transcripts

```python
from transkribus.api import TranskribusAPI, options_from_env
from transkribus.models import Collection
api = TranskribusAPI(**options_from_env())
for collection_data in api.list_collections():
    for document in Collection(collection_data).get_documents(api):
        for page in document.get_pages(api):
            print(str(page.get_transcript()))
```

### Exporting a collection

```python
collection = Collection(COLLECTION_ID)
export_job = collection.export(api)
export_job.wait_for_result(api)
export_job.download_result('path/to/export.zip')
```

### Parsing a PageXML file

```python
from transkribus.pagexml import PageXmlPage
for region in PageXmlPage('/path/to/transcript.xml').page.text_regions:
    for line in region.lines:
        print(line.text)
```

## Contributing

Issues and patches are welcome! Here are some tips to help you get started coding.

### Unit tests

We use [tox](https://tox.wiki) for unit tests. You can install and run it like so:

```
pip install tox
tox
```

### Linting

We use [pre-commit](https://pre-commit.com/) with [black](https://github.com/psf/black) to automatically format the Python source code of this project.

To be efficient, you should run pre-commit before committing (hence the name…).

To do that, run once:

```
pip install pre-commit
pre-commit install
```

The linting workflow will now run on modified files before committing, and will fix issues for you.

If you want to run the full workflow on all the files: `pre-commit run -a`.
