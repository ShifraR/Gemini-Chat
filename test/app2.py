import os
import requests
from dotenv import load_dotenv

import sys

# הגדרת תו הכיווניות (RTL)
RTL_MARK = '\u200f'

# יצירת פונקציית הדפסה חדשה שעוטפת את המקורית
def print_rtl(*args, **kwargs):
    # מוסיף את תו ה-RTL לכל איבר שנשלח להדפסה
    new_args = [f"{RTL_MARK}{arg}" if isinstance(arg, str) else arg for arg in args]
    # קורא לפונקציית ההדפסה האמיתית של פייתון
    __builtins__.print(*new_args, **kwargs)

# החלפת ה-print הסטנדרטי בפונקציה שלנו
print = print_rtl

# --- מכאן והלאה את כותבת קוד כרגיל ---

print("שלום, איך זה נראה עכשיו?")
print("בדיקה של סימן שאלה?")
print(123, "מספרים עובדים גם")

# --- הגדרות תשתית (פעם אחת בתחילת הקובץ) ---
netfree_bundle = r'C:\ProgramData\NetFree\CA\netfree-ca-bundle-curl.crt'
os.environ['SSL_CERT_FILE'] = netfree_bundle
os.environ['REQUESTS_CA_BUNDLE'] = netfree_bundle

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
# המודל שעבד לנו בוודאות
MODEL_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"

def ask_gemini(prompt):
    """
    פונקציה שמקבלת טקסט ומחזירה את תגובת ה-AI
    """
    if not API_KEY:
        return "שגיאה: API_KEY לא מוגדר ב-.env"

    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(MODEL_URL, headers=headers, json=data)
        result = response.json()
        
        if response.status_code == 200:
            # שליפת הטקסט מתוך מבנה ה-JSON של גוגל
            return result['candidates'][0]['content']['parts'][0]['text']
        elif response.status_code == 429:
            return "שגיאה: חרגת מהמכסה (Quota), נסה שוב בעוד דקה."
        else:
            return f"שגיאה מהשרת ({response.status_code}): {result.get('error', {}).get('message', 'Unknown error')}"
            
    except Exception as e:
        return f"שגיאה בתקשורת: {e}"



# בדיקה מהירה של הפונקציה
if __name__ == "__main__":
    user_input = input("מה תרצה לשאול את Gemini? ")
    answer = ask_gemini(user_input)
    print("\nתשובה:")
    print(answer)