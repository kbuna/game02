import subprocess
import os

# mapGEN.py を実行して map.txt を生成
subprocess.run(["python", "mapGEN.py"])

# tileTST.py を実行して生成された map.txt を参照してマップを描画
subprocess.run(["python", "tileTST.py"])