from . import common, database


@common.main
def main():
    with database.Database() as db:
        print(db.get_sleep_period())
