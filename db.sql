# table CITYSTATE
# ------------------------------------------------------------
DROP TABLE IF EXISTS `CITYSTATE`;

CREATE TABLE CITYSTATE
(
    City VARCHAR(50),
    State VARCHAR(50),
    PRIMARY KEY(City, State)
)ENGINE=INNODB DEFAULT CHARSET=utf8;

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

# table DATATYPE
# ------------------------------------------------------------
DROP TABLE IF EXISTS `DATATYPE`;
CREATE TABLE DATATYPE
(
     Type VARCHAR(50) NOT NULL,
     PRIMARY KEY(Type)
)ENGINE=INNODB DEFAULT CHARSET=utf8;

# table DATAPOINT
# ------------------------------------------------------------
DROP TABLE IF EXISTS `DATAPOINT`;
CREATE TABLE DATAPOINT
(
    PLocation_Name  VARCHAR(50) NOT NULL,
    DateRecorded DATETIME  NOT NULL,
    Data_Value VARCHAR(50) NOT NULL,
    Accepted BOOLEAN DEFAULT NULL,
    DType VARCHAR(50) NOT NULL,
    PRIMARY KEY(PLocation_Name, DateRecorded),
    FOREIGN KEY(PLocation_Name) REFERENCES POI(Location_Name),
    FOREIGN KEY(DType) REFERENCES DATATYPE(Type)
)ENGINE=INNODB DEFAULT CHARSET=utf8;

