from os import getenv
from os.path import dirname, join
from dotenv import load_dotenv

rootDir = dirname(__file__)
dotEnvPath = join(rootDir, '.env')
load_dotenv(dotEnvPath)

connParam = {
    'dbname': getenv('DB_NAME'),
    'user': getenv('DB_USER'),
    'password': getenv('DB_PASSWORD'),
    'host': getenv('DB_HOST'),
}

telegram = {
    'username': getenv('TEL_USERNAME'),
    'api_id': getenv('TEL_API_ID'),
    'api_hash': getenv('TEL_API_HASH'),
    'phone': getenv('TEL_PHONE')
}
