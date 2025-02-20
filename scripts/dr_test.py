# scripts/dr_test.py
import subprocess
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DisasterRecoveryTest:
    def __init__(self):
        self.backup_name = f"dr-test-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
    def create_backup(self):
        logger.info("Creating backup...")
        cmd = f"velero backup create {self.backup_name} --include-namespaces default,monitoring"
        return self._run_command(cmd)
    
    def simulate_disaster(self):
        logger.info("Simulating disaster - deleting resources...")
        cmd = "kubectl delete deployment flask-app"
        return self._run_command(cmd)
    
    def restore_from_backup(self):
        logger.info("Restoring from backup...")
        cmd = f"velero restore create --from-backup {self.backup_name}"
        return self._run_command(cmd)
    
    def verify_restoration(self):
        logger.info("Verifying restoration...")
        time.sleep(30)  # Wait for restoration
        cmd = "kubectl get pods"
        return self._run_command(cmd)
    
    def _run_command(self, cmd):
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"Command failed: {result.stderr}")
                return False
            logger.info(result.stdout)
            return True
        except Exception as e:
            logger.error(f"Error executing command: {str(e)}")
            return False
    
    def run_test(self):
        steps = [
            ("Creating backup", self.create_backup),
            ("Simulating disaster", self.simulate_disaster),
            ("Restoring from backup", self.restore_from_backup),
            ("Verifying restoration", self.verify_restoration)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"\n=== {step_name} ===")
            if not step_func():
                logger.error(f"DR test failed at step: {step_name}")
                return False
        
        logger.info("\n=== DR Test Completed Successfully ===")
        return True

if __name__ == "__main__":
    dr_test = DisasterRecoveryTest()
    dr_test.run_test()