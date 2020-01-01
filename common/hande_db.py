"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/7 18:55
E-mail  : 506615839@qq.com
File    : hande_db.py
============================
"""
import pymysql
from common.read_conf import conf


class HandDB:
    def __init__(self):
        # 连接数据库
        self.con = pymysql.connect(
            host=conf.get('mysql_db', 'host'),
            user=conf.get('mysql_db', 'user'),
            password=conf.get('mysql_db', 'password'),
            port=conf.getint('mysql_db', 'port'),
            charset='utf8'
        )
        # 创建游标
        self.cur = self.con.cursor()

    def get_one(self, sql):
        '''获取查询到的第一条数据'''
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchone()

    def get_all(self, sql):
        '''获取查询到的数据集'''
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def get_count(self, sql):
        '''获取sql语句查询到的所有数据'''
        self.con.commit()
        res = self.cur.execute(sql)
        return res

    def close(self):
        # 关闭游标对象
        self.cur.close()
        # 断开连接
        self.con.close()


if __name__ == '__main__':
    from common.hander_data import TestData,replace_data
    db = HandDB()
    sql = 'select id from fybanks_hfjyuan.dynamic_info where id not in (select dynamic_id from fybanks_hfjyuan.dynamic_comment where state=1  order by id desc) and status=3 and state=1 order by id desc'
    id = db.get_one(sql)[0]
    setattr(TestData, 'id', str(id))
    sql1 = 'select * from fybanks_hfjyuan.dynamic_comment where dynamic_id=#id#'
    sql1=replace_data(sql1)
    print(sql1,type(sql1))

