import sys
import sqlite3
import datetime
from jenkins import Jenkins, JenkinsException


def connect_db(name):
    return sqlite3.connect(name)


def jenkin_server_instance(url, username, password):
    print("Connecting to jenkin instance \n")
    try:
        server = Jenkins(url, username, password)
        user = server.get_whoami()
        version = server.get_version()
        print("Hello %s from Jenkins %s \n" % (user["fullName"], version))
        return server
    except JenkinsException:
        print("Authentication Error: Invalid Password/Token for user \n")
    return


def get_jobs_details(server):
    print("Getting insatnce jobs \n")
    jobs = server.get_jobs()
    print("%s jobs fetched... \n" % (len(jobs)))
    job_data = []
    for job in jobs:
        name, status = job["fullname"], job["color"]
        time = datetime.datetime.now()
        job_data.append(
            {"name": name, "status": status, "datetime": datetime.datetime.now()}
        )
    return job_data


def db_setup(name):
    conn = connect_db(name)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """CREATE TABLE jenkin_jobs
                    (job, status, datetime)"""
        )
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()


def store_data(db_name, data):
    conn = connect_db(db_name)
    cursor = conn.cursor()
    scripts = []
    print("Storing Job records into database \n")
    for job in data:
        result = jobExistInDB(cursor, job["name"])
        if result.fetchone():
            scripts.append(
                """
                UPDATE jenkin_jobs 
                SET status = '%s', datetime = '%s'
                WHERE job = '%s'
            """
                % (job["status"], job["datetime"], job["name"])
            )
        else:
            scripts.append(
                "INSERT INTO jenkin_jobs (job, status, datetime) VALUES ('%s', '%s', '%s')"
                % (job["name"], job["status"], job["datetime"])
            )

    cursor.executescript(""";""".join(scripts))
    print("Process completed \n")

    conn.commit()
    conn.close()


def jobExistInDB(cursor, name):
    result = cursor.execute("select * from jenkin_jobs where job = '%s'" % name)
    return result


if __name__ == "__main__":
    db_name = "jenkins.db"
    db_setup(db_name)
    server = jenkin_server_instance("http://127.0.0.1:8080", "jen_1", "Passme@123")
    if server:
        data = get_jobs_details(server)
        store_data(db_name, data)

