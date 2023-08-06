# unitunes

[![PyPI version](https://badge.fury.io/py/unitunes.svg)](https://badge.fury.io/py/unitunes)
![unituneslogo](https://github.com/platers/unitunes/blob/master/unitunes.png?raw=true)

A command-line interface tool to manage playlists across music streaming services.

## Introduction

unitunes is designed to keep playlists in sync across multiple streaming services.
unitunes is a free, local, replacement for services like Soundiiz and TuneMyMusic.

unitunes defines Universal Playlists (UPs), a service agnostic representation of a playlist. UPs are the source of truth for playlists on streaming services. UPs are stored as plain text JSON, enabling them to be checked into version control systems.

The unitunes CLI tool provides a command-line interface to manage UPs. Playlists can be pushed and pulled from streaming services. unitunes automatically searches for missing tracks.

### Current Supported Streaming Services

| Name          | Pullable | Pushable | Searchable |
| ------------- | :------: | :------: | :--------: |
| MusicBrainz   |          |          |     ✅     |
| Spotify       |    ✅    |    ✅    |     ✅     |
| Youtube Music |    ✅    |    ✅    |     ✅     |

Want to add support for a new streaming service? See [contributing](#contributing).

## Documentation

[Documentation](https://github.com/platers/unitunes/blob/master/docs.md)

## Quickstart

### Installation

```bash
pip install unitunes
```

### Initialize

```bash
unitunes init
```

This creates a `config.json` file in the current directory.

### Add Services

#### Spotify

Follow the instructions at https://spotipy.readthedocs.io/en/2.19.0/#getting-started to obtain client credentials.

Put the credentials in a file like so:

```json
{
  "client_id": "...",
  "client_secret": "...",
  "redirect_uri": "http://example.com"
}
```

Register the service in unitunes:

```bash
unitunes service add spotify spotify_config.json
```

#### Youtube Music

Follow the instructions at https://ytmusicapi.readthedocs.io/en/latest/setup.html#manual-file-creation to create a `ytm_config.json` file.

Register the service in unitunes:

```bash
unitunes service add ytm ytm_config.json
```

### Add Playlists

Initialize UP's from your existing playlists:

```bash
unitunes fetch spotify # use -f to skip confirmation
unitunes fetch ytm
```

### Pull Playlists

Pull all tracks from all playlists.

```bash
unitunes pull
```

### Search Playlists

Search for tracks on another service:

```bash
unitunes search SERVICE_NAME PLAYLIST_NAME
```

### Push Playlists

Push all changes to streaming services:

```bash
unitunes push
```

## Contributing

unitunes is in alpha. Contributions are very welcome. I am looking for collaborators to grow unitunes into a foundation for user controlled music software.

Take a look at the open issues!

To develop, fork the repository and clone it into your local directory. Install [poetry](https://python-poetry.org/).
Run `pytest` to run tests. Add a service config to run more tests.

```bash
pytest --spotify spotify_config.json --ytm ytm_config.json # may need to run with -s to paste spotify redirect URL the first time
```
