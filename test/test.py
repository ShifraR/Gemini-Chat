import pandas as pd
import sklearn
print("Pandas version:", pd.__version__)
print("Scikit-learn version:", sklearn.__version__)
print("Success! Everything is ready for the test.")
print()

import requests
try:
    # ניסיון לגשת לאתר מאובטח
    response = requests.get("https://www.google.com", timeout=5)
    print("✅ הניצחון! Python מצליח לעבור את הסינון ולגשת לאינטרנט.")
except Exception as e:
    print(f"❌ עדיין יש חסימה: {e}")