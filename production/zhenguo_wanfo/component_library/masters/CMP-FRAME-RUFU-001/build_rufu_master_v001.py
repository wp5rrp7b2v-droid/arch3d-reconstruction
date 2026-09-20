"""T-024 Rufu Master build entrypoint."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"scripts"))
from rufu_master_common_v001 import main
if __name__=="__main__": main()
