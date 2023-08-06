# AMTI Islands

Object-oriented islands in the South China Sea.

## Installation

Install with `pip`.

## Interface

### Island

The `Island` class represents an island in the South China Sea.

Each instance has the following properties:

* `url`, the URL for the AMTI reference,
* `title`, the AMTI title,
* `names`, a dictionary of names for the island,
* `occupier`, optional occupying country,
* `legal_status`, the legal status of the feature,
* `geo`, a `Coordinates` object with `lat` and `long` properties.

### AMTI

Instantiate the `AMTI` class. This is a factory class for `Island` objects and has methods `islands` (a generator for `Island` instances) and `random_island` (which returns a random `Island`).
