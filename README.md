# eth-tx-api
Practice FastAPI using a Ethereum Transaction Dataset

Start the API on a local machine using
```bash
 uvicorn app:app
 ```

Notes:
 - The csv file is in the data folder
 - pip install the python dependencies in `requirements.txt`
 - There are some minimal tests on the core logic that can be run using `pytest`
 - The two endpoints are `/stats` and `/transactions/{hash}`


