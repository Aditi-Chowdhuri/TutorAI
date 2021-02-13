import sqlite3

# Insert new course in Database
def add_new_data(COURSE_ID):
    conn = sqlite3.connect('Server_side.db')
    try:
        conn.execute(r"INSERT INTO FEEDBACK (COURSE_ID, UNAME, RATING) VALUES ('%s', 'NULL', 0)" %COURSE_ID)
        s = 'Data added Successfully'
    except:
        s = 'Failed to register'

    conn.commit()
    conn.close()
    return s

# Insert new rating in Database
def add_new_rating(COURSE_ID, UNAME, RATING):
    conn = sqlite3.connect('Server_side.db')
    conn.execute("INSERT INTO FEEDBACK (COURSE_ID, UNAME, RATING) VALUES (?, ?, ?)", (COURSE_ID, UNAME, RATING))
    s = 'Data added Successfully'

    conn.commit()
    conn.close()
    return s

# read Values from database
def read_db(COURSE_ID):
    conn = sqlite3.connect('Server_side.db')
    avg_rat = conn.execute("SELECT avg(RATING) FROM FEEDBACK WHERE COURSE_ID = ?", COURSE_ID)

    cursor = conn.execute("SELECT * FROM FEEDBACK")
    data = cursor.fetchall()
    uname_arr = []
    for record in data:
        u = record[0]
        if u == COURSE_ID:
            uname_arr.append(record[1])

    conn.close()
    return [avg_rat, uname_arr]

def del_course(COURSE_ID):
    conn = sqlite3.connect('Server_side.db')
    conn.execute(" DELETE FROM FEEDBACK WHERE COURSE_ID=?", (COURSE_ID,))
    conn.commit()
    conn.close()
    return "deleted"