# Configurations
niko = {
    'db':
    {
        'host': "localhost",
        'user': "root",
        'password': "951847",
        'database': "cs_go",
        'connect_timeout': 2000,
        'buffered': True,

    },

    'dw':
    {
        'host': "localhost",
        'user': "root",
        'password': "951847",
        'database': "csgo_stats_dw",
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
            'database': "csgo_stats",
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
            'database': "csgo_stats_dw",
            'charset': 'utf8',
            'use_unicode': True,
            'connect_timeout': 2000,
            'buffered': True,
            'raise_on_warnings': True
        }
}