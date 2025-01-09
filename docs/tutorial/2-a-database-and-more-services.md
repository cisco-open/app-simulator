# Tutorial 2: A database and more services

> [!NOTE]
>
> This tutorial is work in progress.

In this tutorial we will take the simulation with
[two services from tutorial 1](./1-two-services.md) and add a database and some
additional services.

If you continue from tutorial 1, open `config.yaml`, otherwise create a file
with that name in an empty directory. Fill the file with the following content:

```yaml
services:
  frontend:
    type: java
    endpoints:
      http:
        /list:
          - http://backend/list/items
  backend:
    type: java
    endpoints:
      http:
        /list/items:
          - slow,1024
          - sql://backend-db/mydb?query=SELECT id, name FROM items
        /insert/item:
          - sql://backend-db/mydb?query=INSERT INTO items(id,name) VALUES(123,
            'test')
databases:
  backend-db:
    type: mysql
    databases:
      mydb:
        items: [id, name]
loaders:
  user1:
    type: curl
    wait: 5
    sleep: 1
    urls:
      - http://frontend/list
```
