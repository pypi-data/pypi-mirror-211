# mysql

### mysql Object Oriented

```shell
touch .env #and edit .env file
```
project root path command run 'touch .env' and paste environment config
```text
DB_HOST = "127.0.0.1" #host
DB_PORT = 3306 #port
DB_USER = 'root' #database login user
DB_PASSWORD = None #password
DB_NAME = 'name' #database
```

```python
from mysqloop.mysqloop import mysqloop
import time
db = mysqloop()
# create table
createtable = db.table("user_name").create_table({
    "id":"INTEGER PRIMARY KEY AUTOINCREMENT",
    "name":"VARCHAR(80) NOT NULL"
})
print(createtable)

# create datas
insert = db.table("user_name").insert([{"name": "davie"}, {"name": "johan"}])

# create data
insert = db.table("user_name").create({"name": "davie"})

# delete
db.table("user_name").where("id",1).delete()
db.table("user_name").where("name","davie").delete()

# update
db.table("user_name").where("name","davie").updata({"name":"lisa"})

# select
db.table("user_name").where("name","<>","davie").limit(5).select("*")

# find
db.table("user_name").where("name","johan").find("*")

```
