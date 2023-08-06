![logo do projeto](docs/assets/logo.png){width="100" .center}
# JWT Validation

The Python **jwt-validation library** is a collection of predefined codes and functions that allow users to verify a JWT token's authenticity and integrity. In other words, the library can be used to check if the JWT token is valid and was issued by a trusted source. In addition to decoding the JWT token, the library usually includes methods for verifying its digital signature, and extracting information from its header and payload. Application and system developers can integrate this library into user authentication and data security applications.


## HowTo?
The following example illustrates how to use validate-jwt in your endpoint regardless of the web request verb.

```python

from fastapi import FastAPI, Body, Depends
from fastapi.security import HTTPAuthorizationCredentials
from src.validate.validate_jwt import (security, validate_jwt,validate_jwt_scopes)

app = FastAPI()

    
@app.get("/")
@validate_jwt_scopes(required_scopes=['block-storage.read'])
async def root( credentials: HTTPAuthorizationCredentials = Depends(security),):
    
    return {"message":"WELCOME TO THE JUNGLE !!!!"}  
    
```
### Validate JWT

#### Tasks(Poetry)

The following command will load the dependencies needed to execute the poetry tasks:
```sh
$ poetry shell
```

Type the following command to verify the test coverage of implemented functionalities:
```sh
$ task test
```

You can view API documentation by uploading a service as follows: 
```sh
$ task docs
```

The following command must always be executed whenever new functionalities are implemented:
```sh
$ task lint
```