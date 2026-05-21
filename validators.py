import logging

def validate_post(post):
    required_fields = ['userId', 'title', 'id']
    for field in required_fields:
        if field not in post:
            raise KeyError(f"Нет поля {field} в посте")
    
    if not isinstance(post['userId'], int):
        raise TypeError(f"userId должен быть int, а не {type(post['userId'])}")
    
    if len(post['title']) == 0:
        raise ValueError('Заголовок не может быть пустым')
    
    if not isinstance(post['id'], int):
        raise TypeError(f"id должен быть int, а не {type(post['id'])}")
    
    logging.debug(f"Пост {post['id']} прошел валидацию")
    return True

def validate_posts(posts):
    valid_posts = []
    for post in posts:
        try:
            validate_post(post)
            valid_posts.append(post)
        except (KeyError, TypeError, ValueError) as e:
            logging.warning(f"Пост {post.get('id', 'unknown')} пропущен: {e}")
    return valid_posts