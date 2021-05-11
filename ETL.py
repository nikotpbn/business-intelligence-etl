import datetime as dt
import mysql.connector
from mysql.connector import errorcode
# import scrapper
import json
import csv


class StagingArea:

    def __init__(self, user_config):
        # Access configurations
        self.db_config = user_config['db']
        self.dw_config = user_config['dw']

        # Connections variables
        self.db = None
        self.dw = None

        # Staging Variables
        self.events = None
        self.players = None
        self.matches = None
        self.teams = None
        self.times = None
        self.vetoes = []
        self.dict_events = {}
        # self.dict_matches = {}
        self.regions = []

        # Maps
        self.maps = [
            (1, 'Cache'),
            (2, 'Cobblestone'),
            (3, 'Dust2'),
            (4, 'Inferno'),
            (5, 'Mirage'),
            (6, 'Nuke'),
            (7, 'Overpass'),
            (8, 'Train'),
            (9, 'Vertigo')
        ]

    # Print database configurations
    def config(self):
        print(self.db_config)
        print(self.db_config)

    ####################################################################
    ################## CONNECTION RELATED METHODS ######################
    ####################################################################

    # Open connections
    def open_connection(self):
        try:
            self.db = mysql.connector.connect(**self.db_config)
            self.dw = mysql.connector.connect(**self.dw_config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    # Close connections
    def close_connection(self):
        self.db.close()
        self.dw.close()

    ####################################################################
    #################### DATABASE RELATED METHODS ######################
    ####################################################################
    # Create data warehouse tables
    def create_tables(self):
        print("(Re)Creating tables tables...")
        self.open_connection()
        cursor = self.dw.cursor()
        file = open('create_model.sql')
        script_text = file.read()
        cursor.execute(script_text, multi=True)

    # Drop data warehouse tables
    def drop_tables(self):
        print("Dropping tables...")
        self.open_connection()
        cursor = self.dw.cursor()
        query = "DROP TABLE `performance_fact`, `vetoes_fact`, `event`, `de_map`, `player`, `team`, `time`,`match`;"
        cursor.execute(query, multi=True)
        cursor.close()

    # Populate maps (from memory)
    def populate_maps(self):
        print("Populating maps table...")
        self.open_connection()
        cursor = self.dw.cursor()
        stmt = "INSERT INTO de_map (id, name) " \
               "VALUES (%s, %s)"
        cursor.executemany(stmt, self.maps)
        self.dw.commit()
        cursor.close()

    ####################################################################
    #################### DATASET RELATED METHODS #######################
    ####################################################################
    # Load country per continent list into object variable
    def load_continent_country(self):
        with open('datasets/continents-according-to-our-world-in-data.csv') as f:
            data = csv.reader(f)
            for index, row in enumerate(data):
                # 0['Entity', 'Code', 'Year', 'Continent']
                if index > 0:
                    data = {
                        'Entity': row[0],
                        'Code': row[1],
                        'Year': row[2],
                        'Continent': row[3]
                    }
                    self.regions.append(data)
        f.close()

    # Find a country continent by name
    def find_continent(self, country):
        continent = None
        for entry in self.regions:
            if entry['Entity'] == country:
                continent = entry['Continent']
        return continent

    # TODO: FUNCTION IS NOT NECESSARY, CAN BE REMOVED
    def check_data_warehouse_players_continent(self):
        self.open_connection()
        cursor = self.dw.cursor(dictionary=True)
        stmt = "SELECT * FROM player"
        cursor.execute(stmt)
        players = cursor.fetchall()
        cursor.close()

        for player in players:
            continent = self.find_continent(player['country'])
            if continent is None:
                print("Name: {}  |  Country: {}  |  Continent: {}".format(player['name'], player['country'], continent))


    ####################################################################
    ####################### ETL RELATED METHODS ########################
    ####################################################################
    def export_and_transform_events(self):
        print("Exporting and transforming events...")
        self.open_connection()
        cursor = self.db.cursor(dictionary=True)
        stmt = "SELECT DISTINCT \
                    players.event_id as id, \
                    TRIM(players.event_name) as name \
                FROM players \
                INNER JOIN picks \
                    ON picks.match_id = players.match_id \
                    AND picks.event_id = players.event_id \
                INNER JOIN results \
                    ON results.match_id = players.match_id \
                    AND results.event_id = results.event_id \
                ORDER BY id;"
        cursor.execute(stmt)
        self.events = cursor.fetchall()

    def load_events(self):
        self.report_quantity(len(self.events), "events")
        self.open_connection()
        cursor = self.dw.cursor()
        for event in self.events:
            stmt = "INSERT INTO event (id, name) " \
                   "VALUES (%s, %s)"
            data = (event['id'], event['name'])
            cursor.execute(stmt, data)
            self.dw.commit()
        cursor.close()

    def update_events(self):
        self.report_quantity(len(self.events), "events")
        self.open_connection()
        cursor = self.dw.cursor(dictionary=True)
        with open('events.json') as json_file:
            self.dict_events = json.load(json_file)
        for event in self.events:
            lan = self.dict_events[str(event['id'])][0]
            stars = self.dict_events[str(event['id'])][1]
            tier = self.get_event_tier(event['id'], cursor)
            stmt = "UPDATE event SET tier = %s, lan = %s, stars = %s WHERE id = %s"
            data = (tier, lan, stars, event['id'])
            cursor.execute(stmt, data)
            self.dw.commit()
        cursor.close()

    # def load_scrap_events(self):
    #     self.report_quantity(len(self.events), "events tiers to fill")
    #     self.open_connection()
    #     cursor = self.dw.cursor()
    #     for event in self.events:
    #         lan = scrapper.scrap_lan(event['id'])
    #         stmt = f"UPDATE event SET lan = {lan} WHERE id = {event['id']}"
    #         cursor.execute(stmt)
    #         self.dw.commit()
    #     cursor.close()

    def export_and_transform_players(self):
        print("Exporting and transforming players...")
        self.open_connection()
        cursor = self.db.cursor(dictionary=True)
        stmt = "SELECT DISTINCT \
                    players.player_id AS id, \
                    TRIM(players.player_name) AS name, \
                    TRIM(players.country) AS country \
                FROM players \
                INNER JOIN picks \
                    ON picks.match_id = players.match_id \
                    AND picks.event_id = players.event_id \
                INNER JOIN results \
                    ON results.match_id = players.match_id \
                    AND results.event_id = players.event_id \
                ORDER BY id;"
        cursor.execute(stmt)
        self.players = cursor.fetchall()
        cursor.close()

    def load_players(self):
        self.report_quantity(len(self.players), "players")
        self.open_connection()
        cursor = self.dw.cursor()
        for player in self.players:
            stmt = "INSERT INTO player (id, name, country) " \
                   "VALUES (%s, %s, %s)"
            data = (player['id'], player['name'], player['country'])
            cursor.execute(stmt, data)
            self.dw.commit()
        cursor.close()

    def export_and_transform_matches(self):
        print("Exporting and transforming matches...")
        self.open_connection()
        cursor = self.db.cursor(dictionary=True)
        stmt = "SELECT DISTINCT players.match_id AS id, \
                results.rank_1, \
                results.rank_2, \
                players.best_of AS best_of \
                FROM players \
                INNER JOIN picks \
                    ON picks.match_id = players.match_id \
                    AND picks.event_id = players.event_id \
                INNER JOIN results  \
                    ON results.match_id = players.match_id \
                    AND results.event_id = players.event_id \
                ORDER BY id"
        cursor.execute(stmt)
        self.matches = cursor.fetchall()
        cursor.close()

    def load_matches(self):
        self.report_quantity(len(self.matches), "matches")
        self.open_connection()
        cursor = self.dw.cursor()
        for match in self.matches:
            tier = self.get_match_tier(match['rank_1'], match['rank_2'])
            stmt = "INSERT INTO `match` (id, best_of, tier) " \
                   "VALUES (%s, %s, %s)"
            data = (match['id'], match['best_of'], tier)
            cursor.execute(stmt, data)
            self.dw.commit()
        cursor.close()

    def export_and_transform_teams(self):
        print("Exporting and transforming teams...")
        self.open_connection()
        cursor = self.db.cursor(dictionary=True)
        stmt = "SELECT DISTINCT TRIM(players.team) as name \
                FROM players \
                   INNER JOIN picks \
                    ON picks.match_id = players.match_id \
                    AND picks.event_id = players.event_id \
                INNER JOIN results \
                    ON results.match_id = players.match_id \
                    AND results.event_id = results.event_id \
                ORDER BY name;"
        cursor.execute(stmt)
        self.teams = cursor.fetchall()
        cursor.close()

    def load_teams(self):
        self.report_quantity(len(self.teams), "teams")
        self.open_connection()
        cursor = self.dw.cursor()
        pk = 1
        for team in self.teams:
            stmt = "INSERT INTO team (id, name)" \
                   "VALUES (%s, %s)"
            data = (pk, team['name'])
            cursor.execute(stmt, data)
            self.dw.commit()
            pk += 1
        cursor.close()

    def export_and_transform_time(self):
        print("Exporting and transforming times...")
        self.open_connection()
        cursor = self.db.cursor(dictionary=True)
        stmt = "SELECT DISTINCT \
                    players.date \
                FROM players \
                   INNER JOIN picks \
                    ON picks.match_id = players.match_id \
                    AND picks.event_id = players.event_id \
                INNER JOIN results \
                    ON results.match_id = players.match_id \
                    AND results.event_id = results.event_id \
                ORDER BY players.date;"
        cursor.execute(stmt)
        self.times = cursor.fetchall()
        cursor.close()

        # Transform data
        pk = 1
        for time in self.times:
            time_split = time['date'].split("-")
            year = int(time_split[0])
            month = int(time_split[1])
            day = int(time_split[2])
            semester = self.check_semester(month)
            quarter = self.check_quarter(month)
            week_of_month = self.check_week_of_month(day)
            weekday = dt.datetime(year, month, day).weekday() # Return the day of the week as an integer, where Monday is 0 and Sunday is 6
            weekend = self.check_weekend(year, month, day)

            time.update({'id': pk,
                         'year': year,
                         'month': month,
                         'day': day,
                         'semester': semester,
                         'quarter': quarter,
                         'week_of_month': week_of_month,
                         'weekday': weekday,
                         'weekend': weekend})
            pk = pk + 1

    def load_times(self):
        self.report_quantity(len(self.times), "times")
        self.open_connection()
        cursor = self.dw.cursor()
        for time in self.times:
            stmt = "INSERT INTO time (id, year, month, day, semester, quarter, week_of_month, weekend, weekday)" \
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (time['id'],
                    time['year'],
                    time['month'],
                    time['day'],
                    time['semester'],
                    time['quarter'],
                    time['week_of_month'],
                    time['weekend'],
                    time['weekday'])
            cursor.execute(stmt, data)
            self.dw.commit()
        cursor.close()

    def export_and_transform_performance(self):
        print("Exporting and transforming performance facts...")
        self.open_connection()
        cursor = self.db.cursor(dictionary=True)
        stmt = "SELECT DISTINCT \
                   players.event_id, \
                   players.match_id, \
                   players.player_id, \
                   TRIM(players.team) as team, \
                   players.date, \
                   kills, deaths, assists, \
                   hs, kddiff, fkdiff, COALESCE(adr,0) as adr, kast, rating \
                FROM players \
                INNER JOIN picks \
                    ON picks.match_id = players.match_id \
                    AND picks.event_id=  players.event_id \
                INNER JOIN results \
                    ON results.match_id = players.match_id \
                    AND results.event_id = players.event_id;"

        cursor.execute(stmt)
        self.performances = cursor.fetchall()
        cursor.close()

        # Transform
        for performance in self.performances:
            time_split = performance['date'].split("-")
            year = int(time_split[0])
            month = int(time_split[1])
            day = int(time_split[2])
            time_id = self.get_time_id(year, month, day)
            team_id = self.get_team_id(performance['team'])
            performance.update({'time_id': time_id,
                                'team_id': team_id})

    def load_performances(self):
        self.report_quantity(len(self.performances), "performances")
        self.open_connection()
        cursor = self.dw.cursor()
        for performance in self.performances:
            stmt = "INSERT INTO performance_fact (event_id, match_id, team_id, player_id, time_id," \
                   "kills, deaths, assists, headshots, kddiff, fkdiff, adr, kast, rating)" \
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (performance['event_id'], performance['match_id'], performance['team_id'],
                    performance['player_id'], performance['time_id'], performance['kills'],
                    performance['deaths'], performance['assists'],
                    performance['hs'], performance['kddiff'], performance['fkdiff'],
                    performance['adr'], performance['kast'], performance['rating'])
            cursor.execute(stmt, data)
            self.dw.commit()
        cursor.close()

    def export_and_transform_veto(self):
        print("Exporting and transforming vetoes...")
        self.open_connection()
        cursor = self.db.cursor(dictionary=True)
        stmt = "SELECT DISTINCT \
                    picks.event_id, \
                    picks.match_id, \
                    picks.date, TRIM(picks.team_1) AS team_1, TRIM(picks.team_2) AS team_2, \
                    TRIM(picks.t1_removed_1) AS t1_removed_1, \
                    TRIM(picks.t1_removed_2) AS t1_removed_2, \
                    TRIM(picks.t1_removed_3) AS t1_removed_3, \
                    TRIM(picks.t2_removed_1) AS t2_removed_1, \
                    TRIM(picks.t2_removed_2) AS t2_removed_2, \
                    TRIM(picks.t2_removed_3) AS t2_removed_3 \
                FROM picks \
                INNER JOIN players \
                    ON players.match_id = picks.match_id \
                    AND players.event_id = picks.event_id \
                INNER JOIN results \
                    ON results.match_id = picks.match_id \
                    AND results.event_id = picks.event_id \
                ORDER BY picks.date;"
        cursor.execute(stmt)
        vetoes = cursor.fetchall()
        cursor.close()

        # Transform
        for veto in vetoes:
            time_split = veto['date'].split("-")
            year = int(time_split[0])
            month = int(time_split[1])
            day = int(time_split[2])
            time_id = self.get_time_id(year, month, day)

            t1_id = self.get_team_id(veto['team_1'])
            t1_vetoes = {
                            '1': self.get_map_id(veto['t1_removed_1']),
                            '2': self.get_map_id(veto['t1_removed_2']),
                            '3': self.get_map_id(veto['t1_removed_3'])
                         }

            t2_id = self.get_team_id(veto['team_2'])
            t2_vetoes = {
                            '1': self.get_map_id(veto['t2_removed_1']),
                            '2': self.get_map_id(veto['t2_removed_2']),
                            '3': self.get_map_id(veto['t2_removed_3'])
                        }

            number = 1
            for map_id in t1_vetoes:
                if t1_vetoes[map_id] is not None:
                    data = {
                                'event_id': veto['event_id'],
                                'match_id': veto['match_id'],
                                'team_id': t1_id,
                                'map_id': t1_vetoes[map_id],
                                'time_id': time_id,
                                'number': number
                            }
                    number += 1
                    self.vetoes.append(data)

            number = 1
            for map_id in t2_vetoes:
                if t2_vetoes[map_id] is not None:
                    data = {
                                'event_id': veto['event_id'],
                                'match_id': veto['match_id'],
                                'team_id': t2_id,
                                'map_id': t2_vetoes[map_id],
                                'time_id': time_id,
                                'number': number
                            }
                    number += 1
                    self.vetoes.append(data)

    def load_vetoes(self):
        self.report_quantity(len(self.vetoes), "vetoes")
        self.open_connection()
        cursor = self.dw.cursor()
        for veto in self.vetoes:
            stmt = "INSERT INTO vetoes_fact (event_id, match_id, team_id, de_map_id, time_id, number)" \
                   "VALUES (%s, %s, %s, %s, %s, %s)"
            data = (veto['event_id'], veto['match_id'], veto['team_id'], veto['map_id'], veto['time_id'], veto['number'])
            cursor.execute(stmt, data)
            self.dw.commit()
        cursor.close()

    def testing(self):
        self.open_connection()

    ####################################################################
    ######################## SCRAPPER METHODS ##########################
    ####################################################################
    # def scrapper(self):
    #     print("Scrapping informations from HLTV...")
    #     for event in self.events:
    #         match_id, match_stars, event_lan, event_stars = scrapper.scrap_all(event['id'])
    #         self.dict_matches[match_id] = match_stars
    #         self.dict_events[event['id']] = [event_lan, event_stars]
    #     with open('matches.json', 'w') as fp:
    #         json.dump(self.dict_matches, fp)
    #     with open('events.json', 'w') as fp:
    #         json.dump(self.dict_events, fp)
    #     return dict

    ####################################################################
    ############### AUXILIARY OBJECT RELATED METHODS ###################
    ####################################################################
    def get_time_id(self, year, month, day):
        self.open_connection()
        cursor = self.dw.cursor(dictionary=True)
        stmt = "SELECT id FROM time \
                    WHERE year = {} \
                    AND month = {} \
                    AND DAY = {}".format(year, month, day)
        cursor.execute(stmt)
        time = cursor.fetchone()
        cursor.close()
        return time['id']

    def get_team_id(self, name):
        self.open_connection()
        cursor = self.dw.cursor(dictionary=True)
        query = 'SELECT id FROM team WHERE name = "{}"'.format(name)
        cursor.execute(query)
        team = cursor.fetchone()
        cursor.close()
        return team['id']

    def get_map_id(self, name):
        for map in self.maps:
            if map[1] == name:
                return map[0]

    def get_match_tier(self, rank_1, rank_2):
        rank_avg = (rank_1 + rank_2) / 2
        if rank_avg < 11:
            return 1
        elif 11 <= rank_avg < 21:
            return 2
        elif 21 <= rank_avg < 31:
            return 3
        elif 31 <= rank_avg < 41:
            return 4
        else:
            return 5

    def get_event_tier(self, event_id, cursor):
        query = 'SELECT AVG(match.tier) as tier \
                FROM `match` \
                INNER JOIN vetoes_fact as vf on `match`.id = vf.match_id \
                WHERE vf.event_id = {}'.format(event_id)
        cursor.execute(query)
        rank_avg = cursor.fetchone()
        return rank_avg['tier']

    # def make_dict(self):
    #     self.open_connection()
    #     cursor = self.db.cursor(dictionary=True)
    #     query = f'SELECT id, lan, tier FROM events'
    #     cursor.execute(query)
    #     events = cursor.fetchall()
    #     for event in events:
    #         self.dict_events[event['id']] = [event['lan'], event['tier']]
    #     with open('events.json', 'w') as fp:
    #         json.dump(self.dict_events, fp)


    ####################################################################
    #################### AUXILIARY STATCIC METHODS #####################
    ####################################################################
    @staticmethod
    def report_quantity(qntty, object_name):
        print("Loading {} {}...".format(qntty, object_name))

    @staticmethod
    def check_semester(month):
        if 1 >= month <= 6:
            return 1
        else:
            return 2

    @staticmethod
    def check_quarter(month):
        if 1 >= month <= 3:
            return 1
        elif 5 >= month <= 7:
            return 2
        elif 6 >= month <= 8:
            return 3
        else:
            return 4

    @staticmethod
    def check_week_of_month(day):
        if 1 >= day <= 7:
            return 1
        elif 8 >= day <= 15:
            return 2
        elif 16 >= day <= 23:
            return 3
        else:
            return 4

    @staticmethod
    def check_weekend(year, month, day):
        x = dt.datetime(year, month, day).weekday()
        if x < 5:
            return 0
        else:
            return 1