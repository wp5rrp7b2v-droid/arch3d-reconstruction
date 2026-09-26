"""Independent entrypoint for T-036 bottom long-kai dou; shared dou pipeline."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from dou_master_common_v001 import main
if __name__ == "__main__":
    main()
