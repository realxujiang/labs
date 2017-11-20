#!/usr/bin/env python
# coding: utf-8
__author__ = 'whoami'
import commands,logging

def is_num_by_except(num):
        try:
                int(num)
                return True
        except ValueError:
                # print "%s ValueError" % num
                return False

def db_settings():
	# db info format --> id,db_username,jdbc_info,db_passswd
	db_info = {1:'PU_WEB,jdbc:oracle:thin:@135.33.6.58:1521:orcl,tydic', 
		   2:'PU_AT,jdbc:oracle:thin:@135.33.6.58:1521:orcl,tydic',
		   3:'PU_IT,jdbc:oracle:thin:@135.33.6.58:1521:orcl,tydic',
		   2:'mysql,com.mysql.jdbc.Driver,admin123'}

	return db_info

def database_info():
	lines = db_settings()
	print 'SQOOP:Oracle jdbc connect info...'
	for k,v in lines.items():
		print '		',k,v

def get_matche_conn(db):

	while 1:
		number = raw_input("Please input number: ")
		if is_num_by_except(number):
			con = db.get(int(number))
			return con
			break
		else:
			logging.error(' Input types Error,please input number types... ')
			continue

def is_sqoop_split():
	is_split = raw_input("Do you want support sqoop split [y/n] (n)?")
	if 'y' is is_split:
		return True
	else:
		return False

def sqoop_split_column():
	  while 1:
		sqoop_split_cloumn = raw_input("Please input sqoop split cloumn,cloumn type is integer: ")
	        number = raw_input("Please input sqoop split map concurrent execution number: ")
                
		if is_num_by_except(number):
                        return sqoop_split_cloumn,number
                        break
                else:
                        logging.error(' Input types Error,please input number types... ')
                        continue

def delete_hive_table(table_name):
	command = "hive -e 'drop table if exists %s'" %(table_name)
	logging.warn(' drop table if exists %s ... ' %table_name)
	status,result = commands.getstatusoutput(command)

	if status == 0:
		logging.warn(result)
		logging.warn('drop hive table success... '),
	else:
		logging.warn('drop hive table fail...')

def raw_table():
	rdbms_table_name = raw_input("Please input rdbms table name: ")
	
	hive_table_name = raw_input("Please input hive table name: ")
	
	return rdbms_table_name,hive_table_name

def sqoop_task_parse(is_split,rdbms_table_name,hive_table_name,rdbms_username,rdbms_jdbc,rdbms_passwd):
 	if is_split:
		split_column,split_m=sqoop_split_column()
		sqoop_import = 'sqoop import  -D mapreduce.job.queuename=mapred --connect %s --username %s --password %s --table %s --fields-terminated-by "\\t" --lines-terminated-by "\\n" --hive-import --create-hive-table --hive-table %s --compression-codec "org.apache.hadoop.io.compress.SnappyCodec" -m %s --split-by %s' %(rdbms_jdbc,rdbms_username,rdbms_passwd,rdbms_table_name,hive_table_name,split_m,split_column) + " --null-string '\\\N' --null-non-string '\\\N'"
		return sqoop_import
	else:
		sqoop_import = 'sqoop import  -D mapreduce.job.queuename=mapred --connect %s --username %s --password %s --table %s --fields-terminated-by "\\t" --lines-terminated-by "\\n" --hive-import --create-hive-table --hive-table %s --compression-codec "org.apache.hadoop.io.compress.SnappyCodec" -m 1' %(rdbms_jdbc,rdbms_username,rdbms_passwd,rdbms_table_name,hive_table_name) + " --null-string '\\\N' --null-non-string '\\\N'"
		return sqoop_import

def sqoop_task(sqoop_import):
        logging.warn('sqoop import rdbms to hive ...')
        status,result = commands.getstatusoutput(sqoop_import)

        if status == 0:
                logging.warn(result)
                logging.warn('sqoop import rdbms to hive success... '),
        else:
                logging.warn('sqoop import rdbms to hive fail...')	



def task_execute(hive_table_name,sqoop_import):
	delete_hive_table(hive_table_name)
	sqoop_task(sqoop_import)

def sqoop_main():
	database_info()
	db = db_settings()
	conn = get_matche_conn(db).strip().split(',')
	rdbms_table_name,hive_table_name = raw_table()
	is_split = is_sqoop_split() 
	sqoop_import = sqoop_task_parse(is_split,rdbms_table_name,hive_table_name,conn[0],conn[1],conn[2])
	task_execute(hive_table_name,sqoop_import)

sqoop_main()
