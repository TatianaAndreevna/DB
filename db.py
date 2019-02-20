import psycopg2
from psycopg2.extensions import AsIs


DATABASE = 'dbt'
USER = 'Tatiana'


# создает таблицы
def create_db(database_name=DATABASE, user_name=USER):
    with psycopg2.connect('dbname=%s user=%s' % (database_name, user_name)) \
            as conn:
        with conn.cursor() as curs:
            curs.execute("""CREATE TABLE student (
                id serial PRIMARY KEY NOT NULL,
                name varchar(100) NOT NULL,
                gpa numeric(10,2),
                birth timestamp with time zone);
                """)
            curs.execute("""CREATE TABLE course (
                id serial PRIMARY KEY NOT NULL,
                name varchar(100) NOT NULL);
                """)
            curs.execute("""CREATE TABLE student_course (
                id serial PRIMARY KEY NOT NULL,
                student_id INTEGER REFERENCES student(id),
                course_id INTEGER REFERENCES course(id));
                """)


# возвращает студентов определенного курса
def get_students(course_id):
    with psycopg2.connect('dbname=%s user=%s' % (DATABASE, USER)) \
            as conn:
        with conn.cursor() as curs:
            curs.execute("""select student.name, course.id from student
                join student_course on student_course.student_id = student.id
                join course on course_id = course.id
                where course_id = %s
                """, (course_id,))
            return curs.fetchall()


# создает студентов и
# записывает их на курс
def add_students(course_id, students):
    for student in students:
        columns = student.keys()
        values = [student[column] for column in columns]
        with psycopg2.connect('dbname=%s user=%s' % (DATABASE, USER)) \
                as conn:
            with conn.cursor() as curs:
                insert_st = 'insert into student (%s) values %s returning id'
                curs.execute(curs.mogrify(insert_st,
                                          (AsIs(','.join(columns)),
                                           tuple(values))))
                student_id = curs.fetchone()[0]
                curs.execute("insert into student_course (student_id, course_id) values (%s, %s)",
                             (student_id, course_id))


# просто создает студента
def add_student(student):
    columns = student.keys()
    values = [student[column] for column in columns]
    with psycopg2.connect('dbname=%s user=%s' % (DATABASE, USER)) \
            as conn:
        with conn.cursor() as curs:
            insert_st = 'insert into student (%s) values %s'
            curs.execute(curs.mogrify(insert_st,
                                      (AsIs(','.join(columns)),
                                       tuple(values))))


def get_student(student_id):
    with psycopg2.connect('dbname=%s user=%s' % (DATABASE, USER)) \
            as conn:
        with conn.cursor() as curs:
            curs.execute("select * from student where student.id = %s",
                         (student_id,))
            received_student = curs.fetchall()
            return received_student[0][1]   

        
if __name__ == '__main__':
    create_db()
    student_1 = {
        'name': 'Tatiana',
        'gpa': 10.2,
        'birth': '1994-10-12'
    }
    student_2 = {
        'name': 'Steve',
        'gpa': 7.4,
        'birth': '1982-06-05'
    }
    add_student(student_1)
    add_student(student_2)
