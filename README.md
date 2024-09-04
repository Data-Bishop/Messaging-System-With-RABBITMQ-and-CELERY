# Messaging System With Rabbitmq and Celery - Setup and Deployment Guide (For ubuntu/linux machines)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

## Local Setup
1. Clone the repository:

```
git clone https://github.com/Data-Bishop/Messaging-System-With-RABBITMQ-and-CELERY.git
cd Messaging-System-With-RABBITMQ-and-CELERY
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Set up RabbitMQ and Redis locally.
5. Configure Nginx:

- Edit /etc/nginx/sites-available/messaging_system
- Create a symlink in /etc/nginx/sites-enabled/
- Restart Nginx: sudo systemctl restart nginx
  
6. Run the Flask application:

```
python3 app.py
```

7. Start Celery worker:

```
celery -A celery_worker.celery worker --loglevel=info
```

8. Set up ngrok:
Ensure that you have completed the initial ngrok setup.
   
```
ngrok http 5000
```

## AWS EC2 Deployment
1. Launch an EC2 instance (Ubuntu 20.04 LTS).

2. SSH into your EC2 instance:

```
ssh -i your-key-pair.pem ubuntu@your-ec2-public-dns
```

3. Update and install dependencies:

```
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx rabbitmq-server redis-server -y
sudo snap install ngrok
```

4. Transfer project files:

```
scp -i your-key-pair.pem -r ./* ubuntu@your-ec2-public-dns:/home/ubuntu/messaging_system
```

5. Set up the project environment:

```
cd messaging_system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. Configure Nginx:

- Edit /etc/nginx/sites-available/messaging_system
- Create symlink: sudo ln -s /etc/nginx/sites-available/messaging_system /etc/nginx/sites-enabled

7. Test and restart Nginx:

```
sudo nginx -t
sudo systemctl restart nginx
```

8. Set up logging:

```
sudo touch /var/log/messaging_system.log
sudo chown ubuntu:ubuntu /var/log/messaging_system.log
sudo chmod 644 /var/log/messaging_system.log
```

9. Start the Flask application:

```
nohup python3 app.py > app.log 2>&1 &
```

10. Start Celery worker:

```
nohup celery -A celery_worker.celery worker --loglevel=info > celery.log 2>&1 &
```

11. Set up ngrok:

```
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
nohup ngrok http 5000 | tee ngrok_output.log &
```

12. Retrieve ngrok URL:

```
curl http://localhost:4040/api/tunnels
```
