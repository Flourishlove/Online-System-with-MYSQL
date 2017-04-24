# table CITYSTATE
# ------------------------------------------------------------
DROP TABLE IF EXISTS `CITYSTATE`;

CREATE TABLE CITYSTATE
(
    City VARCHAR(50),
    State VARCHAR(50),
    PRIMARY KEY(City, State)
)ENGINE=INNODB DEFAULT CHARSET=utf8;

INSERT INTO `CITYSTATE` (`City`, `State`)
VALUES
    ('Atlanta','Georgia'),
    ('Los Angeles','California'),
    ('Phoenix','Arizona'),
    ('Boston','Massachusetts');

# table USER
# ------------------------------------------------------------
DROP TABLE IF EXISTS `USER`;

CREATE TABLE USER
(
    Email VARCHAR(50) NOT NULL,
    Username VARCHAR(50) NOT NULL,
    Password VARCHAR(50) NOT NULL,
    UserType VARCHAR(50) NOT NULL,
    Title VARCHAR(50) DEFAULT NULL,
    Approved BOOLEAN DEFAULT NULL,
    UCity VARCHAR(50),
    UState VARCHAR(50),
    CONSTRAINT contacts_unique UNIQUE (Username),
    PRIMARY KEY(Email),
    FOREIGN KEY(UCity, UState) REFERENCES CITYSTATE(City, State)
)ENGINE=INNODB DEFAULT CHARSET=utf8;

INSERT INTO `USER` (`Email`, `Username`, `Password`, `UserType`, `Title`, `Approved`, `UCity`, `UState`)
VALUES
    ('lxy.meteor@gmail.com', 'Admin', 'FriApr14', 'admin', NULL, TRUE, 'Atlanta', 'Georgia'),
    ('lry@gmail.com', 'lyr', 'FriApr14', 'city_official', NULL, FALSE, 'Phoenix', 'Arizona'),
    ('xinzhihao.meteor@gmail.com', 'xzh', 'FriApr14', 'city_official', NULL, FALSE, 'Boston', 'Massachusetts');

# table POI
# ------------------------------------------------------------
DROP TABLE IF EXISTS `POI`;
CREATE TABLE POI
(
    Location_Name VARCHAR(50) NOT NULL,
    Flag          BOOLEAN,
    Date_Flagged  DATE,
    Zip_Code      INT,
    PCity         VARCHAR(50),
    PState        VARCHAR(50),
    PRIMARY KEY(Location_Name),
    FOREIGN KEY(PCity, PState) REFERENCES CITYSTATE(City, State)
)ENGINE=INNODB DEFAULT CHARSET=utf8;

INSERT INTO `POI` (`Location_Name`, `Flag`, `Date_Flagged`, `Zip_Code`, `PCity`, `PState`)
VALUES
    ('Georgia Tech', FALSE, NULL, 310058, 'Atlanta', 'Georgia'),
    ('UCLA', FALSE, NULL, 819232, 'Los Angeles', 'California'),
    ('ASU', FALSE, NULL, 182421, 'Phoenix', 'Arizona'),
    ('MIT', TRUE, DATE '2016-03-21', 519932, 'Boston', 'Massachusetts');

# table DATATYPE
# ------------------------------------------------------------
DROP TABLE IF EXISTS `DATATYPE`;
CREATE TABLE DATATYPE
(
     Type VARCHAR(50) NOT NULL,
     PRIMARY KEY(Type)
)ENGINE=INNODB DEFAULT CHARSET=utf8;

INSERT INTO `DATATYPE` (`Type`)
VALUES
    ('mold'),
    ('airquality');

# table DATAPOINT
# ------------------------------------------------------------
DROP TABLE IF EXISTS `DATAPOINT`;
CREATE TABLE DATAPOINT
(
    PLocation_Name  VARCHAR(50) NOT NULL,
    DateRecorded DATETIME  NOT NULL,
    Data_Value INT NOT NULL,
    Accepted BOOLEAN DEFAULT NULL,
    DType VARCHAR(50) NOT NULL,
    PRIMARY KEY(PLocation_Name, DateRecorded),
    FOREIGN KEY(PLocation_Name) REFERENCES POI(Location_Name),
    FOREIGN KEY(DType) REFERENCES DATATYPE(Type)
)ENGINE=INNODB DEFAULT CHARSET=utf8;

INSERT INTO `DATAPOINT` (`PLocation_Name`, `DateRecorded`, `Data_Value`, `Accepted`, `DType`)
VALUES
    ('Georgia Tech', DATE '2017-04-13', 8712, FALSE, 'mold'),
    ('ASU', DATE '2016-05-28', 783, FALSE, 'airquality'),
    ('UCLA', DATE '2012-04-13', 722, FALSE, 'mold'),
    ('MIT', DATE '2016-03-21', 32, TRUE, 'airquality');