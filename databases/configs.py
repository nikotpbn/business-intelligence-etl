# Configurations
niko = {
    'db':
    {
        'host': "localhost",
        'user': "root",
        'password': "951847",
        'database': "data_test",
        'connect_timeout': 2000,
        'buffered': True,

    },

    'dw':
    {
        'host': "localhost",
        'user': "root",
        'password': "951847",
        'database': "bi_csgo",
        'connect_timeout': 2000,
        'raise_on_warnings': True
    }
}

lucas = {
    'db':
        {
            'host': "localhost",
            'user': "lucas",
            'password': "",
            'database': "cs_go",
            'charset': 'utf8',
            'use_unicode': True,
            'connect_timeout': 2000,
            'buffered': True,
            'raise_on_warnings': True
        },

    'dw':
        {
            'host': "localhost",
            'user': "lucas",
            'password': "",
            'database': "bi_csgo",
            'charset': 'utf8',
            'use_unicode': True,
            'connect_timeout': 2000,
            'buffered': True,
            'raise_on_warnings': True
        }
}