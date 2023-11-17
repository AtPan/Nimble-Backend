CREATE TABLE users 
(id int(11) NOT NULL AUTO_INCREMENT, 
name varchar(45) NOT NULL, 
password varchar(45) NOT NULL, 
email varchar(45) NOT NULL, 
PRIMARY KEY (id)) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

CREATE TABLE projects
(id int(11) NOT NULL AUTO_INCREMENT, 
name varchar(45) NOT NULL, 
color varchar(45) NOT NULL, 
user_id int(11) NOT NULL, PRIMARY KEY (id), KEY user_id_idx (user_id),
CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES users (id)
ON DELETE CASCADE ON UPDATE CASCADE) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

CREATE TABLE tasks (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(45) NOT NULL,
  description varchar(256) DEFAULT NULL,
  due_date varchar(45) NOT NULL,
  user_id int(11) NOT NULL,
  project_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY userid_idx (user_id),
  KEY projectid_idx (project_id),
  CONSTRAINT userid FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
