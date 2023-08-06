# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_json_to_proto']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['jsp = py_json_to_proto.cli:main']}

setup_kwargs = {
    'name': 'py-json-to-proto',
    'version': '0.1.3',
    'description': 'file:README.md',
    'long_description': '# PyJsonToProto\n> Thanks for checking out PyJsonToProto, this is a port of https://github.com/json-to-proto/json-to-proto.github.io in to Python to be used in a number of applications using Protobufs\n\n## Installation\n> This package is published as a pip installable package.\n\n```bash\npip install py_json_to_proto\n```\n\n## How to use\n\n### CLI usage\n> The CLI is the name of the project abbreviated as `jsp`.  Why? Try typing `py_json_to_proto`\n> a ton of times\n\n**HELP:**\n```bash\nusage: jsp.exe [-h] [--google_timestamp GOOGLE_TIMESTAMP] [--inline INLINE] [--input_file INPUT_FILE] [--output_file OUTPUT_FILE]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --google_timestamp GOOGLE_TIMESTAMP\n                        Add timestamp to imports if in json\n  --inline INLINE       unsure...this could use a contribution\n  --input_file INPUT_FILE, -i INPUT_FILE\n                        The input file to convert\n  --output_file OUTPUT_FILE, -o OUTPUT_FILE\n                        The location to save the protos\n```\n\n\n```bash\njsp --input_file="test.json" --output_file="yolo.proto"\n```\n\n\nThe input file used\n`test.json`\n\n```json\n{\n    "id": 23357588,\n    "node_id": "MDEwOlJlcG9zaXRvcnkyMzM1NzU4OA==",\n    "name": "protobuf",\n    "full_name": "protocolbuffers/protobuf",\n    "private": false,\n    "arg2": 1009,\n    "arg1": 11124\n  }\n```\n\nThe output of the file\n`yolo.proto`\n\n```protobuf\nsyntax = "proto3";\n\nmessage SomeMessage {\n    uint32 id = 1;\n    string node_id = 2;\n    string name = 3;\n    string full_name = 4;\n    uint32 private = 5;\n    uint32 arg2 = 6;\n    uint32 arg1 = 7;\n}\n```\n\n### Code Usage\n> I would take a look at the cli code in `cli.py` to get a better feel.\n\n```python\nfrom py_json_to_proto.convert import convert, Options\n\n# Read in your json file and then convert to proto string\nwith open(\'test.json\'), \'r\') as file:\n    data = convert(file.read(), Options(False, False))\n\n# You\'re done, save the proto string\nwith open(args.output_file, \'w\') as file:\n    file.write(str(data))\n```\n___\n\n### Authors:\n* Benjamin Garrard',
    'author': 'benjamin garrard',
    'author_email': 'benjamingarrard5279@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/B2Gdevs/PyJsonToProto',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6.3,<4.0.0',
}


setup(**setup_kwargs)
