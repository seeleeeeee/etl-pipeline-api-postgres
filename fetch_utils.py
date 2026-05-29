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
            
            # Проверка статус-кода
            if response.status_code == 200:
                logger.info(f"Успешно: статус {response.status_code}")
                return response.json()
            elif response.status_code == 404:
                logger.error(f"Ресурс не найден (404): {url}")
                return []  # Не повторяем, ресурса нет
            elif response.status_code == 429:
                logger.warning(f"Слишком много запросов (429), ждём дольше")
                delay = (2 ** attempt) * 5 + random.uniform(0, 2)  # дольше, чем обычно
            elif 500 <= response.status_code < 600:
                logger.warning(f"Ошибка сервера {response.status_code}, повтор через {2 ** attempt} сек")
                delay = (2 ** attempt) + random.uniform(0, 0.5 * (2 ** attempt))
            else:
                logger.warning(f"Неожиданный статус {response.status_code}, пробуем снова")
                delay = (2 ** attempt) + random.uniform(0, 0.5 * (2 ** attempt))
            if attempt < max_retries - 1:
                time.sleep(delay)
                
        except requests.exceptions.Timeout:
            logger.warning(f"Таймаут, попытка {attempt+1}")
            if attempt < max_retries - 1:
                delay = (2 ** attempt) + random.uniform(0, 0.5 * (2 ** attempt))
                time.sleep(delay)
        except Exception as e:
            logger.warning(f"Ошибка: {e}, попытка {attempt+1}")
            if attempt < max_retries - 1:
                delay = (2 ** attempt) + random.uniform(0, 0.5 * (2 ** attempt))
                time.sleep(delay)
    
    logger.critical(f"Не удалось загрузить {url} после {max_retries} попыток")
    return []