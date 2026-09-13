"""Independent CMP-FRAME-UPPER-SIX-CHUANFU-001 T-013 Master build entrypoint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from six_chuanfu_master_common_v001 import main
if __name__ == "__main__":
    main()
