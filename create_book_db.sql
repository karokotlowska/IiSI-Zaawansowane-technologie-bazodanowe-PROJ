-- Create tables
CREATE TABLE Author (
    author_id SERIAL PRIMARY KEY,
    author_name VARCHAR(100) NOT NULL,
    UNIQUE(author_name)
);

CREATE TABLE Category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    UNIQUE(category_name)
);

CREATE TABLE Book (
    book_id SERIAL PRIMARY KEY,
    book_title VARCHAR(100) NOT NULL,
    author_id INT NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES Author(author_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE CASCADE,
    UNIQUE(book_title, author_id) 
);

CREATE TABLE BookDetails (
    book_id INT PRIMARY KEY,
    details_text TEXT,
    FOREIGN KEY (book_id) REFERENCES Book(book_id) ON DELETE CASCADE
);

CREATE TABLE Reader (
    reader_id SERIAL PRIMARY KEY,
    reader_name VARCHAR(100) NOT NULL,
    UNIQUE(reader_name)
);

CREATE TABLE BookReader (
    book_id INT NOT NULL,
    reader_id INT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES Book(book_id) ON DELETE CASCADE,
    FOREIGN KEY (reader_id) REFERENCES Reader(reader_id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, reader_id)
);
