# coding:utf8  #����������python����
import sys
import MySQLdb
 
class TransferMoney(object):
    def __init__(self,con):
        self.con=con
    
    def check_account(self, transfers):
        cursor=self.con.cursor()
        try:
            sql="select * from user where _id=%s" % transfers
            print '��ѯ���:'+sql
            cursor.execute(sql)
            rs=cursor.fetchall();
            if len(rs)!=1:
                raise Exception("���޴���")
        finally:
            cursor.close();
        
    def has_enough_momey(self,transfers, money):
        cursor=self.con.cursor()
        try:
            sql="select _money from user where _id=%s and _money>%s" % (transfers,money)
            print '������:'+sql
            cursor.execute(sql)
            rs=cursor.fetchall();
            if len(rs)!=1:
                raise Exception("����")
        finally:
            cursor.close();
    
    def reduce_money(self,transfers,money):
        cursor=self.con.cursor()
        try:
            sql="update user set  _money=_money-%s where _id=%s" % (money,transfers)
            print 'ת�����:'+sql
            cursor.execute(sql)
            rs=cursor.rowcount;
            if rs!=1:
                raise Exception("ת��ʧ��")
        finally:
            cursor.close();
    
    def add_money(self, receives, money):
        cursor=self.con.cursor()
        try:
            sql="update user set  _money=_money+%s where _id=%s" % (money,receives)#������������Ҫ������
            print 'ת�����:'+sql
            cursor.execute(sql)
            rs=cursor.rowcount;#������Ҫʹ��rowcount��ȡ���ı��������������fetch�����
            if rs!=1:
                raise Exception("��Ǯʧ��")
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
        print 'ת�˳���'+str(e)
    finally:
        con.close()