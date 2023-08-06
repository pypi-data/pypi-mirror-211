# BOSMiner-py

Python client to retrieve data from any miner running Braiins OS+ Socket API.


## Install

```
pip install bosminer
```

## Usage

```python
from bosminer.client import BosMiner

host = 'moe.s5p8'
miner = BosMiner(host)
print(miner.version())
```

```json
{
   "STATUS": [
      {
         "STATUS": "S",
         "When": 1684938931,
         "Code": 22,
         "Msg": "BOSer versions",
         "Description": "BOSer boser-buildroot 0.1.0-0ce150e9"
      }
   ],
   "VERSION": [
      {
         "API": "3.7",
         "BOSer": "boser-buildroot 0.1.0-0ce150e9"
      }
   ],
   "id": 1
}
```

```python
print(miner.fans())
```

```json
{
   "STATUS": [
      {
         "STATUS": "S",
         "When": 1684941022,
         "Code": 202,
         "Msg": "4 Fan(s)",
         "Description": "BOSer boser-buildroot 0.1.0-0ce150e9"
      }
   ],
   "FANS": [
      {
         "FAN": 0,
         "ID": 0,
         "RPM": 3226,
         "Speed": 32
      },
      {
         "FAN": 1,
         "ID": 1,
         "RPM": 3315,
         "Speed": 32
      },
      {
         "FAN": 2,
         "ID": 2,
         "RPM": 3226,
         "Speed": 32
      },
      {
         "FAN": 3,
         "ID": 3,
         "RPM": 3255,
         "Speed": 32
      }
   ],
   "id": 1
}

```

## Implemented commands

All available commands are implemented. Check [Bosminer API docs](https://docs.braiins.com/os/plus-en/Development/1_api.html).

> The commands switchpool, enablepool, disablepool, addpool and removepool are not fully implemented in Braiins OS. The outcome of these commands is reset after restart and they do not activate the pools. This is a known issue and is being fixed.
