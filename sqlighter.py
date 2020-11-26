import sqlite3
import os

class SQLighter:

	def __init__(self, database):
		self.connection = sqlite3.connect(database)
		self.cursor = self.connection.cursor()

	def create_base(self):
		with self.connection:
			self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_info (
								id		 INTEGER NOT NULL PRIMARY KEY,
								user_id	  INTEGER)'''
							)
			self.cursor.execute('''CREATE TABLE IF NOT EXISTS cotegory_filter (
								id		 INTEGER NOT NULL PRIMARY KEY,
								name     STRING,
								filter    STRING,
								chat_id   INTEGER)''')

	def add_db(self, user_id, name):
		with self.connection:
			self.cursor.execute("INSERT INTO `user_info` (`user_id`) VALUES(?)", (user_id,))

	def subscriber_exists(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			return bool(len(result))

	def subscriber_cotegory(self, cotegory):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `cotegory_filter` WHERE `name` = ?', (cotegory,)).fetchall()
			return bool(len(result))

	def add_cotegory(self, cotegory, filterr):
		with self.connection:
			self.cursor.execute("INSERT INTO `cotegory_filter` (`name`,`filter`,`chat_id`) VALUES(?,?,?)", (cotegory,filterr,0))

	def dekete_cotegory(self, cotegory):
		with self.connection:
			self.cursor.execute(f"DELETE FROM cotegory_filter WHERE name = '" + cotegory+"'")

	def get_filter(self):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `cotegory_filter`').fetchall()
			p = []
			for i in result:
				id,name,filter,chat_id = i
				p.append(filter)
			return p

	def chat_id(self, chat_id, filter):
		with self.connection:
			self.cursor.execute(f"UPDATE `cotegory_filter` SET `chat_id` = ? WHERE `filter` = ?", (chat_id, filter))

	def get_cotegory(self):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `cotegory_filter`').fetchall()
			p = []
			for i in result:
				id,name,filter,chat_id = i
				p.append(name)
			return p

	def channe_id(self, cotegory):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `cotegory_filter` WHERE `name` = ?', (cotegory,)).fetchall()[0]
			return result[3]

	def update_cotegory(self, cotegory, filter):
		with self.connection:
			self.cursor.execute(f"UPDATE `cotegory_filter` SET `filter` = ? WHERE `name` = ?", (filter, cotegory))
			self.cursor.execute(f"UPDATE `cotegory_filter` SET `chat_id` = ? WHERE `name` = ?", (0, cotegory))



	


