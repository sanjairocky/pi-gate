CREATE TABLE
IF NOT EXISTS datasource
(
id INTEGER PRIMARY KEY autoincrement,
name varchar(255) not null,
country varchar(255) not null,
[description] varchar(255),
active BOOLEAN
NOT NULL CHECK
(active IN (0, 1)) DEFAULT 1,
min_freq REAL null,
max_freq REAL null,
mean_freq REAL null,
s_freq REAL null,
last_received DATETIME2 null,
created_on DATETIME2
not null DEFAULT CURRENT_TIMESTAMP,
changed_on DATETIME2 not NULL DEFAULT CURRENT_TIMESTAMP,
changed_by_fk int not null DEFAULT 1,
created_by_fk int not null DEFAULT 1,
CONSTRAINT UQ_datasource UNIQUE (name,country),
CONSTRAINT fk_user_data_source
FOREIGN KEY
(changed_by_fk) REFERENCES user
(id),
CONSTRAINT fk_user_data_source
FOREIGN KEY
(created_by_fk) REFERENCES user
(id)
);


create table
if not EXISTS gl_feed
( source varchar
(255) not null,
country varchar
(2) not null,
[timestamp] DATE not null,
total_feeds BIGINT not null,
created_on DATETIME2
not null DEFAULT CURRENT_TIMESTAMP,
changed_on DATETIME2 not NULL DEFAULT CURRENT_TIMESTAMP,
changed_by_fk int not null DEFAULT 1,
created_by_fk int not null DEFAULT 1,
CONSTRAINT PK_gl_feed PRIMARY KEY
(source, country, timestamp),
CONSTRAINT FK_gl_feed FOREIGN KEY
(source, country) REFERENCES datasource
(id, country),
CONSTRAINT FK_gl_feed
FOREIGN KEY
(country) REFERENCES datasource
(country),
CONSTRAINT fk_user_gl_feed
FOREIGN KEY
(changed_by_fk) REFERENCES user
(id),
CONSTRAINT fk_user_gl_feed
FOREIGN KEY
(created_by_fk) REFERENCES user
(id));


create table
if not EXISTS user( id INT NOT null,
first_name varchar
(255) not null,
last_name varchar
(255) not null,
username VARCHAR
(15) not null,
created_on DATETIME2
not null DEFAULT CURRENT_TIMESTAMP,
changed_on DATETIME2 not NULL DEFAULT CURRENT_TIMESTAMP,
changed_by_fk int not null DEFAULT 1,
created_by_fk int not null DEFAULT 1,
CONSTRAINT pk_user PRIMARY KEY
(id),
CONSTRAINT fk_user FOREIGN KEY
(changed_by_fk) REFERENCES user
(id),
CONSTRAINT fk_user
FOREIGN KEY
(created_by_fk) REFERENCES user
(id)
);