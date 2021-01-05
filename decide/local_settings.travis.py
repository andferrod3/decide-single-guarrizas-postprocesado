ALLOWED_HOSTS = ["*"]
# Modules in use, commented modules that you won't use
MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]

APIS = {
    'authentication': 'http://localhost:8001',
    'base': 'http://localhost:8001',
    'booth': 'http://localhost:8001',
    'census': 'http://localhost:8001',
    'mixnet': 'http://localhost:8001',
    'postproc': 'http://localhost:8001',
    'store': 'http://localhost:8001',
    'visualizer': 'http://localhost:8001',
    'voting': 'http://localhost:8001',
}

BASEURL = 'http://localhost:8001'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256
