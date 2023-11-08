CREATE TABLE public.users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

CREATE TABLE public.profiles (
    profile_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE,
    profile_info VARCHAR(255)
);

ALTER TABLE public.profiles
ADD CONSTRAINT fk_user_id
FOREIGN KEY (user_id)
REFERENCES public.users(user_id);

CREATE TABLE public.departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL
);

CREATE TABLE public.employees (
    employee_id SERIAL PRIMARY KEY,
    employee_name VARCHAR(50) NOT NULL,
    department_id INT
);

ALTER TABLE public.employees
ADD CONSTRAINT fk_department_id
FOREIGN KEY (department_id)
REFERENCES public.departments(department_id);

CREATE TABLE public.employee_department (
    employee_id INT REFERENCES employees(employee_id),
    department_id INT REFERENCES departments(department_id),
    PRIMARY KEY (employee_id, department_id)
);

ALTER TABLE public.employee_department
ADD CONSTRAINT fk_employee_id
FOREIGN KEY (employee_id)
REFERENCES public.employees(employee_id);

ALTER TABLE public.employee_department
ADD CONSTRAINT fk_department_id
FOREIGN KEY (department_id)
REFERENCES public.departments(department_id);



```
CREATE TABLE public.students (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(50) NOT NULL
);

CREATE TABLE public.courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(50) NOT NULL
);

CREATE TABLE public.student_courses (
    student_id INT REFERENCES public.students(student_id),
    course_id INT REFERENCES public.courses(course_id),
    PRIMARY KEY (student_id, course_id)
);

CREATE TABLE public.departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL
);

ALTER TABLE public.students
ADD COLUMN department_id INT REFERENCES public.departments(department_id);

CREATE TABLE public.teachers (
    teacher_id SERIAL PRIMARY KEY,
    teacher_name VARCHAR(50) NOT NULL
);

ALTER TABLE public.courses
ADD COLUMN teacher_id INT REFERENCES public.teachers(teacher_id);

ALTER TABLE public.students
ADD COLUMN teacher_id INT REFERENCES public.teachers(teacher_id);
```