from datetime import datetime

LOG_FILE = "logs/migration_logs.log"
ERROR_LOG = "logs/migration_errors.log"

def log(message, timestamp=True):
    if timestamp: 
      prefix=datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    else:
      prefix=""
    with open(LOG_FILE, "a") as f:
        f.write(f"{prefix} {message}\n")

def log_error(message, timestamp=True):
    if timestamp: 
      prefix=datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    else:
      prefix=""
    with open(ERROR_LOG, "a") as f:
        f.write(f"{prefix} {message}\n")
