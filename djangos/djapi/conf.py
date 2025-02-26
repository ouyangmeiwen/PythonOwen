DEBUG = True
DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.mysql',  #mysql
        'NAME': 'djangodb',
        'USER': 'root',
        'PASSWORD': 'abc@123',
        'HOST': '192.168.229.130',
        'PORT': '3306',
    },
    'invengodb': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'invengodbv41',
        'USER': 'root',
        'PASSWORD': 'abc@123',
        'HOST': '192.168.229.130',
        'PORT': '3306',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.oracle',
    #     'NAME': 'DCLHR',  # Oracle 数据库的服务名或 SID
    #     'USER': 'C##sa',      # 用户名
    #     'PASSWORD': 'abc123',  # 密码
    #     'HOST': '192.168.229.130',          # 数据库主机地址（如 192.168.229.130）
    #     'PORT': '1521',               # Oracle 数据库端口，默认 1521
    # }

    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',  #postsql
    #     'NAME': 'postgres',
    #     'USER': 'postgres',
    #     'PASSWORD': 'abc@123',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # }


    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',  #sqllite
    #     'NAME': 'db.sqlite3'
    # }
}