from ETL import StagingArea
import database_configs
import time

# 1. Niko | 2.Lucas
CONFIG = 1
DEBUG = True
SCRATCH = False


def main(new_project=True):

    sa = StagingArea(database_configs.niko) if CONFIG is 1 else StagingArea(database_configs.lucas)

    if SCRATCH:
        # Clean data warehouse and exit program
        sa.drop_tables()
        # Create tables
        sa.create_tables()
        exit(1)

    # Maps ETL
    # sa.populate_maps()

    # Events ETL
    # start_time = time.time()
    # sa.export_and_transform_events()
    # sa.load_events()
    # if DEBUG:
    #     print('Finished events ETL with success in: ', round(time.time() - start_time, 2), ' seconds')

    # Players ETL
    # start_time = time.time()
    # sa.export_and_transform_players()
    # sa.load_players()
    # if DEBUG:
    #     print('Finished players ETL with success in: ', round(time.time() - start_time, 2), ' seconds')

    # Matches ETL
    # start_time = time.time()
    # sa.export_and_transform_matches()
    # sa.load_matches()
    # if DEBUG:
    #     print('Finished Matches ETL with success in: ', round(time.time() - start_time, 2), ' seconds')

    # # Teams ETL
    # start_time = time.time()
    # sa.export_and_transform_teams()
    # sa.load_teams()
    # if DEBUG:
    #     print('Finished Teams ETL with success in: ', round(time.time() - start_time, 2), ' seconds')

    # Time ETL
    # start_time = time.time()
    # sa.export_and_transform_time()
    # sa.load_times()
    # if DEBUG:
    #     print('Finished Time ETL with success in: ', round(time.time() - start_time, 2), ' seconds')

    # Performance ETL
    start_time = time.time()
    sa.export_and_transform_performance()
    sa.load_performances()
    if DEBUG:
        print('Finished performances ETL with success in: ', round(time.time() - start_time, 2), ' seconds')

main()
