import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# .env 파일에서 smtp관련 변수 로드
load_dotenv()

# 환경 변수 읽기
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))
smtp_user = os.getenv('SMTP_USER')
smtp_password = os.getenv('SMTP_PASSWORD')

def send_email(to_email: str, reset_link: str):
    """이메일을 전송하는 함수"""
    
    # 이메일 내용 작성
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = "비밀번호 재설정 요청"

    body = f"비밀번호를 재설정하려면 다음 링크를 클릭하세요: {reset_link}"
    msg.attach(MIMEText(body, 'plain'))

    # SMTP 서버에 연결하여 이메일 전송
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_user, to_email, text)
        server.quit()

        print(f"비밀번호 재설정 링크가 {to_email}로 발송되었습니다.")
    except Exception as e:
        print(f"이메일 전송 중 오류가 발생했습니다: {e}")