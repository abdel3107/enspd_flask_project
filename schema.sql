CREATE TABLE IF NOT EXISTS mainUser (
  user_id SERIAL PRIMARY KEY,
  lastname VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS instAdmin (
  admin_id SERIAL PRIMARY KEY,
  user_id INT,
  FOREIGN KEY (user_id) REFERENCES mainUser(user_id)
);

CREATE TABLE IF NOT EXISTS institution (
  inst_id SERIAL PRIMARY KEY,
    admin_id INT,
  FOREIGN KEY (admin_id) REFERENCES instAdmin(admin_id),
  institution_name VARCHAR(255) NOT NULL,
    country VARCHAR(255),
  town VARCHAR(255),
  address VARCHAR(255),
    website VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS teacher (
  teacher_id SERIAL PRIMARY KEY,
  user_id INT,
  FOREIGN KEY (user_id) REFERENCES mainUser(user_id)
);

CREATE TABLE IF NOT EXISTS course (
  course_id SERIAL PRIMARY KEY,
  teacher_id INT,
  FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id),
  inst_id INT,
  FOREIGN KEY (inst_id) REFERENCES institution(inst_id),
  title VARCHAR(255) NOT NULL,
  description VARCHAR(255),
  is_confirmed BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS content (
  content_id SERIAL PRIMARY KEY,
  course_id INT,
  FOREIGN KEY (course_id) REFERENCES course(course_id),
  content_type VARCHAR(255) NOT NULL,
  content_data VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS student (
  stud_id SERIAL PRIMARY KEY,
  user_id INT,
  FOREIGN KEY (user_id) REFERENCES mainUser(user_id)
);
