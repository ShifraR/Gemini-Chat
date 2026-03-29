FROM python:3.10-slim

# הוספת תעודת נטפרי (הדרך הרשמית שלהם)
ADD https://netfree.link/cacert/united/x2/unix.sh /home/netfree-unix-ca.sh
RUN cat /home/netfree-unix-ca.sh | sh

# הגדרת משתני סביבה שיעזרו ל-PIP ול-Requests
ENV REQUESTS_CA_BUNDLE=/etc/ca-bundle.crt
ENV SSL_CERT_FILE=/etc/ca-bundle.crt

WORKDIR /app

# העתקת הקובץ
COPY requirements.txt .

# התקנה עם "trusted-host" - הפעם בשורה אחת ארוכה כדי למנוע טעויות סינטקס
RUN pip install --no-cache-dir -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

COPY . .

CMD ["python", "main.py"]

