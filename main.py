from ETL import StagingArea
import database_configs
import time


def main(**kwargs):
    sa = StagingArea(database_configs.niko) if kwargs['DATABASE_CONFIG'] is 1 else StagingArea(database_configs.lucas)

    if kwargs['SCRATCH']:
        # Clean data warehouse and exit program
        sa.drop_tables()
        # Create tables
        sa.create_tables()
        exit(1)

    # Maps ETL
    # sa.populate_maps()

    # # Events ETL
    # start_time = time.time()
    # sa.export_and_transform_events()
    # sa.load_events()
    # if kwargs['DEBUG']:
    #     print('Finished EVENTS ETL with success in: ', round(time.time() - start_time, 2), ' seconds')
    #
    # # Players ETL
    # start_time = time.time()
    # sa.export_and_transform_players()
    # sa.load_players()
    # if kwargs['DEBUG']:
    #     print('Finished PLAYERS ETL with success in: ', round(time.time() - start_time, 2), ' seconds')
    #
    # # Matches ETL
    # start_time = time.time()
    # sa.export_and_transform_matches()
    # sa.load_matches()
    # if kwargs['DEBUG']:
    #     print('Finished MATCHES ETL with success in: ', round(time.time() - start_time, 2), ' seconds')

    # # Teams ETL
    # start_time = time.time()
    # sa.export_and_transform_teams()
    # sa.load_teams()
    # if kwargs['DEBUG']:
    #     print('Finished TEAMS ETL with success in: ', round(time.time() - start_time, 2), ' seconds')

    # # Time ETL
    # start_time = time.time()
    # sa.export_and_transform_time()
    # sa.load_times()
    # if kwargs['DEBUG']:
    #     print('Finished TIMES ETL with success in: ', round(time.time() - start_time, 2), ' seconds')

    # # Performance ETL
    # start_time = time.time()
    # sa.export_and_transform_performance()
    # sa.load_performances()
    # if kwargs['DEBUG']:
    #     print('Finished PERFORMANCES ETL with success in: ', round(time.time() - start_time, 2), ' seconds')

    # Veto ETL
    start_time = time.time()
    sa.export_and_transform_veto()
    sa.load_vetoes()
    if kwargs['DEBUG']:
        print('Finished VETOES ETL with success in: ', round(time.time() - start_time, 2), ' seconds')


# DATABASE_CONFIG: 1. Niko | 2.Lucas
# DEBUG: True | False  (to print  ETL process duration time and number of instances on loading)
# SCRATCH: True | False (start a project from zero)
main(DATABASE_CONFIG=1, DEBUG=True, SCRATCH=False)
