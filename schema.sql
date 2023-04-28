-- SQLBook: Code
DROP TABLE IF EXISTS device ;
CREATE TABLE device (
  id    INTEGER PRIMARY KEY AUTOINCREMENT,
  name         varchar(50) not null,
  lat          DECIMAL(10,6) not null,
  long         DECIMAL(6,5) not null
  -- primary key (id)
);

DROP TABLE IF EXISTS data;
CREATE TABLE data (
  device_id INTEGER not null,
--   date-time DATETIME not null,
  temp FLOAT not null,
  humid FLOAT not null,
  pm_2_5 FLOAT not null,
  pm_10 FLOAT not null,
  aqi_2_5 FLOAT not null,
  aqi_10 FLOAT not null,
  lat          DECIMAL(10,6) not null,
  long         DECIMAL(10,6) not null,
  foreign key (device_id) references device(id)
);

INSERT INTO device VALUES
(99, "betty", 38.89889031725395, -77.04961667870883);

INSERT INTO data VALUES (1, 25, 99, 2, 7, 2, 7, 38.89889031725395, -77.04961667870883); --Tompkins
INSERT INTO data VALUES (1, 25, 99, 2, 7, 2, 7, 38.899233225055276, -77.04780527396329); --Kogan
INSERT INTO data VALUES (1, 25, 99, 2, 7, 2, 7, 38.899963791367554, -77.04703312016095); --USC
INSERT INTO data VALUES (1, 25, 99, 2, 7, 2, 7, 38.89990375406295, -77.0495692487137); --SEH 
INSERT INTO data VALUES (1, 25, 99, 2, 7, 2, 7, 38.899170828081886, -77.04579799732835);-- U-yard

