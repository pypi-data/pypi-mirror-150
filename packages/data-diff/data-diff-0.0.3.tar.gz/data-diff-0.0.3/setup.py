# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_diff']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1,<9.0', 'dsnparse', 'pyparsing', 'runtype>=0.2.4,<0.3.0']

extras_require = \
{'mysql': ['mysql-connector-python'],
 'pgsql': ['psycopg2'],
 'preql': ['preql>=0.2.11,<0.3.0'],
 'snowflake': ['snowflake-connector-python']}

entry_points = \
{'console_scripts': ['data_diff = data_diff.__main__:main']}

setup_kwargs = {
    'name': 'data-diff',
    'version': '0.0.3',
    'description': 'A cross-database, efficient diff between mostly-similar database tables',
    'long_description': '# Data Diff\n\nA cross-database, efficient diff between mostly-similar database tables.\n\nUse cases:\n\n- Quickly validate that a table was copied correctly\n\n- Find changes between two versions of the same table\n\nWe currently support the following databases:\n\n- PostgreSQL\n\n- MySQL\n\n- Oracle\n\n- Snowflake\n\n- BigQuery\n\n- Redshift\n\n\n# How does it work?\n\nData Diff finds the differences between two tables by utilizing checksum calculations and logarithmic search.\n\nInstead of comparing the entire table, it compares the tuple (primary_key, version_column), where the primary key is a unique identifier of the rows, and the version_column updates each time the row changes to a new value, that is unique to that update. Usually the versioning column would be a timestamp like `updated_at`, that would auto-update by the database. But it could also be an auto-counting integer, and so on.\n\nData Diff runs a checksum on these columns using MD5. If the checksums are not the same, we know the tables are different. We then split each table into "n" different segments of similar size (determined by the bisection factor), and repeat the comparison for each matching pair of segments. When segments are below a certain size (bisection threshold), we instead download the segments to the client, and diff them locally.\n\nData Diff splits the segments using "checkpoints", to ensure that inserted or deleted rows don\'t affect the quality of the diff.\n\nThis process is incremental, so differences are printed to stdout as they are found. Users can ensure Data Diff quits after finding some number of differences, either by providing the `--limit` option, or by closing the pipe (for example, by piping to `head`).\n\nThe algorithm goes like this:\n\n0. Table segments `A` and `B` are set to the two tables for comparison.\n\n1. Calculate the checksums on `A` and `B` using MD5.\n\n    1. If they are the same, the tables are considered equal. Stop.\n\n    2. If their size is below the threshold, diff them locallly and print the results.\n\n    3. Else:  (they are different and above the threshold)\n\n        1. Select `n-1` rows (checkpoints) in table `A`, splitting it into `n` segments of similar size.\n\n        2. Filter out checkpoints that don\'t exist in table `B`.\n\n        3. Split both `A` and `B` into `m <= n` segments according to the mutual checkpoints. `m` must be at least 2.\n\n        4. For each pair of segments `Ai` and `Bi` (where `0 <= i <= m`), recurse into step 1.\n\n## Example\n\nThe following printout shows the diff of two tables, Original and Original_1diff, with 25 million rows each, and just 1 different row between them.\n\nWe ran it with a very low bisection factor, and with the verbose flag, to demonstrate how it works.\n\nNote: It\'s usually much faster to use high bisection factors, especially when there are very few changes, like in this example.\n\n```python\n$ data_diff postgres:/// Original  postgres:/// Original_1diff  -v --bisection-factor=4\n[16:55:19] INFO - Diffing tables of size 25000095 and 25000095 | segments: 4, bisection threshold: 1048576.\n[16:55:36] INFO - Diffing segment 0/4 of size 8333364 and 8333364\n[16:55:45] INFO - . Diffing segment 0/4 of size 2777787 and 2777787\n[16:55:52] INFO - . . Diffing segment 0/4 of size 925928 and 925928\n[16:55:54] INFO - . . . Diff found 2 different rows.\n+ (20000, 942013020)\n- (20000, 942013021)\n[16:55:54] INFO - . . Diffing segment 1/4 of size 925929 and 925929\n[16:55:55] INFO - . . Diffing segment 2/4 of size 925929 and 925929\n[16:55:55] INFO - . . Diffing segment 3/4 of size 1 and 1\n[16:55:56] INFO - . Diffing segment 1/4 of size 2777788 and 2777788\n[16:55:58] INFO - . Diffing segment 2/4 of size 2777788 and 2777788\n[16:55:59] INFO - . Diffing segment 3/4 of size 1 and 1\n[16:56:00] INFO - Diffing segment 1/4 of size 8333365 and 8333365\n[16:56:06] INFO - Diffing segment 2/4 of size 8333365 and 8333365\n[16:56:11] INFO - Diffing segment 3/4 of size 1 and 1\n[16:56:11] INFO - Duration: 53.51 seconds.\n```\n\n\n# How to install\n\nRequires Python 3.7+ with pip.\n\n    poetry build --format wheel\n    pip install "dist/data_diff-0.0.2-py3-none-any.whl[mysql,pgsql]"\n\n# How to use\n\nUsage: `data_diff DB1_URI TABLE1_NAME DB2_URI TABLE2_NAME [OPTIONS]`\n\nOptions:\n\n  - `--help` - Show help message and exit.\n  - `-k` or `--key_column` - Name of the primary key column\n  - `-c` or `--columns` - List of names of extra columns to compare\n  - `-l` or `--limit` - Maximum number of differences to find (limits maximum bandwidth and runtime)\n  - `-s` or `--stats` - Print stats instead of a detailed diff\n  - `-d` or `--debug` - Print debug info\n  - `-v` or `--verbose` - Print extra info\n  - `--bisection-factor` - Segments per iteration. When set to 2, it performs binary search.\n  - `--bisection-threshold` - Minimal bisection threshold. i.e. maximum size of pages to diff locally.\n\n## Tips for performance\n\nIt\'s highly recommended that all involved columns are indexed.\n\n# License\n\nTBD',
    'author': 'Erez Shinnan',
    'author_email': 'erezshin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/datafold/data-diff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
