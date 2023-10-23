from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.parser import Parser
from email.policy import default
import smtplib
import json
import datetime


app = Flask(__name__)


@app.route('/alert', methods=['POST'])
def receive_alert():
    try:
        data = json.loads(request.data)
        alerts = data['alerts']

        for alert in alerts:
            summary = alert['annotations']['summary']
            severity = alert['labels']['severity']
            description = alert['annotations']['description']
            start_time = alert['startsAt']
            end_time = alert['endsAt']

            start_dt = datetime.datetime.fromisoformat(start_time.replace("Z", ""))
            start_str = start_dt.strftime("%Y-%m-%d %H:%M:%S")

            if end_time == '0001-01-01T00:00:00Z':
                end_str = start_str
            else:
                end_dt = datetime.datetime.fromisoformat(end_time.replace("Z", ""))
                end_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")

            email_body = f"""Server Monitoring: NotificationTitle: {summary}
Severity: {severity}
NotificationInfo: {description}
First Time:{start_str}
OccurTime: {end_str}
"""
            msg = MIMEText(email_body)
            msg['Subject'] = summary
            msg['From'] = 'Wang'
            msg['To'] = 'jiajie.wang'
            print(msg)
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login('1550435561@qq.com', 'mzjffxvrfqfagijb')  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail('1550435561@qq.com', ['jiajie.wang@zznode.com', ], msg.as_string())

    except Exception as e:
        print(e)

    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)