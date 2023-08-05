# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stairlight', 'stairlight.source']

package_data = \
{'': ['*'], 'stairlight.source': ['sql/*']}

install_requires = \
['Jinja2>=2.10.3', 'PyYAML>=5.0']

extras_require = \
{'gcs': ['google-cloud-storage>=1.28.1,<2.0.0'],
 'redash': ['psycopg2>=2.9.3,<3.0.0', 'SQLAlchemy>=1.4.31,<2.0.0']}

entry_points = \
{'console_scripts': ['stairlight = stairlight.cli:main']}

setup_kwargs = {
    'name': 'stairlight',
    'version': '0.4.1',
    'description': 'Table-level data lineage tool',
    'long_description': '<div align="center">\n  <img src="img/stairlight_white.png" width="400" alt="Stairlight">\n</div>\n\n-----------------\n\n# Stairlight\n\n[![PyPi Version](https://img.shields.io/pypi/v/stairlight.svg?style=flat-square&logo=PyPi)](https://pypi.org/project/stairlight/)\n[![PyPi License](https://img.shields.io/pypi/l/stairlight.svg?style=flat-square)](https://pypi.org/project/stairlight/)\n[![PyPi Python Versions](https://img.shields.io/pypi/pyversions/stairlight.svg?style=flat-square)](https://pypi.org/project/stairlight/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)\n[![CI](https://github.com/tosh2230/stairlight/actions/workflows/ci.yml/badge.svg)](https://github.com/tosh2230/stairlight/actions/workflows/ci.yml)\n\nA table-level data lineage tool, detects table dependencies by SELECT queries.\n\nQueries can be read from following systems.\n\n- Local file system(with Python Pathlib module)\n- [Google Cloud Storage](https://cloud.google.com/storage)\n    - Mainly designed for use with [Google Cloud Composer](https://cloud.google.com/composer)\n- [Redash](https://redash.io/)\n\n## Installation\n\nThis package is distributed on PyPI.\n\n```sh\n$ pip install stairlight\n```\n\n(v0.4+) The base package is for Local file system only. Please set extras when reading from other data sources.\n\n```sh\n$ pip install "stairlight[gcs,redash]"\n```\n\n## Getting Started\n\nThere are 3 steps to use.\n\n```sh\n# Step 1: Initialize and set data location settings\n$ stairlight init\n\'./stairlight.yaml\' has created.\nPlease edit it to set your data sources.\n\n# Step 2: Map SQL queries and tables, and add metadata\n$ stairlight map\n\'./mapping_yyyyMMddhhmmss.yaml\' has created.\nPlease map undefined tables and parameters, and append to your latest configuration file.\n\n# Step 3: Get a table dependency map\n$ stairlight\n```\n\n## Description\n\n### Input\n\n- SQL `SELECT` queries\n- Configuration files (YAML)\n    - stairlight.yaml: SQL query locations and include/exclude conditions.\n    - mapping.yaml: Mapping SQL queries and tables.\n\n### Output\n\n- Dependency map (JSON)\n\n    <details>\n\n    <summary>Example</summary>\n\n    ```json\n    {\n        "PROJECT_d.DATASET_e.TABLE_f": {\n            "PROJECT_j.DATASET_k.TABLE_l": {\n                "TemplateSourceType": "File",\n                "Key": "tests/sql/main/one_line_2.sql",\n                "Uri": "/foo/bar/stairlight/tests/sql/main/one_line_2.sql",\n                "Lines": [\n                    {\n                        "LineNumber": 1,\n                        "LineString": "SELECT * FROM PROJECT_j.DATASET_k.TABLE_l WHERE 1 = 1"\n                    }\n                ]\n            },\n            "PROJECT_C.DATASET_C.TABLE_C": {\n                "TemplateSourceType": "GCS",\n                "Key": "sql/cte/cte_multi_line.sql",\n                "Uri": "gs://stairlight/sql/cte/cte_multi_line.sql",\n                "Lines": [\n                    {\n                        "LineNumber": 6,\n                        "LineString": "        PROJECT_C.DATASET_C.TABLE_C"\n                    }\n                ],\n                "BucketName": "stairlight",\n                "Labels": {\n                    "Source": "gcs",\n                    "Test": "b"\n                }\n            }\n        },\n        "AggregateSales": {\n            "PROJECT_e.DATASET_e.TABLE_e": {\n                "TemplateSourceType": "Redash",\n                "Key": 5,\n                "Uri": "AggregateSales",\n                "Lines": [\n                    {\n                        "LineNumber": 1,\n                        "LineString": "SELECT service, SUM(total_amount) FROM PROJECT_e.DATASET_e.TABLE_e GROUP BY service"\n                    }\n                ],\n                "DataSourceName": "BigQuery",\n                "Labels": {\n                    "Category": "Sales"\n                }\n            }\n        },\n    }\n    ```\n\n    </details>\n\n## Configuration\n\nConfiguration files can be found [here](https://github.com/tosh2230/stairlight/tree/main/tests/config), used for unit test in CI.\n\n### stairlight.yaml\n\n\'stairlight.yaml\' is for setting up Stairlight itself.\n\nIt is responsible for specifying the destination of SQL queries to be read, and for specifying data sources.\n\n```yaml\nInclude:\n  - TemplateSourceType: File\n    FileSystemPath: "./tests/sql"\n    Regex: ".*/*.sql$"\n    DefaultTablePrefix: "PROJECT_A"\n  - TemplateSourceType: GCS\n    ProjectId: null\n    BucketName: stairlight\n    Regex: "^sql/.*/*.sql$"\n    DefaultTablePrefix: "PROJECT_A"\n  - TemplateSourceType: Redash\n    DatabaseUrlEnvironmentVariable: REDASH_DATABASE_URL\n    DataSourceName: BigQuery\n    QueryIds:\n      - 1\n      - 3\n      - 5\nExclude:\n  - TemplateSourceType: File\n    Regex: "main/exclude.sql$"\nSettings:\n  MappingPrefix: "mapping"\n```\n\n### mapping.yaml\n\n\'mapping.yaml\' is used to define relationships between input queries and tables.\n\nA template of this file can be created by `map` command, based on the configuration of \'stairlight.yaml\'.\n\n```yaml\nGlobal:\n  Parameters:\n    DESTINATION_PROJECT: stairlight\n    params:\n      PROJECT: 1234567890\n      DATASET: public\n      TABLE: taxirides\nMapping:\n  - TemplateSourceType: File\n    FileSuffix: "tests/sql/main/union_same_table.sql"\n    Tables:\n      - TableName: "test_project.beam_streaming.taxirides_aggregation"\n  - TemplateSourceType: GCS\n    Uri: "gs://stairlight/sql/one_line/one_line.sql"\n    Tables:\n      - TableName: "PROJECT_a.DATASET_b.TABLE_c"\n  - TemplateSourceType: Redash\n    QueryId: 5\n    DataSourceName: metadata\n    Tables:\n      - TableName: Copy of (#4) New Query\n        Parameters:\n          table: dashboards\n        Labels:\n          Category: Redash test\nMetadata:\n  - TableName: "PROJECT_A.DATASET_A.TABLE_A"\n    Labels:\n      Source: Null\n      Test: a\n```\n\n#### Global Section\n\nThis section is for global configurations.\n\n`Parameters` attribute is used to set common parameters. If conflicts has occurred with `Parameters` attributes in mapping section, mapping section\'s parameters will be used in preference to global.\n\n#### Mapping Section\n\nMapping section is used to define relationships between queries and tables that created as a result of query execution.\n\n`Parameters` attribute allows you to reflect settings in [jinja](https://jinja.palletsprojects.com/) template variables embedded in queries. If multiple settings are applied to a query using jinja template, the query will be read as if there were the same number of queries as the number of settings.\n\n#### Metadata Section\n\nThis section is mainly used to set metadata to tables appears only in queries.\n\n## Command and Option\n\n```txt\n$ stairlight --help\nusage: stairlight [-h] [-c CONFIG] [--save SAVE] [--load LOAD] {init,check,up,down} ...\n\nA table-level data lineage tool, detects table dependencies by SELECT queries.\nWithout positional arguments, return a table dependency map as JSON format.\n\npositional arguments:\n  {init,map,check,up,down}\n    init                create new Stairlight configuration file\n    map (check)         create new configuration file about undefined mappings\n    up                  return upstairs ( table | SQL file ) list\n    down                return downstairs ( table | SQL file ) list\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -c CONFIG, --config CONFIG\n                        set Stairlight configuration directory\n  -q, --quiet           keep silence\n  --save SAVE           file path where results will be saved(File system or GCS)\n  --load LOAD           file path in which results are saved(File system or GCS), can be specified multiple times\n```\n\n### init\n\n`init` creates a new Stairlight configuration file.\n\n```txt\n$ stairlight init --help\nusage: stairlight init [-h] [-c CONFIG]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -c CONFIG, --config CONFIG\n                        set Stairlight configuration directory.\n  -q, --quiet           keep silence\n```\n\n### map(check)\n\n`map` creates new configuration file about undefined mappings.`check` is an alias.\nThe option specification is the same as `init`.\n\n### up\n\n`up` outputs a list of tables or SQL files located upstream from the specified table.\n\n- Use table(`-t`, `--table`) or label(`-l`, `--label`) option to specify tables to search.\n- Recursive option(`-r`, `--recursive`) is set, Stairlight will find tables recursively and output as a list.\n- Verbose option(`-v`, `--verbose`) is set, Stairlight will add detailed information and output it as a dict.\n\n```txt\n$ stairlight up --help\nusage: stairlight up [-h] [-c CONFIG] [--save SAVE] [--load LOAD] (-t TABLE | -l LABEL) [-o {table,file}]\n                     [-v] [-r]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -c CONFIG, --config CONFIG\n                        set Stairlight configuration directory\n  -q, --quiet           keep silence\n  --save SAVE           file path where results will be saved(File system or GCS)\n  --load LOAD           file path in which results are saved(File system or GCS), can be specified multiple times\n  -t TABLE, --table TABLE\n                        table names that Stairlight searches for, can be specified\n                        multiple times. e.g. -t PROJECT_a.DATASET_b.TABLE_c -t\n                        PROJECT_d.DATASET_e.TABLE_f\n  -l LABEL, --label LABEL\n                        labels set for the table in mapping configuration, can be\n                        specified multiple times. The separator between key and value\n                        should be a colon(:). e.g. -l key_1:value_1 -l key_2:value_2\n  -o {table,file}, --output {table,file}\n                        output type\n  -v, --verbose         return verbose results\n  -r, --recursive       search recursively\n```\n\n### down\n\n`down` outputs a list of tables or SQL files located downstream from the specified table.\nThe option specification is the same as `up`.\n\n## Use as a library\n\nStairlight can also be used as a library.\n\n[tosh2230/stairlight-app](https://github.com/tosh2230/stairlight-app) is a sample web application rendering table dependency graph with Stairlight, using Graphviz, Streamlit and Google Cloud Run.\n',
    'author': 'tosh2230',
    'author_email': 'rev.to12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
