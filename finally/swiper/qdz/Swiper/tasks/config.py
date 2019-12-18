broker_url = 'redis://127.0.0.1:6379/5'

broker_pool_limit = 10  # Borker连接池，默认为10

timezone = 'Asia/Shanghai'
accept_content = ['pickle', 'json']
task_serializer = 'pickle'

result_backend = 'redis://127.0.0.1:6379/5'
result_serializer = 'pickle'
result_cache_max = 10000  # 任务结果最大缓存数量
result_expires = 3600

worker_redirect_stdouts_level = 'INFO'