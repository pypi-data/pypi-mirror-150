#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2022 drad <drader@adercon.com>

import json
from operator import itemgetter
from pathlib import Path
from typing import List

import pycouchdb
import requests
import typer
from natsort import natsorted
from rich import box
from rich.table import Table

from mpbroker.config.config import user_cfg
from mpbroker.models.media import MediaMetadata

server = pycouchdb.Server(user_cfg.database.db_uri)


def db_not_available():
    """
    Database is not available: display message and exit.
    """

    typer.secho(
        "Database unavailable, is it up?", fg=typer.colors.RED, bold=True, err=True
    )
    raise typer.Exit()


def get_sources_paths(sources: List):
    """
    Get sources paths.
    NOTE: source paths are validated (checked), if a path is invalid (does not exist)
          it will not be returned.
    @return: list of source paths.
    """

    # ~ typer.echo(f">> sources: {sources}")
    _ret = []
    for source in sources:
        # ~ typer.echo(f"   ─⏵ checking source: {source}")
        if source in user_cfg.source_mappings:
            _path = user_cfg.source_mappings[source]
            # check if path exists.
            if Path(_path).is_dir() and any(Path(_path).iterdir()):
                # ~ typer.echo(f"- found {_path} and it has data...")
                _ret.append({"source": source, "path": _path})
            # ~ typer.echo(f"- found {source} in source_mappings: {user_cfg.source_mappings[source]}")

    # typer.echo(f"_ret is: {_ret}")
    return _ret


def generate_sid(instr: str = None):
    """
    Generate a sid given an input string.
    Example: 'Duck_Dynasty_S1_D1.mkv' ─⏵ 'DCKDNSTS1D1.MKV'
    """

    return instr.translate(str.maketrans("", "", "AaEeIiOoUuYy_-()[]")).upper()


def make_doc(doc=None, rename_doc_id: bool = False):
    """
    Create a couchdb doc by deserializing the class to json, loading it back to
    json and finally renaming the doc_id field to _id.

    NOTE: the double deserialization is needed to get dates deserialized (easily)
    NOTE: we need to rename doc_id to _id as we can name it _id in the model or alias
          it as python treats it as a local and does not export it on deserialization.
    """

    j = json.loads(doc.json())
    if "doc_id" in j and rename_doc_id:
        j["_id"] = j.pop("doc_id")
    # ~ typer.echo(f"j={j}")

    return j


def extract_metadata(filepath) -> MediaMetadata:
    """
    Extract media metadata from a file
    """

    from pymediainfo import MediaInfo

    # ~ typer.echo(f"- extracting media metadata for filepath: {filepath}")
    try:
        media_info = MediaInfo.parse(filepath)

        # extract metadata
        metadata = MediaMetadata(
            file_size=media_info.tracks[0].other_file_size[0],
            file_type=media_info.tracks[1].internet_media_type,
            file_format=media_info.tracks[0].format,
            encoding=media_info.tracks[1].encoded_library_name,
            duration=media_info.tracks[0].other_duration[0],
            resolution=f"{media_info.tracks[1].width} x {media_info.tracks[1].height}",
            aspect_ratio=media_info.tracks[1].other_display_aspect_ratio[0],
            audio_format=media_info.tracks[2].format,
            audio_sampling=media_info.tracks[2].sampling_rate,
        )
    except Exception as e:
        # typer.secho(f"Failed extracting metadata for {filepath} with error: {e}", fg=typer.colors.RED, bold=True, err=True)
        return None, f"Failed extracting metadata for {filepath} with error: {e}"

    # typer.echo(f"- extracted metadata: {metadata}")

    return metadata, None


def results_by_name(name: str, user: str):
    """
    Get Results from a given Name.
    """

    try:
        db = server.database("media")
        results = db.query(
            "filters/names",
            startkey=f"{user}:{name}",
            endkey=f"{user}:{name}\ufff0",
            as_list=True,
        )
        if results:
            return results
        else:
            typer.secho("No results found", fg=typer.colors.MAGENTA, bold=True)
            raise typer.Exit()
    except requests.exceptions.ConnectionError:
        db_not_available()


def results_to_table(results=None, name: str = None, user: str = None):
    """
    Make query results into a [rich] table for display.
    """

    typer.echo("\n\n")
    # ~ typer.echo(f"- results: {results}")
    table = Table(
        title=f"Results for: '{name}'",
        title_justify="center",
        box=box.ROUNDED,
        show_lines=False,
        caption=f"Results for: '{name}'",
        collapse_padding=True,
        pad_edge=False,
        padding=0,
        show_edge=True,
        leading=0,
        header_style="bold magenta",
    )
    table.add_column("Item", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center", style="magenta")
    table.add_column("Rating")
    table.add_column("Notes")
    table.add_column("Sources", justify="right", style="yellow")
    table.add_column("Length")

    # typer.echo(f"- results: {results}")
    for item in natsorted(results, key=itemgetter(*["id"])):
        _status = item["value"][1]
        _rating = f"{item['value'][2]}" if item["value"][2] else ""
        _rating = f"{_rating} {item['value'][3]}" if item["value"][3] else _rating
        _notes = f"{item['value'][4]}" if item["value"][4] else ""
        _duration = f"{item['value'][6]}" if item["value"][6] else ""
        # ~ typer.echo(f" - {item['value'][0]}/{item['key']} | {_status} {_rating}")
        _user = f"{user}:"
        table.add_row(
            f"{item['value'][0]}/{item['key'].replace(_user, '')}",
            _status,
            _rating,
            _notes,
            f"{', '.join(item['value'][5])}",
            _duration,
        )
    return table
