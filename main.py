from fetch_utils import setup_logger, fetch_with_retry
from validators import validate_posts
from db_utils import create_table, save_posts
from datetime import datetime

def run_etl_pipeline():
    logger = setup_logger('pipeline')
    logger.info(" ETL ПАЙПЛАЙН ЗАПУЩЕН ")
    start_time = datetime.now()

    create_table()
    
    #пагинация
    all_posts = []
    limit = 20
    start = 0
    
    while True:
        url = f"https://jsonplaceholder.typicode.com/posts?_start={start}&_limit={limit}"
        posts = fetch_with_retry(url)
        
        if not posts:
            break
        
        valid_posts = validate_posts(posts)
        all_posts.extend(valid_posts)
        
        logger.info(f"Загружено: {len(posts)} | Валидных: {len(valid_posts)} | Всего: {len(all_posts)}")
        start += limit
    
    if all_posts:
        save_posts(all_posts)
    else:
        logger.warning("Нет данных для сохранения")
    
    print("\n СТАТИСТИКА ")
    print(f"Всего загружено постов: {len(all_posts)}")
    
    long_titles = [p for p in all_posts if len(p['title']) >= 30]
    print(f"Постов с заголовком >=30 символов: {len(long_titles)}")
    
    end_time = datetime.now()
    logger.info(f"Пайплайн завершён. Время: {end_time - start_time}")
    print(f"Время выполнения: {end_time - start_time}")

if __name__ == "__main__":
    run_etl_pipeline()