import pymysql

import SQL_Connection as sqlhandler

def increaseMessageCounter(author, authorID) -> bool:
	"""
	Increases the message counter for the given user
	:param author: The Discord name, e.g. Paddy#4547
	:param authorID: The Discord ID, e.g. a very long number as 12343582334645764575
	:return: If it was successful
	"""
	conn = sqlhandler.getConnection()
	cur = conn.cursor()
	getUserQuery = """SELECT userID, numberOfMessagesSent FROM users WHERE discordID = %s"""
	cur.execute(getUserQuery, (authorID,))
	userSqlRow = cur.fetchall()
	conn.commit()

	if cur.rowcount == 1:
		userID = userSqlRow[0][0]
		numberOfMessagesSent = userSqlRow[0][1]
		updateUserQuery = """UPDATE users SET numberOfMessagesSent = %s, name = %s WHERE userID = %s"""
		cur.execute(updateUserQuery, (int(numberOfMessagesSent)+1, str(author), str(userID)))
		conn.commit()
	else:
		insertUserQuery = """INSERT INTO users (name, discordID, numberOfMessagesSent) VALUES (%s, %s, %s)"""
		cur.execute(insertUserQuery, (str(author), str(authorID), 1))
		conn.commit()
	cur.close()
	return True

