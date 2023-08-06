# alt:V Masterlist for Python

You can use this Package to interface with the alt:V master list API.

# Install 

```pip install altvmasterlist``` or ```pip3 install altvmasterlist```

# Examples

```
from altvmasterlist import masterlist as altv

# get the server json
altv.get_server_by_id("ceaac3d1cc22761223beac38386f5ab2").get_json()

# get all servers as server object
altv.get_servers()

# get all server stats
altv.get_server_stats()

# get a server and read stuff
server = altv.get_server_by_id("ceaac3d1cc22761223beac38386f5ab2")
print(server.players) 
This should output something like 200
```

# Usage

## General

If a function is failing, it is going to return None.

## Server Object

| Parameter | Type
| ------- | ------------------ 
| active | boolean
| id | string
| maxPlayers | int
| players | int
| name | string
| locked | boolean
| host | string
| port | int
| gameMode | string
| website | string
| language | string
| description | string
| verified | boolean
| promoted | boolean
| useEarlyAuth | boolean
| earlyAuthUrl | string
| useCdn | boolean
| cdnUrl | string
| useVoiceChat | boolean
| tags | array
| bannerUrl | string
| branch | string
| build | int
| version | string
| lastUpdate | int


Example:<br>
```
server = ...
print(server.players)
```

| Option  | Description           | Example Output  | Extra
| ------- | ------------------ | ------------------ | ------------------ 
| get_json() | Use this to get the Server data as Json Output | https://api.altv.mp/server/ceaac3d1cc22761223beac38386f5ab2 | There is no "info" Object
| update() | Use this to Update the Data in the Server Object | Values like server.players are updates | 
| fetchconnectjson() | Use this to fetch the Connect.json when the Server is using a CDN | ```{"earlyAuthUrl":"https://freeroam.nickwasused.com/auth","files":[{"hash":"b4029e455ff21c20","name":"core"},{"hash":"b4d95c9269392f1a","name":"dumps"},{"hash":"e1cfce6f4d8edec1","name":"webview-images"}],"host":"134.255.227.168","optional-permissions":[],"port":6135,"required-permissions":[]}``` | 

## Commands

| Option  | Description           | Example Output  | Extra
| ------- | ------------------ | ------------------ | ------------------ 
| get_server_stats() | Get the Stats of all alt:V Servers | {'serversCount': 111, 'playersCount': 665} | 
| get_servers() | Get an Array of all alt:V Servers on the Masterlist | [ServerObject1, ServerObject2, ServerObject3] | Array with Server Object
| get_server_by_id(id) | Get a specific Server using the id | ServerObject | Returned as Server Object
| get_server_by_id_avg(id, time) | Get the average Player Numbers of a specific alt:V Server | [{'t': 1638140400, 'c': 521}, {'t': 1638226800, 'c': 527}] |
| get_server_by_id_avg_result(id, time) | Get the average Player Count over a defined time span. | 300 |
| get_server_by_id_max(id, time) | Get the max Player Numbers of a specific alt:V Server | [{'t': 1638140400, 'c': 521}, {'t': 1638226800, 'c': 527}] |
| validate_id(id) | Validate a alt:V Server id | True / False | Example id: ceaac3d1cc22761223beac38386f5ab2

