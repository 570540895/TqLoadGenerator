import pymysql
import logging

log_file = r'logs/test.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG)
log = logging.getLogger(__name__)


def query_mysql(**kwargs):
    db = pymysql.connections.Connection(**kwargs)
    cur = db.cursor()
    sql = "select uuid, name, startTime from gpu_consumption_info where status = 'running';"
    try:
        cur.execute(sql)
        data = cur.fetchall()
    except Exception as e:
        log.error(e)
    cur.close()
    db.close()
    return data
