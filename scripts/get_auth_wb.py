from pprint import pprint
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from postavkamp import get_active_authorizations


if __name__ == "__main__":
    pprint(get_active_authorizations())
