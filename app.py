import os.path
import mysql.connector
from flask import Flask, render_template, send_from_directory, Response


def get_connection():
    connection = mysql.connector.connect(
        host="db",
        user="root",
        password="rootpassword",
        database="mydatabase",
        connection_timeout=600
    )
    return connection


con = get_connection()
cur = con.cursor()


app = Flask(__name__)


def execute_query(con, cur, query, params):
    try:
        cur.execute(query, params)
    except mysql.connector.Error as err:
        if err.errno in (
                mysql.connector.errorcode.CR_SERVER_LOST,
                mysql.connector.errorcode.CR_SERVER_GONE_ERROR,
                mysql.connector.errors.InternalError,
                mysql.connector.errors.DatabaseError
        ):
            print("Reconnecting to the database...")
            new_con = get_connection()
            new_con.reconnect(attempts=20, delay=5)
            new_cur = new_con.cursor()
            try:
                new_cur.execute(query, params)
            except mysql.connector.Error as err:
                print(f"Error during retry: {err}")
                raise
        else:
            raise


@app.route('/photos/<filename>')
def photos_directory(filename):
    return send_from_directory('photos', filename)


@app.route('/img/<int:skill_id>')
def img(skill_id):
    query = "SELECT img FROM skills WHERE id = %s"
    params = (skill_id,)
    execute_query(con, cur, query, params)
    img_data = cur.fetchone()
    if img_data:
        return Response(img_data[0], mimetype='image/png')
    return "Image not found", 404


@app.route('/certification/<int:skill_id>')
def certification(skill_id):
    query = "SELECT certification FROM skills WHERE id = %s"
    params = (skill_id,)
    execute_query(con, cur, query, params)
    cert_data = cur.fetchone()
    if cert_data:
        return Response(cert_data[0], mimetype='image/png')
    return "Certification not found", 404


@app.route('/')
def index():
    con = get_connection()
    try:
        cur = con.cursor()

        skills_query = "SELECT * FROM skills"
        projects_query = "SELECT * FROM projects"
        params = ()
        execute_query(con, cur, skills_query, params)
        skills = cur.fetchall()
        execute_query(con, cur, projects_query, params)
        projects = cur.fetchall()
        return render_template('index.html', skills=skills, projects=projects)
    finally:
        cur.close()
        con.close()


def upload_skill_to_db(image_path, title, description, certification=None):
    con = get_connection()
    with open(image_path, 'rb') as file:
        img_data = file.read()

    cur.execute("""
        INSERT INTO skills (title, img, description, certification)
        VALUES (%s, %s, %s, %s)
    """, (title, img_data, description, certification))
    con.commit()


def upload_project_to_db(title, link, description):
    con = get_connection()
    cur.execute("""
        INSERT INTO projects (title, link, description)
        VALUES (%s, %s, %s)
        """, (title, link, description))
    con.commit()



# cur.execute("""drop table if exists skills """)
# con.commit()
# cur.execute(
#     """CREATE TABLE IF NOT EXISTS skills (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(255) NOT NULL,
#     img BLOB,
#     description VARCHAR(10000) NOT NULL,
#     certification BLOB
#     )""")
# con.commit()
#
# cpp_title = 'c++'
# cpp_description = """
#   I started my journey in the programming world by studying
# C++ in the University of Georgia. I learned the fundamentals
# of, and object oriented programming in this very language
# respectively in the first and second semesters of my studies.
# In this language I have created a simple interactive game
# implementing the mechanics of luck.
# """
# cpp_img_path = 'c++.png'
#
# excel_title = 'microsoft excel'
# excel_description = """
#     My university has provided me with the ability and knowledge to receive a Microsoft certificate, which confirms
#     the ability to be recognized as a Microsoft Office Specialist in Excel.
# """
# excel_img_path = 'microsoft excel.png'
#
# java_title = 'java'
# java_description = """
#     Java is another programming language in my arsenal. I have experience with: client-server socket-based
#     projects, javafx applications and other appliances.
# """
# java_img_path = 'java.png'
#
# htmlncss_title = 'html5&css3'
# htmlncss_description = """
#     Creating webpages is another skill that I possess. Multiple websites and projects, including this very CV,
#     are a proof of my knowledge.
# """
# htmlncss_img_path = 'html&css.png'
#
#
# bootstrap_title = 'bootstrap'
# bootstrap_description = """
#     My web skills also include the Bootstrap framework. I have sufficient knowledge to tweak the Bootstrap blueprints
#     to be shaped around specific needs.
# """
# bootstrap_img_path = 'bootstrap.png'
#
# javascript_title = 'javascript'
# javascript_description = """
#     Of course, a webpage can certainly use some JavaScript, which is yet another programming language in my capabilities.
# """
# javascript_img_path = 'javascript.png'
#
# mssqlnmysql_title = 'mysql&mssql'
# mssqlnmysql_description = """
#     I have quite the experience of working with databases. I have used the relational database
#     management system and utilized SQL for operating data in a number of my projects.
# """
# mssqlnmysql_img_path = 'mssql&mysql.png'
#
# spring_title = 'springboot'
# spring_description = """
#     Another programming language that I have experience with working is Spring. At my university I have created
#     a webpage which utilizes the SpringBoot
# """
# spring_img_path = 'spring.png'
#
# python_title = 'python'
# python_description = """
#     Python is a programming language that I have spent time with most. After having mastered the syntax and gone down
#     the scientific programming route utilizing freeCodeCamp, I studied Python additionally at my university, having
#     created an AI model. This very CV was created using Python and the Flask framework.
# """
# python_img_path = 'python.png'
#
#
# upload_skill_to_db(os.path.join('photos', cpp_img_path), cpp_title.title(), cpp_description, )
# upload_skill_to_db(os.path.join('photos', java_img_path), java_title.title(), java_description, )
# upload_skill_to_db(os.path.join('photos', python_img_path), python_title.title(), python_description, )
# upload_skill_to_db(os.path.join('photos', spring_img_path), spring_title.title(), spring_description, )
# upload_skill_to_db(os.path.join('photos', mssqlnmysql_img_path), mssqlnmysql_title.title(), mssqlnmysql_description, )
# upload_skill_to_db(os.path.join('photos', javascript_img_path), javascript_title.title(), javascript_description, )
# upload_skill_to_db(os.path.join('photos', excel_img_path), excel_title.title(), excel_description, )
# upload_skill_to_db(os.path.join('photos', htmlncss_img_path), htmlncss_title.title(), htmlncss_description, )
# upload_skill_to_db(os.path.join('photos', bootstrap_img_path), bootstrap_title.title(), bootstrap_description, )
# con.commit()
#
#
# cur.execute("""drop table if exists projects """)
# con.commit()
# cur.execute(
#     """CREATE TABLE IF NOT EXISTS projects (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(255) NOT NULL,
#     link VARCHAR(200) NOT NULL,
#     description VARCHAR(10000) NOT NULL
#     )""")
#
# probability_calculator_title = "Probability Calculator"
# probability_calculator_link = "https://github.com/GiorgiKarchiladze/Probability-Calculator"
# probability_calculator_description = ("Calculates the probability of a drawn set of balls drawn matching the desired"
#                                       " set of balls on a large scale of experiments instead of the mathematical way.")
#
#
# vectors_title = "Vectors"
# vectors_link = "https://github.com/GiorgiKarchiladze/Vectors"
# vectors_description = ("Vector operations, summing, subtracting, multiplication (cross-multiplication for three-"
#                        "dimensional vectors). Functions to check if one is equal, greater or less than another vector")
#
# projectile_trajectory_calculator_title = "Projectile Trajectory Calculator"
# projectile_trajectory_calculator_link = "https://github.com/GiorgiKarchiladze/Projectile-trajectory-calculator"
# projectile_trajectory_calculator_description = ("Given the initial speed, height and angle, calculates and displays an "
#                                                 "approximate graph of the trajectory")
#
# upload_project_to_db(probability_calculator_title, probability_calculator_link, probability_calculator_description)
# upload_project_to_db(vectors_title, vectors_link, vectors_description)
# upload_project_to_db(projectile_trajectory_calculator_title, projectile_trajectory_calculator_link,
#                      projectile_trajectory_calculator_description)
#
#
#
# _title = ""
# _link = ""
# _description = ""


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host="0.0.0.0", port=port)


#
# import os.path
# import mysql.connector
# from flask import Flask, render_template, send_from_directory, Response
#
# con = mysql.connector.connect(host="db",
#                               user="root",
#                               password="rootpassword",
#                               database="mydatabase")
#
# cur = con.cursor()
#
# app = Flask(__name__)
#
#
# def execute_query(query, params):
#     try:
#         cur.execute(query, params)
#     except mysql.connector.Error as err:
#         if err.errno in (mysql.connector.errorcode.CR_SERVER_LOST, mysql.connector.errorcode.CR_SERVER_GONE_ERROR,
#                          mysql.connector.errors.InternalError, mysql.connector.errors.DatabaseError):
#             con.reconnect(attempts=10, delay=1)
#             cur.execute(query, params)
#         else:
#             raise
#
#
# @app.route('/photos/<filename>')
# def photos_directory(filename):
#     return send_from_directory('photos', filename)
#
#
# @app.route('/img/<int:skill_id>')
# def img(skill_id):
#     query = "SELECT img FROM skills WHERE id = %s"
#     params = (skill_id,)
#     execute_query(query, params)
#     img_data = cur.fetchone()
#     if img_data:
#         return Response(img_data[0], mimetype='image/png')
#     return "Image not found", 404
#
#
# @app.route('/certification/<int:skill_id>')
# def certification(skill_id):
#     query = "SELECT certification FROM skills WHERE id = %s"
#     params = (skill_id,)
#     execute_query(query, params)
#     cert_data = cur.fetchone()
#     if cert_data:
#         return Response(cert_data[0], mimetype='image/png')
#     return "Certification not found", 404
#
#
# @app.route('/')
# def index():
#     skills_query = "SELECT * FROM skills"
#     projects_query = "SELECT * FROM projects"
#     params = ()
#     execute_query(skills_query, params)
#     skills = cur.fetchall()
#     execute_query(projects_query, params)
#     projects = cur.fetchall()
#     return render_template('index.html', skills=skills, projects=projects)
#
#
# def upload_skill_to_db(image_path, title, description, certification=None):
#     with open(image_path, 'rb') as file:
#         img_data = file.read()
#
#     cur.execute("""
#         INSERT INTO skills (title, img, description, certification)
#         VALUES (%s, %s, %s, %s)
#     """, (title, img_data, description, certification))
#     con.commit()
#
#
# def upload_project_to_db(title, link, description):
#     cur.execute("""
#         INSERT INTO projects (title, link, description)
#         VALUES (%s, %s, %s)
#         """, (title, link, description))
#     con.commit()
#
#
#
# cur.execute("""drop table if exists skills """)
# con.commit()
# cur.execute(
#     """CREATE TABLE IF NOT EXISTS skills (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(255) NOT NULL,
#     img BLOB,
#     description VARCHAR(10000) NOT NULL,
#     certification BLOB
#     )""")
# con.commit()
# cur.execute("""drop table if exists projects """)
# con.commit()
# cur.execute(
#     """CREATE TABLE IF NOT EXISTS projects (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(255) NOT NULL,
#     link VARCHAR(200) NOT NULL,
#     description VARCHAR(10000) NOT NULL
#     )""")
# con.commit()
#
# cpp_title = 'c++'
# cpp_description = """
#   I started my journey in the programming world by studying
# C++ in the University of Georgia. I learned the fundamentals
# of, and object oriented programming in this very language
# respectively in the first and second semesters of my studies.
# In this language I have created a simple interactive game
# implementing the mechanics of luck.
# """
# cpp_img_path = 'c++.png'
#
# excel_title = 'microsoft excel'
# excel_description = """
#     My university has provided me with the ability and knowledge to receive a Microsoft certificate, which confirms
#     the ability to be recognized as a Microsoft Office Specialist in Excel.
# """
# excel_img_path = 'microsoft excel.png'
#
# java_title = 'java'
# java_description = """
#     Java is another programming language in my arsenal. I have experience with: client-server socket-based
#     projects, javafx applications and other appliances.
# """
# java_img_path = 'java.png'
#
# htmlncss_title = 'html5&css3'
# htmlncss_description = """
#     Creating webpages is another skill that I possess. Multiple websites and projects, including this very CV,
#     are a proof of my knowledge.
# """
# htmlncss_img_path = 'html&css.png'
#
#
# bootstrap_title = 'bootstrap'
# bootstrap_description = """
#     My web skills also include the Bootstrap framework. I have sufficient knowledge to tweak the Bootstrap blueprints
#     to be shaped around specific needs.
# """
# bootstrap_img_path = 'bootstrap.png'
#
# javascript_title = 'javascript'
# javascript_description = """
#     Of course, a webpage can certainly use some JavaScript, which is yet another programming language in my capabilities.
# """
# javascript_img_path = 'javascript.png'
#
# mssqlnmysql_title = 'mysql&mssql'
# mssqlnmysql_description = """
#     I have quite the experience of working with databases. I have used the relational database
#     management system and utilized SQL for operating data in a number of my projects.
# """
# mssqlnmysql_img_path = 'mssql&mysql.png'
#
# spring_title = 'springboot'
# spring_description = """
#     Another programming language that I have experience with working is Spring. At my university I have created
#     a webpage which utilizes the SpringBoot
# """
# spring_img_path = 'spring.png'
#
# python_title = 'python'
# python_description = """
#     Python is a programming language that I have spent time with most. After having mastered the syntax and gone down
#     the scientific programming route utilizing freeCodeCamp, I studied Python additionally at my university, having
#     created an AI model. This very CV was created using Python and the Flask framework.
# """
# python_img_path = 'python.png'
#
#
# upload_skill_to_db(os.path.join('photos', cpp_img_path), cpp_title.title(), cpp_description, )
# upload_skill_to_db(os.path.join('photos', java_img_path), java_title.title(), java_description, )
# upload_skill_to_db(os.path.join('photos', python_img_path), python_title.title(), python_description, )
# upload_skill_to_db(os.path.join('photos', spring_img_path), spring_title.title(), spring_description, )
# upload_skill_to_db(os.path.join('photos', mssqlnmysql_img_path), mssqlnmysql_title.title(), mssqlnmysql_description, )
# upload_skill_to_db(os.path.join('photos', javascript_img_path), javascript_title.title(), javascript_description, )
# upload_skill_to_db(os.path.join('photos', excel_img_path), excel_title.title(), excel_description, )
# upload_skill_to_db(os.path.join('photos', htmlncss_img_path), htmlncss_title.title(), htmlncss_description, )
# upload_skill_to_db(os.path.join('photos', bootstrap_img_path), bootstrap_title.title(), bootstrap_description, )
# con.commit()
#
#
#
#
# probability_calculator_title = "Probability Calculator"
# probability_calculator_link = "https://github.com/GiorgiKarchiladze/Probability-Calculator"
# probability_calculator_description = ("Calculates the probability of a drawn set of balls drawn matching the desired"
#                                       " set of balls on a large scale of experiments instead of the mathematical way.")
#
#
# vectors_title = "Vectors"
# vectors_link = "https://github.com/GiorgiKarchiladze/Vectors"
# vectors_description = ("Vector operations, summing, subtracting, multiplication (cross-multiplication for three-"
#                        "dimensional vectors). Functions to check if one is equal, greater or less than another vector")
#
# projectile_trajectory_calculator_title = "Projectile Trajectory Calculator"
# projectile_trajectory_calculator_link = "https://github.com/GiorgiKarchiladze/Projectile-trajectory-calculator"
# projectile_trajectory_calculator_description = ("Given the initial speed, height and angle, calculates and displays an "
#                                                 "approximate graph of the trajectory")
#
# upload_project_to_db(probability_calculator_title, probability_calculator_link, probability_calculator_description)
# upload_project_to_db(vectors_title, vectors_link, vectors_description)
# upload_project_to_db(projectile_trajectory_calculator_title, projectile_trajectory_calculator_link,
#                      projectile_trajectory_calculator_description)
#
#
#
# _title = ""
# _link = ""
# _description = ""
#
#
# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0", port=5000)
