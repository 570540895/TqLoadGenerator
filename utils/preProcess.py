import logging
import pandas as pd
log_file = r'logs/test.log'
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
