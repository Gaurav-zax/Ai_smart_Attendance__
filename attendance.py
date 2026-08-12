from datetime import datetime
import sqlite3
import os


# ==================================================
# DATABASE PATH
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


DATABASE = os.path.join(
    BASE_DIR,
    "attendance.db"
)


# ==================================================
# MARK ATTENDANCE
# ==================================================

def mark_attendance(student_id, name):

    conn = sqlite3.connect(
        DATABASE
    )

    cursor = conn.cursor()


    now = datetime.now()


    date = now.strftime(
        "%Y-%m-%d"
    )


    time = now.strftime(
        "%H:%M:%S"
    )


    # ----------------------------------------------
    # CHECK DUPLICATE ATTENDANCE
    # ----------------------------------------------

    cursor.execute(
        """
        SELECT *
        FROM attendance

        WHERE
            date = ?
            AND student_id = ?
        """,

        (
            date,
            student_id
        )
    )


    result = cursor.fetchone()


    if result:

        print(
            "Attendance Already Marked:",
            name
        )


        conn.close()


        return


    # ----------------------------------------------
    # INSERT NEW ATTENDANCE
    # ----------------------------------------------

    cursor.execute(
        """
        INSERT INTO attendance
        (
            date,
            time,
            student_id,
            student_name
        )

        VALUES
        (
            ?,
            ?,
            ?,
            ?
        )
        """,

        (
            date,
            time,
            student_id,
            name
        )
    )


    conn.commit()


    conn.close()


    print(
        "Attendance Marked:",
        name
    )