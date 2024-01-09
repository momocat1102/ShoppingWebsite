#!#!/usr/local/bin/python

import mysql.connector


try: 
	conn = mysql.connector.connect(
		user="root",
		password="",
		host="localhost",
		port=3306,
		database="SE"
	)

except mysql.connector.Error as e:
	print(e)
	print("Error connecting to DB")
	exit(1)
    
cur = conn.cursor()


