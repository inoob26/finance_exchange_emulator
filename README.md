### Requirements
- mongodb
- python3.8+

### Install dependencies
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Env variable
```shell
LOGLEVEL="INFO"
TICKERS_COUNT=100
DB_HOST="localhost"
DB_PORT=27017
DB_USERNAME="username"
DB_PASSWORD="password"
DB_NAME="mydb"
DB_COLLECTION="tickers"
```

### Run code
```shell
python main.py
```
