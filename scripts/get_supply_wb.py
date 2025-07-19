import os
from pprint import pprint
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parents[1]))

from postavkamp import get_supply_wb


if __name__ == "__main__":
    load_dotenv()
    authorization_id = int(os.getenv("AUTHORIZATION_ID", "4"))
    pprint(get_supply_wb(authorization_id))
