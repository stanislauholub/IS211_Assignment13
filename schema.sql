CREATE TABLE IF NOT EXISTS student(id TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS quiz(id TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS result(id TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS student (
    std_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT
);

CREATE TABLE IF NOT EXISTS quiz (
    quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT
    number_of_questions TEXT,
    Date TEXT
);

CREATE TABLE IF NOT EXISTS result (
    res_id INTEGER,
    std_id INTEGER,
    quiz_id INTEGER,
    marks INTEGER, PRIMARY KEY(res_id), FOREIGN KEY(quiz_id) REFERENCES quiz(quiz_id), FOREIGN KEY(std_id) REFERENCES student (std_id)
);

INSERT INTO student VALUES(1, 'John', 'Smith');
INSERT INTO quiz VALUES(1, 'Python Basics', 5, 'February 5, 2015');
INSERT INTO result VALUES(1, 1, 85 )