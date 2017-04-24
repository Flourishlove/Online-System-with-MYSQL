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
    ('New York','New York'),
    ('Los Angeles','California'),
    ('Chicago','Illinois'),
    ('Houston','Texas'),
    ('Philadelphia','Pennsylvania'),
    ('Phoenix','Arizona'),
    ('San Antonio','Texas'),
    ('San Diego','California'),
    ('Dallas','Texas'),
    ('San Jose','California'),
    ('Austin','Texas'),
    ('Jacksonville','Florida'),
    ('San Francisco','California'),
    ('Indianapolis','Indiana'),
    ('Columbus','Ohio'),
    ('Fort Worth','Texas'),
    ('Charlotte','North Carolina'),
    ('Seattle','Washington'),
    ('Denver','Colorado'),
    ('El Paso','Texas'),
    ('Atlanta','Georgia');

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
    ('lxy.meteor@gmail.com', 'admin', 'admin', 'admin', NULL, TRUE, 'Atlanta', 'Georgia'),
    ('zju@gatech.com', 'zju', 'zju1215', 'admin', NULL, TRUE, 'Chicago', 'Illinois'),
    ('lyr@gmail.com', 'lyr', 'sahdiwq', 'admin', NULL, TRUE, 'Atlanta', 'Georgia'),
    ('xinzhihao@gmail.com', 'xinzhihao', 'jasdn', 'admin', NULL, TRUE, 'Atlanta', 'Georgia'),
    ('wanyijun@gmail.com', 'wanyijun', 'admqwoijin', 'admin', NULL, TRUE, 'Atlanta', 'Georgia'),

    ('offical1@gmail.com', 'offical1', '123', 'city_official', NULL, FALSE, 'Phoenix', 'Arizona'),
    ('offical2@gmail.com', 'offical2', '123', 'city_official', NULL, TRUE, 'Atlanta', 'Georgia'),
    ('offical3@gmail.com', 'offical3', '123', 'city_official', NULL, NULL, 'Phoenix', 'Arizona'),
    ('offical4@gmail.com', 'offical4', '123', 'city_official', NULL, NULL, 'Atlanta', 'Georgia'),
    ('offical5@gmail.com', 'offical5', '123', 'city_official', NULL, NULL, 'Phoenix', 'Arizona'),
    ('offical6@gmail.com', 'offical6', '123', 'city_official', NULL, TRUE, 'Atlanta', 'Georgia'),
    ('offica7@gmail.com', 'offical7', '123', 'city_official', NULL, FALSE, 'Phoenix', 'Arizona'),
    ('offical8@gmail.com', 'offical8', '123', 'city_official', NULL, TRUE, 'Atlanta', 'Georgia'),
    ('offical9@gmail.com', 'offical9', '123', 'city_official', NULL, FALSE, 'Phoenix', 'Arizona'),
    ('offical10@gmail.com', 'offical10', '123', 'city_official', NULL, FALSE, 'Phoenix', 'Arizona'),

    ('scientist1@gmail.com', 'scientist1', '123', 'city_scientist', NULL, FALSE, 'Phoenix', 'Arizona'),
    ('scientist2@gmail.com', 'scientist2', '123', 'city_scientist', NULL, NULL, 'Atlanta', 'Georgia'),
    ('scientist3@gmail.com', 'scientist3', '123', 'city_scientist', NULL, NULL, 'Phoenix', 'Arizona'),
    ('scientist4@gmail.com', 'scientist4', '123', 'city_scientist', NULL, NULL, 'Atlanta', 'Georgia'),
    ('scientist5@gmail.com', 'scientist5', '123', 'city_scientist', NULL, FALSE, 'Denver', 'Colorado'),
    ('scientist6@gmail.com', 'scientist6', '123', 'city_scientist', NULL, TRUE, 'Atlanta', 'Georgia'),
    ('scientist7@gmail.com', 'scientist7', '123', 'city_scientist', NULL, FALSE, 'Phoenix', 'Arizona'),
    ('scientist8@gmail.com', 'scientist8', '123', 'city_scientist', NULL, TRUE, 'Atlanta', 'Georgia'),
    ('scientist9@gmail.com', 'scientist9', '123', 'city_scientist', NULL, FALSE, 'Phoenix', 'Arizona'),
    ('scientist10@gmail.com', 'scientist10', '123', 'city_scientist', NULL, FALSE, 'Phoenix', 'Arizona');

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
    ('Georgia Tech', TRUE, DATE '2017-02-23', 30332, 'Atlanta', 'Georgia'),
    ('Uchicago', TRUE, DATE '2017-02-24', 60637, 'Chicago', 'Illinois'),
    ('GSU', FALSE, NULL, 30303, 'Atlanta', 'Georgia'),
    ('Emory', FALSE, NULL, 30322 , 'Atlanta', 'Georgia'),
    ('TLA', FALSE, NULL, 213141, 'Phoenix', 'Arizona'),
    ('UCLA', FALSE, NULL, 213120, 'Los Angeles', 'California'),
    ('DAS', FALSE, NULL, 182421, 'Phoenix', 'Arizona'),
    ('CXZ', FALSE, NULL, 543532, 'Los Angeles', 'California'),
    ('ASU', FALSE, NULL, 124143, 'Phoenix', 'Arizona'),
    ('CCXZ', TRUE, DATE '2016-03-21', 519932, 'Seattle', 'Washington');

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
('Georgia Tech', DATE '2017-01-31', 12, TRUE, 'mold'),
('Georgia Tech', DATE '2017-02-15', 42, TRUE, 'mold'),
('Georgia Tech', DATE '2017-04-15', 87, TRUE, 'airquality'),
('Georgia Tech', DATE '2017-02-24', 4, TRUE, 'airquality'),
('Georgia Tech', DATE '2017-02-01', 34, TRUE, 'airquality'),
('Georgia Tech', DATE '2017-05-13', 17, TRUE, 'mold'),
('Georgia Tech', DATE '2017-04-19', 27, TRUE, 'mold'),
('Georgia Tech', DATE '2017-06-13', 107, TRUE, 'mold'),
('Georgia Tech', DATE '2017-07-13', 85, TRUE, 'mold'),
('Georgia Tech', DATE '2017-04-13', 99, TRUE, 'mold'),
('ASU', DATE '2016-05-28', 38, TRUE, 'airquality'),
('ASU', DATE '2016-05-22', 10, TRUE, 'mold'),
('UCLA', DATE '2012-04-13', 22, TRUE, 'mold'),
('UCLA', DATE '2012-04-22', 122, TRUE, 'mold'),
('Emory', DATE '2012-04-13', 22, TRUE, 'mold'),
('GSU', DATE '2016-03-21', 32, TRUE, 'airquality'),
('DAS', DATE '2012-05-13', 66, TRUE, 'mold'),
('TLA', DATE '2011-03-21', 66, TRUE, 'airquality'),
('DAS', DATE '2012-06-13', 66, TRUE, 'mold'),
('TLA', DATE '2012-03-21', 66, TRUE, 'airquality'),
('DAS', DATE '2012-04-13', 30, TRUE, 'mold'),
('TLA', DATE '2016-06-21', 1, TRUE, 'mold'),
 ('DAS', DATE '2012-06-23', 66, TRUE, 'mold'),
 ('Uchicago', DATE '2016-03-04', 66, FALSE, 'airquality'),
 ('Uchicago', DATE '2016-04-04', 20, TRUE, 'airquality'),
('Uchicago', DATE '2017-03-22', 12, TRUE, 'airquality'),
 ('Uchicago', DATE '2017-03-21', 3, TRUE, 'airquality'),
 ('DAS', DATE '2012-11-13', 30, TRUE, 'mold'),
 ('CXZ', DATE '2016-06-21', 1, TRUE, 'mold'),
 ('CCXZ', DATE '2012-06-13', 66, TRUE, 'mold'),
 ('Uchicago', DATE '2016-12-04', 66, TRUE, 'airquality'),
 ('TLA', DATE '2010-06-21', 10, TRUE, 'mold'),
 ('DAS', DATE '2010-06-13', 26, TRUE, 'mold'),
 ('Uchicago', DATE '2017-03-04', 36, TRUE, 'airquality'),
 ('Uchicago', DATE '2017-04-04', 40, TRUE, 'airquality'),
 ('CCXZ', DATE '2017-03-22', 12, TRUE, 'airquality'),
 ('CCXZ', DATE '2017-03-21', 3, TRUE, 'airquality'),
 ('DAS', DATE '2010-04-13', 3, TRUE, 'mold'),
 ('CXZ', DATE '2010-06-21', 14, TRUE, 'mold'),
 ('CCXZ', DATE '2010-06-13', 6, TRUE, 'mold'),
 ('Uchicago', DATE '2010-03-04', 96, TRUE, 'airquality');