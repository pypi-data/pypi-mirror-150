
## API Reference

#### import

```python
  from queryones import Query
  from tablevalue import Manager, TableValue
```

#### Usage
# 1. simple query with params
```python
data = (('oleg', 'Asbest', 2, 1),
                  ('ivan', 'Asbest', 1, 2),
                  ('nastya', 'Krasnodar', 0, 2),
                  ('Max', 'Asbest', 1, 2),
                  ('Even', 'Krasnodar', 1, 2),
                  ('Rob', 'Krasnodar', 1, 2),
                  ('Mob', 'Ekaterinburg', 1, 2),
                  ('Dick', 'Ekaterinburg', 1, 2),
                  ('Cheize', 'Krasnodar', 1, 2),
                  ('Longard', 'Ekaterinburg', 1, 2),
                  )

manager = Manager()
table1 = TableValue(manager=manager, table_name='first_table')
table1.columns.add('name')
table1.columns.add('city')
table1.columns.add('children_count', TableValue.Types.INTEGER)
table1.columns.add('pets_count', TableValue.Types.INTEGER)
table1.new_bulk_insert(data)

query = Query(manager=manager)
query.text = '''
    select 
        'Amigo' as name,
        &city as city,
        &children_count as children_count,
        &pets_count as pets_count
'''
query.set_parameter('city', 'London')
query.set_parameter('children_count', 3)
query.set_parameter('pets_count', 0)
result = query.execute()
print(result.get_data())
```

#### Output

```http
[('Amigo', 'London', 3, 0)]
```

# 2. multi query
```python
query.text = '''
    select 
        'Amigo' as name,
        &city as city,
        &children_count as children_count,
        &pets_count as pets_count
        ;
    select
        'chili' as come_hot
'''
result = query.execute()
print(result.get_data())
```

#### Output

```http
[('chili',)]
```

# 3. multi query with multi result
```python
query.text = '''
    select 
        'Amigo' as name,
        &city as city,
        &children_count as children_count,
        &pets_count as pets_count
        ;
    select
        'chili' as some_hot
'''
result = query.execute_pack()
print(len(result))
print(result[0].get_data())
print(result[1].get_data())
```
#### Output
```http
2
[('Amigo', 'London', 3, 0)]
[('chili',)]
```

# 4. Using TableValue object in query
```python
query.text = '''
    select
    table1.name as name,
    table1.city as city
    into tmp_double
    from &table1 as table1
    ;
    select 
    table1.name,
    table1.city
    from tmp_double as table1
    
    union all
    
    select
    name,
    city 
    from first_table
    '''
query.set_parameter('table1', table1) # table1 - TableValue object
result = query.execute()
for i in result.get_data(sort='name'):
    print(i)
```
#### Output
```
('Cheize', 'Krasnodar')
('Cheize', 'Krasnodar')
('Dick', 'Ekaterinburg')
('Dick', 'Ekaterinburg')
('Even', 'Krasnodar')
('Even', 'Krasnodar')
('Longard', 'Ekaterinburg')
('Longard', 'Ekaterinburg')
('Max', 'Asbest')
('Max', 'Asbest')
('Mob', 'Ekaterinburg')
('Mob', 'Ekaterinburg')
('Rob', 'Krasnodar')
('Rob', 'Krasnodar')
('ivan', 'Asbest')
('ivan', 'Asbest')
('nastya', 'Krasnodar')
('nastya', 'Krasnodar')
('oleg', 'Asbest')
('oleg', 'Asbest')
```
# 5. manager tables
```python
print(manager.tables.keys())

print('===deleting===')
print(manager.exists('first_table'))
manager.drop_table('first_table')
print(manager.exists('first_table'))

print('===deleting not exist table===')
print(manager.exists('test_table'))
manager.drop_table('test_table')
```
#### Output
```
dict_keys(['first_table', 'ResultTable0', 'ResultTable1', 'ResultTable2', 'ResultTable3', 'ResultTable4'])

===deleting===
True
False

===deleting not exist table===
False
NameError: Table [test_table] is not exists.
```

# 6. Connect to earlier created table
```python
manager = Manager(os.getcwd()+os.sep+'data.db')
if not manager.exists('first_table'):
    table1 = TableValue(manager=manager, table_name='first_table')
    table1.columns.add('name')
    table1.columns.add('city')
    table1.columns.add('children_count', TableValue.Types.INTEGER)
    table1.columns.add('pets_count', TableValue.Types.INTEGER)
    table1.new_bulk_insert(data)
else:
    table1 = manager.get('first_table')
    row1 = table1.get_rows(limit=1)[0]
    print(row1)
```

#### Output
```
[id:1], [name:oleg], [city:Asbest], [children_count:2], [pets_count:1]
```
