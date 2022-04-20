import timeit
import json
import toml
import sys

import fastjsonschema
import jsonschema
from json_schema_validator import schema as json_schema, validator as json_validator


SCHEMA = """
{
  "$id": "https://example.com/person.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Person",
  "type": "object",
  "properties": {
    "firstName": {
      "type": "string",
      "description": "The person's first name."
    },
    "lastName": {
      "type": "string",
      "description": "The person's last name."
    },
    "age": {
      "description": "Age in years which must be equal to or greater than zero.",
      "type": "integer",
      "minimum": 0
    }
  }
}
"""

DATA = """
{
  "firstName": "John",
  "lastName": "Doe",
  "age": 21
}
"""

def test_fast(count, schema, data):
    name = "fastjsonschema"
    validator = fastjsonschema.compile(schema)
    start = timeit.default_timer()
    for i in range(count):
        validator(data)
    average = (timeit.default_timer() - start)/count
    return name, average


def test_jsonschema(count, schema, data):
    name = "jsonschema"
    start = timeit.default_timer()
    for i in range(count):
        jsonschema.validate(data, schema)
    average = (timeit.default_timer() - start)/count
    return name, average


def test_json_schema_validator(count, schema, data):
    name = "json_schema_validator"
    schema = json_schema.Schema(schema)
    start = timeit.default_timer()
    for i in range(count):
        json_validator.Validator.validate(schema, data)
    average = (timeit.default_timer() - start)/count
    return name, average


def main(count, schema, data):
    measured = {}
    tests = [
             {"lib": test_fast,                  "time": 0},
             {"lib": test_jsonschema,            "time": 0},
             {"lib": test_json_schema_validator, "time": 0},
            ]

    print(f"Validation {len(tests)} test, {count} iterations each")
    for i, test in enumerate(tests, 1):
        print(f"[{i}] ", end='')
        sys.stdout.flush()
        start = timeit.default_timer()
        name, mean_time = test["lib"](count, schema, data)
        elapsed = timeit.default_timer() - start
        print(f"{name + ' ' + '.'*(25-len(name))} {count} iterations, elapsed: {elapsed:<20}\tmean: {mean_time}")
        measured[name] = {"mean_validate_time": mean_time}


if __name__ == "__main__":
    count  = 100000
    schema = json.loads(SCHEMA)
    data   = json.loads(DATA)

    main(count, schema, data)
