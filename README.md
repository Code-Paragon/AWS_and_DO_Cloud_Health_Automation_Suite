# 🧬 AWS & DO Cloud Health Automation Suite

A collection of Python automation scripts for monitoring, backing up, and restoring infrastructure resources on AWS EC2, EKS, and **DigitalOcean**. Includes scheduled health checks, volume snapshot handling, and container uptime recovery mechanisms.

---

## 🛠️ Features

-  **EC2 Instance Health Checks** (Scheduled)
-  **EKS Cluster Status Reports**
-  **Volume Snapshot Backups & Pruning**
-  **Volume Restoration from Snapshots**
-  **Website Availability Monitoring** with Email Alerts
-  **Automatic Droplet and Container Recovery** (DigitalOcean)
-  Environment-driven config for secrets/API keys

---

## 📁 Directory Structure

```text
scripts/
├─ ec2-status-checks.py       # EC2 instance health monitor
├─ eks-status-checks.py       # EKS cluster monitor
├─ monitor-website.py         # Uptime check + container/droplet recovery
├─ clean-snapshots.py         # Retain only latest 2 snapshots per volume
├─ restore-volume.py          # Restore EBS volume from most recent snapshot
├─ volume-backups.py          # Scheduled volume snapshot creator
.env.example                  # Sample env file
requirements.txt              # Python dependencies
```

---

## 🚀 Usage

**Install dependencies:**
```
pip install -r requirements.txt
```

**Set up environment variables:**
```
cp .env.example .env
```

**Run any script:**
```
python scripts/ec2-status-checks.py
```

---

## 📨 Notifications

- Emails sent via Gmail SMTP when website goes down
- DigitalOcean recovery scripts restart both Droplet and Docker container
- paramiko is used for SSH-based remote container control

---

## ⚠️ Security Notes

- Never commit .env with secrets
- Consider adding .env to your .gitignore
- Configure AWS and DO credentials securely via environment or IAM roles

