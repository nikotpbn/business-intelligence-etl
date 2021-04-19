from old import connections as conn

# Control Variables
DEBUG = True

# Maps variable
maps = [(1, 'Cache'),
        (2, 'Cobblestone'),
        (3, 'Dust2'),
        (4, 'Inferno'),
        (5, 'Mirage'),
        (6, 'Nuke'),
        (7, 'Overpass'),
        (8, 'Train'),
        (9, 'Vertigo')]


# Function to create all tables
def create_tables(dw):
    cursor = dw.open_connection()
    print("(Re)Creating tables tables...")
    file = open('create_model.sql')
    script_text = file.read()
    cursor.execute(script_text)


# Function to automatically populate maps
def populate_maps(dw):
    print("Populating map table...")
    cursor = dw.open_connection()
    stmt = "INSERT INTO map (id, name) VALUES (%s, %s)"
    cursor.executemany(stmt, maps)
    dw.commit()


# Function to check time
def time_exists(day, month, year):
    # Establish connection (DW)
    cursor = conn.data_warehouse().cursor()

    # Prepare statement
    stmt = "SELECT (day, month, year) FROM `time` WHERE day = {}, month = {}, year = {}".format(day, month, year)
    cursor.execute(stmt)
    exists = cursor.fetchone()

    if exists:
        return True
    else:
        return False


# Auxiliary function to find map id in memory
def find_map_id(name):
    for instance in maps:
        if instance[1] == name:
            return instance[0]
    return 0


# Auxiliary function to check if a table exists
def table_exists(name):
    # Establish connection (DW)
    cursor = conn.data_warehouse().cursor()

    # Prepare query
    query = "SELECT COUNT(*) FROM information_schema.tables \
                WHERE table_schema = 'cs_go_dw' AND table_name = '{}' ".format(name)
    cursor.execute(query)
    x = cursor.fetchone()
    cursor.close()
    if DEBUG:
        print('TABLE EXISTS: ', x[0])
    if x[0] == 1:
        return True
    else:
        return False

# Function to clean data warehouse
def drop_tables():
    # Establish connection (DW)
    cursor = conn.data_warehouse().cursor()
    print("Dropping tables...")
    query = "DROP TABLE `performance_fact`, `vetoes_fact`, `event`, `map`, `player`, `team`, `time`,`match`;"
    cursor.execute(query)
    cursor.close()
    conn.data_warehouse().close()