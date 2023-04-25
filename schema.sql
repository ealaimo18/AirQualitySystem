-- SQLBook: Code
DROP TABLE IF EXISTS device ;
CREATE TABLE device (
  id    INTEGER PRIMARY KEY AUTOINCREMENT,
  name         varchar(50) not null,
  lat          DECIMAL(6,5) not null,
  long         DECIMAL(6,5) not null
  -- primary key (id)
);

DROP TABLE IF EXISTS data;
CREATE TABLE data (
  device_id INTEGER not null,
--   date-time DATETIME not null,
  temp FLOAT not null,
  humid FLOAT not null,
  pmi_in FLOAT not null,
  pmi_out FLOAT not null,
  foreign key (device_id) references device(id)
);

INSERT INTO device VALUES
(1, "betty", 28.500075, -81.463619);

INSERT INTO data VALUES
-- (1, 2019-10-14 14:39:50, 25, 99, 2, 7);
(1, 25, 99, 2, 7);