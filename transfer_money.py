# coding:utf8  #别忘了设置python编码
import sys
import MySQLdb
 
class TransferMoney(object):
    def __init__(self,con):
        self.con=con
    
    def check_account(self, transfers):
        cursor=self.con.cursor()
        try:
            sql="select * from user where _id=%s" % transfers
            print '查询语句:'+sql
            cursor.execute(sql)
            rs=cursor.fetchall();
            if len(rs)!=1:
                raise Exception("查无此人")
        finally:
            cursor.close();
        
    def has_enough_momey(self,transfers, money):
        cursor=self.con.cursor()
        try:
            sql="select _money from user where _id=%s and _money>%s" % (transfers,money)
            print '余额语句:'+sql
            cursor.execute(sql)
            rs=cursor.fetchall();
            if len(rs)!=1:
                raise Exception("余额不足")
        finally:
            cursor.close();
    
    def reduce_money(self,transfers,money):
        cursor=self.con.cursor()
        try:
            sql="update user set  _money=_money-%s where _id=%s" % (money,transfers)
            print '转账语句:'+sql
            cursor.execute(sql)
            rs=cursor.rowcount;
            if rs!=1:
                raise Exception("转账失败")
        finally:
            cursor.close();
    
    def add_money(self, receives, money):
        cursor=self.con.cursor()
        try:
            sql="update user set  _money=_money+%s where _id=%s" % (money,receives)#这里多个参数需要加括号
            print '转账语句:'+sql
            cursor.execute(sql)
            rs=cursor.rowcount;#这里需要使用rowcount获取被改变的行数，而不是fetch结果集
            if rs!=1:
                raise Exception("加钱失败")
        finally:
            cursor.close();
    
    def transfer(self,transfers,receives,money):
        try:
            self.check_account(transfers)
            self.check_account(receives)
            self.has_enough_momey(transfers,money)
            self.reduce_money(transfers,money)
            self.add_money(receives,money)
            self.con.commit()
        except Exception as e:
            raise e
            self.con.rollback()
 
if __name__=='__main__':
    transfers=sys.argv[1];
    receivsys=sys.argv[2];
    money=sys.argv[3];
    con=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='root',db='test',charset='utf8')
    tr_money=TransferMoney(con) 
    try :
        tr_money.transfer(transfers,receivsys,money)
    except Exception as e:
        print '转账出错：'+str(e)
    finally:
        con.close()