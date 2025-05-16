import digitalocean
import os

DO_TOKEN = os.environ.get('DO_TOKEN')  # Make sure your token is set

manager = digitalocean.Manager(token=DO_TOKEN)
droplets = manager.get_all_droplets()

for droplet in droplets:
    print(f"Droplet Name: {droplet.name} | Droplet ID: {droplet.id}")