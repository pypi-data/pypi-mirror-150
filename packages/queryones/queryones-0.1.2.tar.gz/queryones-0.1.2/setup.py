# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['queryones']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'queryones',
    'version': '0.1.2',
    'description': 'Executing multiple sqlite queries',
    'long_description': "\n## API Reference\n\n#### import\n\n```python\n  from queryones import Query\n  from tablevalue import Manager, TableValue\n```\n\n#### Usage\n# 1. simple query with params\n```python\ndata = (('oleg', 'Asbest', 2, 1),\n                  ('ivan', 'Asbest', 1, 2),\n                  ('nastya', 'Krasnodar', 0, 2),\n                  ('Max', 'Asbest', 1, 2),\n                  ('Even', 'Krasnodar', 1, 2),\n                  ('Rob', 'Krasnodar', 1, 2),\n                  ('Mob', 'Ekaterinburg', 1, 2),\n                  ('Dick', 'Ekaterinburg', 1, 2),\n                  ('Cheize', 'Krasnodar', 1, 2),\n                  ('Longard', 'Ekaterinburg', 1, 2),\n                  )\n\nmanager = Manager()\ntable1 = TableValue(manager=manager, table_name='first_table')\ntable1.columns.add('name')\ntable1.columns.add('city')\ntable1.columns.add('children_count', TableValue.Types.INTEGER)\ntable1.columns.add('pets_count', TableValue.Types.INTEGER)\ntable1.new_bulk_insert(data)\n\nquery = Query(manager=manager)\nquery.text = '''\n    select \n        'Amigo' as name,\n        &city as city,\n        &children_count as children_count,\n        &pets_count as pets_count\n'''\nquery.set_parameter('city', 'London')\nquery.set_parameter('children_count', 3)\nquery.set_parameter('pets_count', 0)\nresult = query.execute()\nprint(result.get_data())\n```\n\n#### Output\n\n```http\n[('Amigo', 'London', 3, 0)]\n```\n\n# 2. multi query\n```python\nquery.text = '''\n    select \n        'Amigo' as name,\n        &city as city,\n        &children_count as children_count,\n        &pets_count as pets_count\n        ;\n    select\n        'chili' as come_hot\n'''\nresult = query.execute()\nprint(result.get_data())\n```\n\n#### Output\n\n```http\n[('chili',)]\n```\n\n# 3. multi query with multi result\n```python\nquery.text = '''\n    select \n        'Amigo' as name,\n        &city as city,\n        &children_count as children_count,\n        &pets_count as pets_count\n        ;\n    select\n        'chili' as some_hot\n'''\nresult = query.execute_pack()\nprint(len(result))\nprint(result[0].get_data())\nprint(result[1].get_data())\n```\n#### Output\n```http\n2\n[('Amigo', 'London', 3, 0)]\n[('chili',)]\n```\n\n# 4. Using TableValue object in query\n```python\nquery.text = '''\n    select\n    table1.name as name,\n    table1.city as city\n    into tmp_double\n    from &table1 as table1\n    ;\n    select \n    table1.name,\n    table1.city\n    from tmp_double as table1\n    \n    union all\n    \n    select\n    name,\n    city \n    from first_table\n    '''\nquery.set_parameter('table1', table1) # table1 - TableValue object\nresult = query.execute()\nfor i in result.get_data(sort='name'):\n    print(i)\n```\n#### Output\n```\n('Cheize', 'Krasnodar')\n('Cheize', 'Krasnodar')\n('Dick', 'Ekaterinburg')\n('Dick', 'Ekaterinburg')\n('Even', 'Krasnodar')\n('Even', 'Krasnodar')\n('Longard', 'Ekaterinburg')\n('Longard', 'Ekaterinburg')\n('Max', 'Asbest')\n('Max', 'Asbest')\n('Mob', 'Ekaterinburg')\n('Mob', 'Ekaterinburg')\n('Rob', 'Krasnodar')\n('Rob', 'Krasnodar')\n('ivan', 'Asbest')\n('ivan', 'Asbest')\n('nastya', 'Krasnodar')\n('nastya', 'Krasnodar')\n('oleg', 'Asbest')\n('oleg', 'Asbest')\n```\n# 5. manager tables\n```python\nprint(manager.tables.keys())\n\nprint('===deleting===')\nprint(manager.exists('first_table'))\nmanager.drop_table('first_table')\nprint(manager.exists('first_table'))\n\nprint('===deleting not exist table===')\nprint(manager.exists('test_table'))\nmanager.drop_table('test_table')\n```\n#### Output\n```\ndict_keys(['first_table', 'ResultTable0', 'ResultTable1', 'ResultTable2', 'ResultTable3', 'ResultTable4'])\n\n===deleting===\nTrue\nFalse\n\n===deleting not exist table===\nFalse\nNameError: Table [test_table] is not exists.\n```\n\n# 6. Connect to earlier created table\n```python\nmanager = Manager(os.getcwd()+os.sep+'data.db')\nif not manager.exists('first_table'):\n    table1 = TableValue(manager=manager, table_name='first_table')\n    table1.columns.add('name')\n    table1.columns.add('city')\n    table1.columns.add('children_count', TableValue.Types.INTEGER)\n    table1.columns.add('pets_count', TableValue.Types.INTEGER)\n    table1.new_bulk_insert(data)\nelse:\n    table1 = manager.get('first_table')\n    row1 = table1.get_rows(limit=1)[0]\n    print(row1)\n```\n\n#### Output\n```\n[id:1], [name:oleg], [city:Asbest], [children_count:2], [pets_count:1]\n```\n",
    'author': 'to101',
    'author_email': 'to101kv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nixonsis/query_ones',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.1,<4.0',
}


setup(**setup_kwargs)
