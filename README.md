
# Invantory 

This Django API is designed to maintain and build products using the Cassandra NoSQL database.

## API Reference

### Products
****GET all products****
```http
  GET /products
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
|  |  | |
 
****create new product****
```http
  POST /products
```

| Parameter | Type     | Description                | 
| :-------- | :------- | :------------------------- |
| category |`string`  | **Required**|
|color | `string`|**default** black|
| dname |`string`  | **Required**. name to display|
| required_items |`list[uuid]`  | pid of raw needed to build |
| required_items_no |`list[INT]`  | number of raw needed as per required_items |

```json
{
  "category": "PCB",
  "dname": "RS 1G",                             
  "required_items": [
    "2b955212-9f1a-11ed-a285-f889d2e645af",     
    "59851e5a-9f1a-11ed-b500-f889d2e645af"
    
  ],
  "required_items_no": [4,6]      
}
```
****GET product****
```http
  GET /products/${uuid:pid}
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
|      |    |         |

****move product to trash****
```http
  DELETE /products/${uuid:pid}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
|||||

****update product****
```http
  PUT /products/${uuid:pid}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| category |`string`  | **Required**|
|color | `string`|**default** black|
| dname |`string`  | **Required**. name to display|
| required_items |`list[uuid]`  | pid of raw needed to build |
| required_items_no |`list[INT]`  | number of raw needed as per required_items |

```json
{
  "category": "PCB",
  "dname": "RS 1G", 
  "color":"red",
  "required_items": [
    "2b955212-9f1a-11ed-a285-f889d2e645af",
    "59851e5a-9f1a-11ed-b500-f889d2e645af"
    
  ],
  "required_items_no": [4,6]
}
```
#### Trash
****GET all Trashed product****
```http
  GET /trash/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
|||||

****GET Trashed product****

```http
  GET /trash/${uuid:pid}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
|||||

****restore trashed product****
```http
  POST /trash/${uuid:pid}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| ||| |

****delete trashed product before 30 days****
```http
  DELETE /trash/${uuid:pid}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pid`     | `UUID`   | **Required**. pid to |

### Build
****GET all build product details****
```http
  GET /build/
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
|      |    |         |

****get max possible product can build in available raw****
```http
  GET /build/${uuid:pid}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
|||||

****build product****
```http
  POST /build/${uuid:pid}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `build_no`     | `INT`   | **Required**. number of product to build |

****discard product****
```http
  DELETE /build/${uuid:pid}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `discard_no`     | `INT`   | **Required**. number of product to discard |

****get build details****
```http
  GET /build/edit/${uuid:pid}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
|||||

****Edit product build info****
```http
  PUT /build/edit/${uuid:pid}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `build_no`     | `INT`   | **Required**. to set product to build number|

****Required****
```http
  GET /build/required/${uuid:pid}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
||||

### Account
****GET all workers account****
```http
  GET /account/
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
|      |    |         |

****create worker account****
```http
  POST /account/
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
|f_name      |`Text`    |**required**. first name of user         |
|l_name      |`Text`    |**required**. last name of user         |
|username    |`Text`    |**required**. username for user         |
|password    |`Text`    |**required**. password for user         |

****GET workers account****
```http
  GET /account/${string:username}
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
|      |    |         |

****Edit workers account****
```http
  PUT /account/${string:username}
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
|f_name      |`Text`    |**required**. first name of user  |
|l_name      |`Text`    |**required**. last name of user   |

