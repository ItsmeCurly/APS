# Application Privacy Sentiment

Project requires Python 3.10+

## Build the project

Make sure Poetry is installed, to install it call `curl -sSL https://install.python-poetry.org | python -` and ensure Poetry is added to the environment variables.

To build requirements, call `poetry install`, this will also build a CMD executable to call the project with from the CLI.


## Manage Database

To instantiate the database, call `aps database init`.

To drop the database, call `aps database drop`.

## Google Play

View /examples for some usage examples.

### Google Play Applications and Reviews

To extract all possible apps and reviews, call `aps extract gplay --recursive` from the CLI.


## Appstore Applications and Reviews

To extract all possible apps and reviews, call `aps extract appstore --recursive` from the CLI.