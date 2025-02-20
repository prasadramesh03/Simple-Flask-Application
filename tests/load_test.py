import requests
import time
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_request():
    try:
        response = requests.get('http://your-service-url/')
        return response.status_code
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        return 500

def run_load_test(duration_seconds=300, concurrent_users=50):
    logger.info(f"Starting load test with {concurrent_users} concurrent users for {duration_seconds} seconds")
    
    start_time = time.time()
    success_count = 0
    error_count = 0
    
    with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
        while time.time() - start_time < duration_seconds:
            futures = [executor.submit(make_request) for _ in range(concurrent_users)]
            for future in futures:
                status_code = future.result()
                if 200 <= status_code < 300:
                    success_count += 1
                else:
                    error_count += 1
            
            logger.info(f"Successful requests: {success_count}, Failed requests: {error_count}")
            time.sleep(1)
    
    logger.info("Load test completed")
    logger.info(f"Total successful requests: {success_count}")
    logger.info(f"Total failed requests: {error_count}")

if __name__ == "__main__":
    run_load_test()
