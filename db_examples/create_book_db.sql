CREATE TABLE public.users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

CREATE TABLE public.profiles (
    profile_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL CHECK ( user_id > 0 ),
    profile_info VARCHAR(255),
    birth_date DATE CHECK (birth_date > '1900-01-01'),
    joined_date DATE CHECK (joined_date > birth_date)
);

COMMENT ON COLUMN public.profiles.user_id IS 'Foreign key to users table';
COMMENT ON COLUMN public.profiles.profile_id IS 'Primary key of profiles table';
COMMENT ON COLUMN public.profiles.profile_info IS 'Profile information of the user';
COMMENT ON TABLE public.profiles IS 'Table containing user profiles';


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

CREATE TABLE prices.prices_list (
                             id serial PRIMARY KEY,
                             product_id INT NOT NULL,
                             price NUMERIC NOT NULL,
                             discount NUMERIC NOT NULL,
                             valid_from DATE NOT NULL,
                             valid_to DATE NOT NULL
);
ALTER TABLE prices.prices_list
    ADD CONSTRAINT price_discount_check
        CHECK (
                    price > 0
                AND discount >= 0
                AND price > discount
            );
ALTER TABLE prices.prices_list
    ADD CONSTRAINT valid_range_check
        CHECK (valid_to >= valid_from);

CREATE OR REPLACE FUNCTION auto_generate_user_id()
    RETURNS TRIGGER AS $$
BEGIN
    NEW.user_id := (SELECT MAX(user_id) FROM public.users) + 1;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_auto_generate_user_id
    BEFORE INSERT ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION auto_generate_user_id();

CREATE OR REPLACE FUNCTION check_price_validity()
    RETURNS TRIGGER AS $$
BEGIN
    IF NEW.valid_from > NEW.valid_to THEN
        RAISE EXCEPTION 'Invalid date range: valid_from must be less than or equal to valid_to';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_check_price_validity
    BEFORE INSERT OR UPDATE ON prices.prices_list
    FOR EACH ROW EXECUTE FUNCTION check_price_validity();


CREATE OR REPLACE FUNCTION update_last_updated_column()
    RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_last_updated
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION update_last_updated_column();


CREATE VIEW user_profiles_with_department AS
SELECT p.profile_id, u.username, p.profile_info
FROM public.profiles p
         JOIN public.users u ON p.user_id = u.user_id;

CREATE VIEW student_courses_view AS
SELECT s.student_id, s.student_name, c.course_name
FROM public.students s
         JOIN public.student_courses sc ON s.student_id = sc.student_id
         JOIN public.courses c ON sc.course_id = c.course_id;


CREATE OR REPLACE FUNCTION get_employees_by_department(p_department_name VARCHAR)
    RETURNS TABLE(employee_name VARCHAR, department_name VARCHAR)
AS $$
BEGIN
    RETURN QUERY
        SELECT e.employee_name, d.department_name
        FROM public.employees e
                 JOIN public.departments d ON e.department_id = d.department_id
        WHERE d.department_name = p_department_name;
END;
$$ LANGUAGE plpgsql;


CREATE INDEX idx_user_profile_info ON public.profiles(user_id, profile_info);
CREATE INDEX idx_employee_department ON public.employee_department(employee_id, department_id);
CREATE INDEX idx_student_courses ON public.student_courses(student_id, course_id);
CREATE INDEX idx_student_department ON public.students(student_id, department_id);
CREATE INDEX idx_user_id ON public.profiles(user_id);
CREATE INDEX idx_profile_info ON public.profiles(profile_info);
