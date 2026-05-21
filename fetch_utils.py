import requests
import time
import random
import logging

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('etl_pipeline.log', encoding='utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger

def fetch_with_retry(url, max_retries=5):
    logger = setup_logger('fetch')
    for attempt in range(max_retries):
        try:
            logger.info(f"Попытка {attempt+1} загрузить {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning(f"Ошибка: {e}, попытка {attempt+1}")
        
        if attempt < max_retries - 1:
            delay = (2 ** attempt) + random.uniform(0, 0.5 * (2 ** attempt))
            time.sleep(delay)
    
    logger.critical(f"Не удалось загрузить {url} после {max_retries} попыток")
    return []