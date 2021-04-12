import connections as conn

# Debug variable (for console text)
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
        (9, 'Vertigo'),
        (10, 'Default')]


def main():
    # ETL (Export Transform and Load)
    if DEBUG:
        print("########## MAPS    ETL ##########")
    # maps_etl()

    if DEBUG:
        print("########## EVENTS  ETL ##########")
    # events_etl()

    if DEBUG:
        print("########## TEAMS   ETL ##########")
    # teams_etl()

    if DEBUG:
        print("########## MATCHES ETL ##########")
    # matches_etl()

    if DEBUG:
        print("########## PLAYERS ETL ##########")
    # players_etl()

    if DEBUG:
        print("######## PERFORMANCE ETL ########")
    performance_etl()

    if DEBUG:
        print("########## VETOES  ETL ##########")
    # vetoes_etl()

    # Close connections
    conn.close_connections()


# Auxiliary function to check if a table already exists on the data warehouse connection
def table_exists(name):
    # Fetch data warehouse connection
    cursor = conn.dw.cursor()
    # Prepare query
    query = "SELECT COUNT(*) FROM information_schema.tables \
                WHERE table_schema = 'cs_go_dw' AND table_name = '{}' ".format(name)
    cursor.execute(query)
    x = cursor.fetchone()
    if DEBUG:
        print('TABLE EXISTS: ', x[0])
    if x[0] == 1:
        return True
    else:
        return False


# Auxiliary function to find map id
def find_map_id(name):
    for instance in maps:
        if instance[1] == name:
            return instance[0]


# Auxiliary function to find team id
def find_team_id(name):
    cursor = conn.dw.cursor(dictionary=True)
    query = 'SELECT id FROM teams WHERE name = "{}"'.format(name)
    # if DEBUG:
    #     print(query)
    cursor.execute(query)
    instance = cursor.fetchone()
    return instance['id']


# Function to export maps
def maps_etl():
    # Fetch data warehouse connection
    cursor = conn.dw.cursor()

    # Check if maps table does not exist
    if not table_exists('maps'):
        # Create Table
        if DEBUG:
            print("Creating maps table.")
        query = 'CREATE TABLE maps (id INT NOT NULL, \
                name VARCHAR(16) NOT NULL, \
                PRIMARY KEY (id))'
        cursor.execute(query)

        # Insert values
        if DEBUG:
            print("inserting values into maps table...")
        for instance in maps:
            # Query preparation
            query = "INSERT INTO maps (id, name) " \
                    "VALUES (%s, %s)"
            val = (instance[0], instance[1])
            # Execute and commit
            cursor.execute(query, val)
            conn.dw.commit()

        if DEBUG:
            print("Finished inserting {} values into maps table".format(len(maps)))
            print('Finished loading maps with success.')
    else:
        # If a table already exists, drop it and recall function
        if DEBUG:
            print("dropping maps table and recalling function")
        query = "DROP TABLE maps"
        cursor.execute(query)
        maps_etl()


def events_etl():
    # Fetch data warehouse connection
    cursor = conn.dw.cursor()

    # Check if table to hold events does not exist
    if not table_exists('events'):
        # Create table
        if DEBUG:
            print("Creating events table.")

        query = 'CREATE TABLE events (id INT NOT NULL, \
                name VARCHAR(128) NOT NULL, \
                start_date DATE NOT NULL, \
                end_date DATE NOT NULL, \
                PRIMARY KEY (id))'
        cursor.execute(query)

        if DEBUG:
            print("Exporting / Transforming data...")
        # Fetch main database connection
        cursor = conn.db.cursor(dictionary=True)
        # Query preparation
        query = 'SELECT DISTINCT players.event_id AS id, \
                    players.event_name AS name, \
                    MIN(players.date) AS start_date, \
                    MAX(players.date) AS end_date \
                    FROM players \
                    INNER JOIN picks \
                        ON picks.event_id = players.event_id \
                    GROUP BY players.event_id, players.event_name'

        # Execute query and fetch values
        cursor.execute(query)
        events = cursor.fetchall()

        if DEBUG:
            print("Finished exporting and transforming {} values.".format(len(events)))
            print("inserting values into maps table...")

        cursor = conn.dw.cursor()
        # Iterate through events
        for event in events:
            # Query preparation
            query = "INSERT INTO events (id, name, start_date, end_date) " \
                    "VALUES (%s, %s, %s, %s)"
            val = (event['id'], event['name'], event['start_date'], event['end_date'])

            # Execute and commit
            cursor.execute(query, val)
            conn.dw.commit()

        if DEBUG:
            print('Finished inserting {} values into events table'.format(len(events)))
            print('Finished loading events with success.')

    else:
        # If a table already exists, drop it and recall function
        if DEBUG:
            print("dropping events table and recalling function")
        query = "DROP TABLE events"
        cursor.execute(query)
        events_etl()


def teams_etl():
    # Open connection to the data warehouse
    cursor = conn.dw.cursor()

    # Check if a table to hold values does not exist
    if not table_exists('teams'):
        if DEBUG:
            print("Creating teams table.")

        # Create teams table
        query = 'CREATE TABLE teams (id INT NOT NULL, \
                name VARCHAR(32) NOT NULL, \
                PRIMARY KEY (id))'
        cursor.execute(query)

        if DEBUG:
            print("Finding teams...")

        # Open connection to main database and query teams
        cursor = conn.db.cursor(dictionary=True)
        query = 'SELECT DISTINCT team AS name FROM players'
        cursor.execute(query)
        teams = cursor.fetchall()

        if DEBUG:
            print("Inserting values into data warehouse...")

        # Open connection to the data warehouse and insert teams
        pk = 1  # Primary key
        cursor = conn.dw.cursor()
        for team in teams:
            # Query preparation
            query = "INSERT INTO teams (id, name) " \
                    "VALUES (%s, %s)"
            val = (pk, team['name'])

            # Execute and commit
            cursor.execute(query, val)
            conn.dw.commit()

            # Add 1 to the primary key value
            pk += 1

        if DEBUG:
            print('Finished inserting {} values into teams table'.format(len(teams)))
            print('Finished loading teams with success.')
    else:
        # If a table already exists, drop it and recall function
        if DEBUG:
            print("dropping teams table and recalling function")
        # Drop table
        query = "DROP TABLE teams"
        cursor.execute(query)
        # Recall function
        teams_etl()


def matches_etl():
    # Fetch data warehouse connection
    cursor = conn.dw.cursor()

    # Check if matches tables does not exist
    if not table_exists('matches'):
        if DEBUG:
            print("Creating matches table.")
        # Create table
        query = 'CREATE TABLE matches (id INT NOT NULL, \
                best_of INT NOT NULL, \
                occurred_at DATE NOT NULL, \
                PRIMARY KEY (id))'
        cursor.execute(query)

        if DEBUG:
            print("Exporting / Transforming data...")
        # Query matches
        cursor = conn.db.cursor(dictionary=True)
        query = 'SELECT DISTINCT players.match_id AS id, players.best_of, players.date AS occurred_at \
                FROM players \
                INNER JOIN picks \
                ON players.match_id = picks.match_id'
        cursor.execute(query)
        matches = cursor.fetchall()

        # Fetch data warehouse connection
        if DEBUG:
            print("Loading data...")
        cursor = conn.dw.cursor()
        for match in matches:
            # Query preparation
            query = "INSERT INTO matches (id, best_of, occurred_at) " \
                    "VALUES (%s, %s, %s)"
            val = (match['id'], match['best_of'], match['occurred_at'])

            # Execute and commit
            cursor.execute(query, val)
            conn.dw.commit()

        if DEBUG:
            print('Finished inserting {} values into matches table'.format(len(matches)))
            print('Finished loading matches with success.')

    else:
        # If a table already exists, drop it and recall function
        if DEBUG:
            print("dropping matches table and recalling function")
        # Drop table
        query = "DROP TABLE matches"
        cursor.execute(query)
        # Recall function
        matches_etl()


def players_etl():
    # Fetch data warehouse connection
    cursor = conn.dw.cursor()

    # Check if matches tables does not exist
    if not table_exists('players'):
        if DEBUG:
            print("Creating players table.")
        # Create table
        query = 'CREATE TABLE players (id INT NOT NULL, \
                   name VARCHAR(64) NOT NULL, \
                   country VARCHAR(64) NOT NULL, \
                   PRIMARY KEY (id))'
        cursor.execute(query)

        if DEBUG:
            print("Exporting / Transforming data...")
        # Query matches
        cursor = conn.db.cursor(dictionary=True)
        query = 'SELECT DISTINCT player_id AS id, player_name AS name, country from players'
        cursor.execute(query)
        players = cursor.fetchall()

        # Fetch data warehouse connection
        if DEBUG:
            print("Loading data...")
        cursor = conn.dw.cursor()
        for player in players:
            # Query preparation
            query = "INSERT INTO players (id, name, country) " \
                    "VALUES (%s, %s, %s)"

            if player['name'] is None:
                player['name'] = 'Unknown'

            val = (player['id'], player['name'], player['country'])

            # Execute and commit
            cursor.execute(query, val)
            conn.dw.commit()

        if DEBUG:
            print('Finished inserting {} values into players table'.format(len(players)))
            print('Finished loading players with success.')

    else:
        # If a table already exists, drop it and recall function
        if DEBUG:
            print("dropping players table and recalling function")
        # Drop table
        query = "DROP TABLE players"
        cursor.execute(query)
        # Recall function
        players_etl()


def performance_etl():
    # Fetch data warehouse connection
    cursor = conn.dw.cursor()
    if not table_exists('performance_fact'):
        if DEBUG:
            print("Creating players table.")
        # Create table
        query = 'CREATE TABLE performance_fact ( \
                    event_id INT NOT NULL, \
                    match_id INT NOT NULL, \
                    player_id INT NOT NULL, \
                    team_id INT NOT NULL, \
                    kills INT NOT NULL, \
                    deaths INT NOT NULL, \
                    assists INT NOT NULL, \
                    flash_assists INT NOT NULL, \
                    headshots INT NOT NULL, \
                    kd_diff INT NOT NULL, \
                    fk_diff INT NOT NULL, \
                    adr FLOAT NOT NULL, \
                    kast FLOAT NOT NULL, \
                    rating FLOAT NOT NULL, \
                    PRIMARY KEY (event_id, match_id, player_id), \
                    CONSTRAINT fk_performance_event FOREIGN KEY (event_id) REFERENCES events(id), \
                    CONSTRAINT fk_performance_match FOREIGN KEY (match_id) REFERENCES matches(id), \
                    CONSTRAINT fk_performance_player FOREIGN KEY (player_id) REFERENCES players(id), \
                    CONSTRAINT fk_performance_team FOREIGN KEY (team_id) REFERENCES teams(id))'
        cursor.execute(query)

        if DEBUG:
            print('Querying players performance...')

        cursor = conn.db.cursor(dictionary=True)
        query = 'SELECT players.event_id, \
                    players.match_id, \
                    player_id, \
                    team, kills, deaths, assists, COALESCE(flash_assists,0) AS flash_assists, \
                    hs, kddiff, fkdiff, COALESCE(adr,0) as adr, kast, rating \
                    FROM players \
                    INNER JOIN picks \
                    ON players.event_id = picks.event_id \
                    AND players.match_id = picks.match_id'
        cursor.execute(query)
        performances = cursor.fetchall()

        if DEBUG:
            print('Loading data...')

        cursor = conn.dw.cursor()
        for performance in performances:
            # Swap team name for team ID
            performance['team'] = find_team_id(performance['team'])

            # Query preparation
            query = "INSERT INTO performance_fact (event_id, match_id, player_id, team_id, kills, deaths, " \
                    "assists, flash_assists, headshots, kd_diff, fk_diff, adr, kast, rating) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            val = (performance['event_id'], performance['match_id'], performance['player_id'],
                   performance['team'], performance['kills'], performance['deaths'], performance['assists'],
                   performance['flash_assists'], performance['hs'], performance['kddiff'], performance['fkdiff'],
                   performance['adr'], performance['kast'], performance['rating'])

            # Execute and commit
            cursor.execute(query, val)
            conn.dw.commit()

        if DEBUG:
            print('Finished inserting {} values into performances table'.format(len(performances)))
            print('Finished loading "best of one" performances with success.')

        # if DEBUG:
        #     print("Querying best of one maps...")
        #
        # cursor = conn.db.cursor(dictionary=True)
        # query = 'SELECT event_id, match_id, map_1 AS map, player_id, team, kills, deaths, assists, \
        #         COALESCE(flash_assists, 0) AS flash_assists, hs, kddiff, fkdiff, COALESCE(adr, 0) as adr, \
        #         COALESCE(kast, 0.0) as kast, rating \
        #         FROM players \
        #         WHERE best_of = 1'
        # cursor.execute(query)
        # performances = cursor.fetchall()
        #
        # if DEBUG:
        #     print("Loading data....")
        #
        # cursor = conn.dw.cursor()
        # for performance in performances:
        #     # Swap map name for map id
        #     performance['map'] = find_map_id(performance['map'])
        #     performance['team'] = find_team_id(performance['team'])
        #
        #     # Query preparation
        #     query = "INSERT INTO performance_fact (event_id, match_id, map_id, player_id, team_id, kills, deaths, " \
        #             "assists, flash_assists, headshots, kd_diff, fk_diff, adr, kast, rating) " \
        #             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        #
        #     val = (performance['event_id'], performance['match_id'], performance['map'], performance['player_id'],
        #            performance['team'], performance['kills'], performance['deaths'], performance['assists'],
        #            performance['flash_assists'], performance['hs'], performance['kddiff'], performance['fkdiff'],
        #            performance['adr'], performance['kast'], performance['rating'])
        #
        #     # Execute and commit
        #     cursor.execute(query, val)
        #     conn.dw.commit()

        # if DEBUG:
            # print('Finished inserting {} values into performances table'.format(len(performances)))
            # print('Finished loading "best of one" performances with success.')
            # print("Querying best of three, second map...")

        # cursor = conn.db.cursor(dictionary=True)
        #
        # query = 'SELECT event_id,  \
        #         match_id,  \
        #         map_2 AS map, \
        #         player_id, \
        #         team, COALESCE(m2_kills, 0) AS kills, COALESCE(m2_deaths, 0) AS deaths, COALESCE(m2_assists,0) AS assists, \
        #         COALESCE(m2_flash_assists, 0) AS flash_assists, \
        #         COALESCE(m2_hs, 0) AS hs, COALESCE(m2_kddiff, 0) AS kddiff, COALESCE(m2_fkdiff,0) AS fkdiff, \
        #         COALESCE(m2_adr, 0.0) AS adr, \
        #         COALESCE(m2_kast, 0.0) AS kast, COALESCE(m2_rating, 0) AS rating \
        #         FROM players \
        #         WHERE best_of = 3'
        # cursor.execute(query)
        # performances = cursor.fetchall()
        #
        # if DEBUG:
        #     print("Loading data....")
        #
        # cursor = conn.dw.cursor()
        # for performance in performances:
        #     # Swap map name for map id
        #     if performance['map'] is None:
        #         performance['map'] = 'Default'
        #
        #     performance['map'] = find_map_id(performance['map'])
        #     # Swap team name for map id
        #     performance['team'] = find_team_id(performance['team'])
        #
        #     # Query preparation
        #     query = "INSERT INTO performance_fact (event_id, match_id, map_id, player_id, team_id, kills, deaths, " \
        #             "assists, flash_assists, headshots, kd_diff, fk_diff, adr, kast, rating) " \
        #             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        #
        #     val = (performance['event_id'], performance['match_id'], performance['map'], performance['player_id'],
        #            performance['team'], performance['kills'], performance['deaths'], performance['assists'],
        #            performance['flash_assists'], performance['hs'], performance['kddiff'], performance['fkdiff'],
        #            performance['adr'], performance['kast'], performance['rating'])
        #
        #     # Execute and commit
        #     cursor.execute(query, val)
        #     conn.dw.commit()

        # if DEBUG:
        #     # print('Finished inserting {} values into performances table'.format(len(performances)))
        #     # print('Finished loading "best of three" second map performances with success.')
        #     print("Querying best of three, third map...")
        #
        # cursor = conn.db.cursor(dictionary=True)
        #
        # query = 'SELECT event_id,  \
        #                 match_id,  \
        #                 map_3 AS map, \
        #                 player_id, \
        #                 team, COALESCE(m3_kills, 0) AS kills, COALESCE(m3_deaths, 0) AS deaths, COALESCE(m3_assists,0) AS assists, \
        #                 COALESCE(m3_flash_assists, 0) AS flash_assists, \
        #                 COALESCE(m3_hs, 0) AS hs, COALESCE(m3_kddiff, 0) AS kddiff, COALESCE(m3_fkdiff,0) AS fkdiff, \
        #                 COALESCE(m3_adr, 0.0) AS adr, \
        #                 COALESCE(m3_kast, 0.0) AS kast, COALESCE(m3_rating, 0) AS rating \
        #                 FROM players \
        #                 WHERE best_of = 3 AND map_3 IS NOT NULL'
        # cursor.execute(query)
        # performances = cursor.fetchall()
        #
        # if DEBUG:
        #     print("Loading data....")
        #
        # cursor = conn.dw.cursor()
        # for performance in performances:
        #     # Swap map name for map id
        #     if performance['map'] is None:
        #         performance['map'] = 'Default'
        #
        #     performance['map'] = find_map_id(performance['map'])
        #     # Swap team name for map id
        #     performance['team'] = find_team_id(performance['team'])
        #
        #     # Query preparation
        #     query = "INSERT INTO performance_fact (event_id, match_id, map_id, player_id, team_id, kills, deaths, " \
        #             "assists, flash_assists, headshots, kd_diff, fk_diff, adr, kast, rating) " \
        #             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        #
        #     val = (performance['event_id'], performance['match_id'], performance['map'], performance['player_id'],
        #            performance['team'], performance['kills'], performance['deaths'], performance['assists'],
        #            performance['flash_assists'], performance['hs'], performance['kddiff'], performance['fkdiff'],
        #            performance['adr'], performance['kast'], performance['rating'])
        #
        #     # Execute and commit
        #     cursor.execute(query, val)
        #     conn.dw.commit()
        #
        # if DEBUG:
        #     print('Finished inserting {} values into performances table'.format(len(performances)))
        #     print('Finished loading "best of three" third map performances with success.')

    else:
        # If a table already exists, drop it and recall function
        if DEBUG:
            print("dropping performance table and recalling function")
        # Drop table
        query = "DROP TABLE performance_fact"
        cursor.execute(query)
        # Recall function
        performance_etl()


def vetoes_etl():
    # Fetch data warehouse connection
    cursor = conn.dw.cursor()
    if not table_exists('vetoes_fact'):
        if DEBUG:
            print("Creating vetoes fact table.")
        # Create table
        query = 'CREATE TABLE vetoes_fact ( \
                        event_id INT NOT NULL, \
                        match_id INT NOT NULL, \
                        map_id INT NOT NULL, \
                        team_id INT NOT NULL, \
                        occurred_at DATE NOT NULL, \
                        PRIMARY KEY (event_id, match_id, map_id, team_id, occurred_at), \
                        CONSTRAINT fk_vetoes_event FOREIGN KEY (event_id) REFERENCES events(id), \
                        CONSTRAINT fk_vetoes_match FOREIGN KEY (match_id) REFERENCES matches(id), \
                        CONSTRAINT fk_vetoes_map FOREIGN KEY (map_id) REFERENCES maps(id), \
                        CONSTRAINT fk_vetoes_team FOREIGN KEY (team_id) REFERENCES teams(id))'
        cursor.execute(query)

        if DEBUG:
            print("Querying best of one map vetoes...")

        cursor = conn.db.cursor(dictionary=True)
        query = 'SELECT picks.date, picks.match_id, picks.event_id, \
                    team_1 AS team, \
                    t1_removed_1 AS veto_1, \
                    t1_removed_2 AS veto_2, \
                    t1_removed_3 AS veto_3 \
                    FROM picks \
                        INNER JOIN players \
                        ON picks.event_id = players.event_id \
                    WHERE picks.best_of = 1'
        cursor.execute(query)
        vetoes = cursor.fetchall()

        if DEBUG:
            print("Loading data...")

        cursor = conn.dw.cursor()
        for veto in vetoes:
            veto['team'] = find_team_id(veto['team'])
            veto['veto_1'] = find_map_id(veto['veto_1'])
            veto['veto_2'] = find_map_id(veto['veto_2'])
            veto['veto_3'] = find_map_id(veto['veto_3'])

            query = "INSERT INTO vetoes_fact (event_id, match_id, map_id, team_id, occurred_at)" \
                    "VALUES (%s, %s, %s, %s, %s)"

            # Insert and commit map veto 1
            val = (veto['event_id'], veto['match_id'], veto['veto_1'], veto['team'], veto['date'])
            cursor.execute(query, val)
            conn.dw.commit()

        if DEBUG:
            print('Finished inserting {} values into vetoes fact table'.format(len(vetoes)))
            print('Finished loading "best of one" map vetoes with success.')

    else:
        # If a table already exists, drop it and recall function
        if DEBUG:
            print("dropping vetoes fact table and recalling function")
        # Drop table
        query = "DROP TABLE vetoes_fact"
        cursor.execute(query)
        # Recall function
        vetoes_etl()


main()
