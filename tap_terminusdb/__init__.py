#!/usr/bin/env python3
import os
import json
import singer
from singer import utils, metadata
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema

from terminusdb_client import WOQLClient
from terminusdb_client.woqlschema import WOQLSchema
from terminusdb_client.errors import DatabaseError
from terminusdb_client.scripts.scripts import _connect, _load_settings


REQUIRED_CONFIG_KEYS = ["server", "database", "streams"]
LOGGER = singer.get_logger()


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas(config):
    """ Load schemas from database """
    client, _ = _connect(config)
    dbschema = WOQLSchema()
    dbschema.from_db(client)
    schemas = {}
    for item in dbschema.object:
        schemas[item] = dbschema.to_json_schema(item)
    return schemas


def discover(config):
    raw_schemas = load_schemas(config)
    streams = []
    for stream_id, schema in raw_schemas.items():
        # TODO: populate any metadata and stream's key properties here..
        stream_metadata = []
        key_properties = ['id']
        streams.append(
            CatalogEntry(
                tap_stream_id=stream_id,
                stream=stream_id,
                schema=schema,
                key_properties=key_properties,
                metadata=stream_metadata,
                replication_key=None,
                is_view=None,
                database=None,
                table=None,
                row_count=None,
                stream_alias=None,
                replication_method=None,
            )
        )
    return Catalog(streams)


def sync(config, state, catalog):
    """ Sync data from tap source """
    selected_streams = config["streams"]
    # Loop over selected streams in catalog
    for stream in catalog.streams:
        if stream.tap_stream_id not in selected_streams:
            LOGGER.info(f"'{stream.tap_stream_id}' is not marked selected, skipping.")
            continue
        # import pdb; pdb.set_trace()
        LOGGER.info("Syncing stream:" + stream.tap_stream_id)

        bookmark_column = stream.replication_key
        is_sorted = True  # TODO: indicate whether data is sorted ascending on bookmark value

        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema,
            key_properties=stream.key_properties,
        )

        # TODO: delete and replace this inline function with your own data retrieval process:
        # tap_data = lambda: [{"id": x, "name": "row${x}"} for x in range(1000)]
        client, _ = _connect(config)
        tap_data = client.get_documents_by_type(stream.tap_stream_id)
        max_bookmark = None
        for row in tap_data:
            # TODO: place type conversions or transformations here
            new_row = {}
            for key, value in row.items():
                if key[0] != '@':
                    new_row[key] = value
                elif key == '@id':
                    new_row['id'] = value
            row = new_row
            # write one or more rows to the stream:
            singer.write_records(stream.tap_stream_id, [row])
            if bookmark_column:
                if is_sorted:
                    # update bookmark to latest value
                    singer.write_state({stream.tap_stream_id: row[bookmark_column]})
                else:
                    # if data unsorted, save max value until end of writes
                    max_bookmark = max(max_bookmark, row[bookmark_column])
        if bookmark_column and not is_sorted:
            singer.write_state({stream.tap_stream_id: max_bookmark})
    return


@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    # if args.config:
    #     with open(args.config) as input:
    #         config = _load_settings(args.config)
    # else:
    #     config = {}

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover(args.config)
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover(args.config)
        sync(args.config, args.state, catalog)


if __name__ == "__main__":
    main()
