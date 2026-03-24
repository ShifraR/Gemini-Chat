import os
import requests
import json
from dotenv import load_dotenv

# הגדרות נטפרי
netfree_bundle = r'C:\ProgramData\NetFree\CA\netfree-ca-bundle-curl.crt'
os.environ['SSL_CERT_FILE'] = netfree_bundle
os.environ['REQUESTS_CA_BUNDLE'] = netfree_bundle

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

def test_gemini():
    # שינוי המודל ל-gemini-1.5-flash-latest - זה שם שגוגל תמיד מזהה ב-v1beta
    # ניסיון עם השם המדויק שהופיע אצלך ברשימה
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": "תגיד לי בבקשה 'הצלחנו!'"}]
        }]
    }

    print("🚀 ניסיון אחרון בהחלט עם המודל המעודכן...")
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if response.status_code == 200:
            text = result['candidates'][0]['content']['parts'][0]['text']
            print("\n--- תגובת ה-AI ---")
            print(text)
            print("------------------")
        elif response.status_code == 429:
             print("❌ הגענו לשרת, אבל המכסה (Quota) נגמרה. נסי שוב בעוד דקה.")
        else:
            print(f"❌ שגיאה מהשרת ({response.status_code}):")
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        print(f"❌ שגיאה בתקשורת: {e}")

if __name__ == "__main__":
    test_gemini()