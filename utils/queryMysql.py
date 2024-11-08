import pymysql
import logging

log_file = r'logs/test.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG)
log = logging.getLogger(__name__)


def query_mysql(**kwargs):
    db = pymysql.connections.Connection(**kwargs)
    cur = db.cursor()
    sql = "select j.uuid, j.name, g.startTime from job_info as j " \
          "left join gpu_consumption_info as g on j.name = g.name where g.status = 'running';"
    data = tuple()
    try:
        cur.execute(sql)
        data = cur.fetchall()
    except Exception as e:
        log.error(e)
    cur.close()
    db.close()
    return data
