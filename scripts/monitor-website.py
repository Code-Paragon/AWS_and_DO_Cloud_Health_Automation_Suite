import requests
import smtplib
import os
import paramiko
import time
import digitalocean
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
DO_TOKEN = os.environ.get('DO_TOKEN')
DROPLET_ID = os.environ.get('DROPLET_ID')

def send_notification(email_msg):
    print('Sending notification email...')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f'Subject: Website is down\n {email_msg}'
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)

def restart_container():
    print('Restarting application container...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='167.172.49.163', username='root', key_filename='C:/Users/Adede/.ssh/id_rsa')
    stdin, stdout, stderr = ssh.exec_command('docker start a942588aa888')
    print(stdout.readlines())
    ssh.close()
    print('Application container restarted!')

def restart_droplet():
    print('Restarting droplet...')
    if not DO_TOKEN or not DROPLET_ID:
        print("DigitalOcean token or droplet ID not set in environment.")
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DO_TOKEN}"
    }
    data = {"type": "reboot"}
    url = f"https://api.digitalocean.com/v2/droplets/{DROPLET_ID}/actions"
    response_alt = requests.post(url, headers=headers, json=data)
    if response_alt.status_code == 201:
        print("Droplet reboot initiated.")
    else:
        print("Failed to reboot droplet:", response_alt.json())

def wait_for_server_ready():
    if not DO_TOKEN or not DROPLET_ID:
        print("DigitalOcean token or droplet ID not set in environment.")
        return False

    while True:
        # Create a Droplet object and refresh its data
        droplet = digitalocean.Droplet(token=DO_TOKEN, id=int(DROPLET_ID))
        droplet.load()  # updates droplet.status from the API
        print("Droplet status:", droplet.status)
        if droplet.status == 'active':
            print("Droplet is active!")
            return True
        time.sleep(5)

def restart_server_and_container():
    # Restart DigitalOcean droplet
    restart_droplet()

    # Wait until the server is back up
    if wait_for_server_ready():
        print("Waiting a bit for Docker to be fully ready...")
        time.sleep(10)  # Give Docker extra time to initialize
        restart_container()

def monitor_application():
    try:
        response = requests.get('http://167.172.49.163:8080/')
        if response.status_code == 200:
            print('The website is up and running')
        else:
            print('The website is down')
            msg = f'The website is down. Status code: {response.status_code}'
            send_notification(msg)
            # Restart the container directly if the website returns an error response
            restart_container()

    except Exception as ex:
        print(f"Connection Error happened:\n{ex}")
        msg = 'Application not accessible at all!'
        send_notification(msg)
        restart_server_and_container()

schedule.every(10).minutes.do(monitor_application)

while True:
    schedule.run_pending()

# Optimization: Should send email notification after fixing the website by restarting it!