from flask import Flask, request, jsonify, render_template
from celery_worker import send_email
from datetime import datetime
from config import Config
import logging
import os

app = Flask(__name__, template_folder='html')
app.config.from_object(Config)

# Configure logging
logging.basicConfig(filename=app.config['LOG_FILE'], level=logging.INFO)

@app.route('/', methods=['GET'])
def handle_requests():
    if 'sendmail' in request.args:
        email = request.args.get('sendmail')
        if not email:
            message = f"error: Missing email address"
            return render_template('email_queued.html', message=message)

        mail_sent_message = send_email.delay(email)
        logging.info(f"Email task queued for {email}")
        message = f"Email task queued for {email}\n{mail_sent_message}"
        return render_template('email_queued.html', message=message)

    elif 'talktome' in request.args:
        log_file = app.config['LOG_FILE']
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file, 'a') as log_file:
            log_file.write(f"{current_time}\n")

        logging.info(f"Talktome request received at {current_time}")
        message = f"Logged current time: {current_time}"
        return render_template('talk_to_me.html', message=message)

    else:
        return render_template('index.html')

@app.route('/logs', methods=['GET'])
def show_logs():
    try:
        log_file = app.config['LOG_FILE']
        if os.path.exists(log_file):
             with open(log_file, 'r') as log:
                 logs = log.read()
             return logs, 200, {'Content-Type': 'text/plain'}
        else:
             return jsonify({"error": "Log file not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to read logs: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
