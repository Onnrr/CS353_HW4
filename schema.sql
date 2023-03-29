CREATE DATABASE IF NOT EXISTS cs353hw4db;
USE cs353hw4db;

CREATE TABLE User (
	id INT NOT NULL AUTO_INCREMENT,  
  	password VARCHAR(64),
  	username VARCHAR(64),
  	email VARCHAR(64),
  	PRIMARY KEY(id)
);

CREATE TABLE Task (
    id INT NOT NULL AUTO_INCREMENT,
  	title VARCHAR(64),
  	description TEXT,
  	status VARCHAR(64),
  	deadline datetime,
  	creation_time datetime,
  	done_time datetime,
	user_id INT,  
  	task_type VARCHAR(64),
  	PRIMARY KEY(id)
);

CREATE TABLE TaskType (
    type VARCHAR(64)
);

INSERT INTO User(
  	password,
  	username,
  	email
) VALUES('pass123', 'user1', 'user1@example.com');

INSERT INTO User(
  	password,
  	username,
  	email
) VALUES('password', 'user2', 'user2@example.com');

INSERT INTO TaskType(type) VALUES('Health');
INSERT INTO TaskType(type) VALUES('Job');
INSERT INTO TaskType(type) VALUES('Lifestyle');
INSERT INTO TaskType(type) VALUES('Family');
INSERT INTO TaskType(type) VALUES('Hobbies');

INSERT INTO Task(
  	title,
  	description,
  	status,
  	deadline,
  	creation_time,
  	done_time,
	user_id,  
  	task_type
) VALUES(
    'Go for a walk',
    'Walk for at least 30 mins',
    'Done',
    '2023-03-20 17:00:00',
    '2023-03-15 10:00:00',
    '2023-03-20 10:00:00',
    1,
    'Health'
);
INSERT INTO Task(
  	title,
  	description,
  	status,
  	deadline,
  	creation_time,
  	done_time,
	user_id,  
  	task_type
) VALUES(
    'Clean the house',
    'Clean the whole house',
    'Done',
    '2023-03-18 12:00:00',
    '2023-03-14 09:00:00',
    '2023-03-18 17:00:00',
    1,
    'Lifestyle'
);
INSERT INTO Task(
  	title,
  	description,
  	status,
  	deadline,
  	creation_time,
  	done_time,
	user_id,  
  	task_type
) VALUES(
    'Submit report',
    'Submit quarterly report',
    'Todo',
    '2023-04-12 17:00:00',
    '2023-03-21 13:00:00',
    NULL,
    1,
    'Job'
);
INSERT INTO Task(
  	title,
  	description,
  	status,
  	deadline,
  	creation_time,
  	done_time,
	user_id,  
  	task_type
) VALUES(
    'Call mom',
    'Call mom and wish her',
    'Todo',
    '2023-04-06 11:00:00',
    '2023-03-23 12:00:00',
    NULL,
    1,
    'Family'
);

INSERT INTO Task(
  	title,
  	description,
  	status,
  	deadline,
  	creation_time,
  	done_time,
	user_id,  
  	task_type
) VALUES(
    'Gym workout',
    'Do weight traing for an hour',
    'Done',
    '2023-03-19 14:00:00',
    '2023-03-12 10:00:00',
    '2023-03-19 11:00:00',
    1,
    'Health'
);

INSERT INTO Task(
  	title,
  	description,
  	status,
  	deadline,
  	creation_time,
  	done_time,
	user_id,  
  	task_type
) VALUES(
    'Play guitar',
    'Learn new song for an hour',
    'Todo',
    '2023-04-05 20:00:00',
    '2023-03-20 14:00:00',
    NULL,
    2,
    'Hobbies'
);

INSERT INTO Task(
  	title,
  	description,
  	status,
  	deadline,
  	creation_time,
  	done_time,
	user_id,  
  	task_type
) VALUES(
    'Book flights',
    'Book flights for summer vacation',
    'Done',
    '2023-03-16 09:00:00',
    '2023-03-13 13:00:00',
    '2023-03-16 11:00:00',
    2,
    'Lifestyle'
);

INSERT INTO Task(
  	title,
  	description,
  	status,
  	deadline,
  	creation_time,
  	done_time,
	user_id,  
  	task_type
) VALUES(
    'Write a blog post',
    'Write about recent project',
    'Todo',
    '2023-04-11 17:00:00',
    '2023-03-22 09:00:00',
    NULL,
    2,
    'Job'
);

INSERT INTO Task(
  	title,
  	description,
  	status,
  	deadline,
  	creation_time,
  	done_time,
	user_id,  
  	task_type
) VALUES(
    'Grocery shopping',
    'Buy groceries for the week',
    'Todo',
    '2023-04-05 18:00:00',
    '2023-03-31 10:00:00',
    NULL,
    2,
    'Family'
);

INSERT INTO Task(
  	title,
  	description,
  	status,
  	deadline,
  	creation_time,
  	done_time,
	user_id,  
  	task_type
) VALUES(
    'Painting',
    'Paint a landscape for 2 hours',
    'Done',
    '2023-03-23 15:00:00',
    '2023-03-18 14:00:00',
    '2023-03-23 16:00:00',
    2,
    'Hobbies'
);