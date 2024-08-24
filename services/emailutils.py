import os
import smtplib
from dotenv import load_dotenv
from fastapi import BackgroundTasks
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer

# .env 파일에서 smtp관련 변수 로드
load_dotenv()

# 환경 변수 읽기
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))
smtp_user = os.getenv('SMTP_USER')
smtp_password = os.getenv('SMTP_PASSWORD')

# 이메일을 통해 보낼 url
DOMAIN = os.getenv('ALLOW_DOMAIN')

# 시크릿키 서명 훼손방지
serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
SALT = os.getenv("PASSWORD_RESET_SALT")

def send_reset_email(to_email: str, token: str):
    reset_link = f"{DOMAIN}/reset-password?token={token}"

    msg = MIMEMultipart('alternative')
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = "비밀번호 재설정 요청"
    body = f"비밀번호를 재설정하려면 다음 링크를 클릭하세요: {reset_link}"
    msg.attach(MIMEText(body, 'plain'))

    # SMTP 서버에 연결하여 이메일 전송
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_user, to_email, text)
        server.quit()

# 비밀번호 리셋에 쓰일 토큰 생성
def generate_reset_pwtoken(email):
    token = serializer.dumps(email, SALT)
    return token

# 비밀번호 토큰에서 이메일 추출
def get_email_from_pwtoken(token):
    email = serializer.loads(token, SALT, max_age = 3600)
    return email