import streamlit as st
import os
import requests
from dotenv import load_dotenv

# --- הגדרות נטפרי וסביבה ---
os.environ['SSL_CERT_FILE'] = r'C:\ProgramData\NetFree\CA\netfree-ca-bundle-curl.crt'
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"

# הגדרת דף
st.set_page_config(page_title="Gemini Chat NetFree", layout="centered")

# CSS "אלים" ליישור לימין (RTL) - משנה את כל מבנה הצ'אט
st.markdown("""
    <style>
    /* הגדרת כיווניות כללית לאפליקציה */
    .stApp, .main, .block-container {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* הצמדת בועות הצ'אט לימין וסידור האייקון */
    [data-testid="stChatMessage"] {
        flex-direction: row-reverse !important;
    }
    
    /* יישור הטקסט בתוך הבועה */
    [data-testid="stChatMessageContent"] {
        text-align: right !important;
        direction: rtl !important;
    }

    /* תיקון לשדה הקלט שיתחיל מימין */
    .stChatInput textarea {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* הסתרת כפתור ה-GitHub והתפריט המיותר למראה נקי */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 הצ'אט שלי שפרה")

if "messages" not in st.session_state:
    st.session_state.messages = []

# הצגת היסטוריה
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# תיבת קלט
if prompt := st.chat_input("מה תרצי לשאול?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Gemini חושב..."):
        try:
            data = {"contents": [{"parts": [{"text": m["content"]}]} for m in st.session_state.messages]}
            response = requests.post(URL, json=data, timeout=30)
            
            # בדיקת חסימה של נטפרי (418, 403, או הודעה ספציפית ב-JSON)
            if response.status_code in [418, 403]:
                st.error("אופסס... נטפרי לא מרשה לי לדבר איתך על זה, לפרטים נוספים עיינו בקישור הזה https://netfree.link/wiki/%D7%A6%D7%90%D7%98_AI_%D7%91%D7%A0%D7%98%D7%A4%D7%A8%D7%99")
            
            elif response.status_code == 200:
                result = response.json()
                # וידוא שיש תוכן (לפעמים גוגל מחזיר 200 אבל עם סיבת חסימה פנימית)
                if 'candidates' in result and result['candidates'][0].get('content'):
                    answer = result['candidates'][0]['content']['parts'][0]['text']
                    with st.chat_message("assistant"):
                        st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.warning("המערכת קיבלה תשובה ריקה, ייתכן שמדובר בחסימת תוכן.")
            
            else:
                st.error(f"שגיאה לא צפויה: {response.status_code}")
                
        except Exception as e:
            st.error(f"תקלה בתקשורת: {e}")

# כפתור איפוס בצד
with st.sidebar:
    if st.button("🗑️ ניקוי שיחה"):
        st.session_state.messages = []
        st.rerun()