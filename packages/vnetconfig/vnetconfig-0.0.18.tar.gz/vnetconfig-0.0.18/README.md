# vnetconfig
## _Package for extacting credentila for vNet - Internal Use_



## Features

- Connect to RDS Cluster for Multiple Env
- Get S3object based on ENV as well custom RoleArn


## Installation

vnetconfig requires [Python 3](https://www.python.org/download/releases/3.0/)  to run.

Install the dependencies by.

```
pip install vnetconfig==0.0.18
```

## Method Available

Use below python function for connecting RDS Cluster

Detail:

```
from vnet.config import *
auroraConnect(env,accessType)
```

get S3Object:

```
create_presigned_url(bucket_name, object_path, expiration=60, roleArn="None", env="None")
```


## License

MIT

**Internal Use only!**


