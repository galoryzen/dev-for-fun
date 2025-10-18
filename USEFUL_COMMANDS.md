## EB Commands

```bash
# Deploy changes
eb deploy

# Open app in browser
eb open

# View logs
eb logs

# Check status
eb status

# SSH into instance
eb ssh

# View environment variables
eb printenv

# Scale application
eb scale 2

# Terminate environment
eb terminate

# Rebuild environment
eb rebuild

# Create new environment
eb create
```

## See logs while connected via SSH to EC2 instance

```bash
# Check EB health
sudo systemctl status web.service

# Application logs
sudo tail -20 /var/log/web.stdout.log

# Nginx logs
sudo tail -10 /var/log/nginx/error.log

# View environment variables
sudo cat /opt/elasticbeanstalk/deployment/env | grep RDS

# Follow logs
sudo tail -f /var/log/web.stdout.log
```