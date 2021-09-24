# tap-terminusdb

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from [TerminusDB](https://terminusdb.com/)
- Extract the specific streams in config.json
- Outputs the schema for each streams
- Incrementally pulls data based on the input state

## To install

`tap-terminusdb` can be install via pip with Python >= 3.7:

`python3 -m pip install -U tap-terminusdb`

## To use

You can start a project in a directory using conjunction with TerminusDB easily by:

`terminusdb startproject`

This will create the config.json that stores information about the endpoint and database that you are connecting to. In addition you can add the `streams` settings with:

`terminusdb config streams=[MyClass1, MyClass2]`


Then you can data from TerminusDB into a Singer.io target. For details about how to use a Singer.io target you can [see here](https://github.com/singer-io/getting-started/blob/master/docs/RUNNING_AND_DEVELOPING.md#developing-a-target).

For example, if you are extracting data from TerminusDB to [google spreadsheet](https://github.com/singer-io/target-gsheet):

```
tap-terminusdb -c config.json | target-gsheet -c gsheet-config.json
```
