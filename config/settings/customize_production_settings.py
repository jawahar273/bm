
import os
DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jawahar$bm',
        'USER': 'jawahar',
        'PASSWORD': 'jon2speed',
        'HOST': 'jawahar.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
