import logging
import pandas as pd

log_file = 'logs/test.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG)
log = logging.getLogger(__name__)


def sort_csv_file(csv_file, sorted_csv_file):
    try:
        df = pd.read_csv(csv_file)
        assert df.shape[0] >= 2
        df = df.sort_values('createDate', ascending=True)
        df = df.reset_index(drop=True)
        df.to_csv(sorted_csv_file, index=False)
    except Exception as e:
        log.error(e)
        print(e)
        raise


def get_min_duration(sorted_csv_file):
    min_duration = 10000
    try:
        df = pd.read_csv(sorted_csv_file)
        for _, row in df.iterrows():
            min_duration = min(min_duration, row['exec_duration'])
    except Exception as e:
        log.error(e)
        raise
    return min_duration
