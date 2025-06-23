import os
from dotenv import load_dotenv

# Manually specify the path to the env file
from pathlib import Path

env_path = Path(__file__).parent.parent / '..'/ '.env'

def getValue(key):
    # print("from config"+str(env_path))
    load_dotenv(dotenv_path=env_path)

    value = os.getenv(key)
    if value is None:
        raise EnvironmentError(f"Missing required environment variable: {key}")
    return value
