-- Table: Colors
CREATE TABLE Colors (
    ID bigserial PRIMARY KEY,
    Name character varying(200) NOT NULL
);

-- Table: SouvenirMaterials
CREATE TABLE SouvenirMaterials (
    ID serial PRIMARY KEY,
    Name character varying(200) NOT NULL
);

-- Table: ApplicationMethods
CREATE TABLE ApplicationMethods (
    ID serial PRIMARY KEY,
    Name character varying(200) NOT NULL
);

-- Table: ProcurementStatuses
CREATE TABLE ProcurementStatuses (
    ID serial PRIMARY KEY,
    Name character varying(200) NOT NULL
);

-- Table: Providers
CREATE TABLE Providers (
    ID serial PRIMARY KEY,
    Name character varying(200) NOT NULL,
    Email character varying(200) NOT NULL,
    ContactPerson character varying(200) NOT NULL,
    Comments character varying(1000)
);

-- Table: SouvenirsCategories
CREATE TABLE SouvenirsCategories (
    ID bigserial PRIMARY KEY,
    IdParent bigint REFERENCES SouvenirsCategories(ID),
    Name character varying(100) NOT NULL
);

-- Table: Souvenirs
CREATE TABLE Souvenirs (
    ID bigserial PRIMARY KEY,
    URL character varying(100) NOT NULL,
    ShortName character varying(150) NOT NULL,
    Name character varying(200) NOT NULL,
    Description character varying(2500) NOT NULL,
    Rating smallint NOT NULL,
    IdCategory bigint NOT NULL REFERENCES SouvenirsCategories(ID),
    IdColor bigint NOT NULL REFERENCES Colors(ID),
    Size character varying(150) NOT NULL,
    IdMaterial integer NOT NULL REFERENCES SouvenirMaterials(ID),
    Weight numeric(10,3),
    QTypics character varying(10),
    PicsSize character varying(20),
    IdApplicMetod integer NOT NULL REFERENCES ApplicationMethods(ID),
    AllCategories character varying(150) NOT NULL,
    DealerPrice numeric(10,2) NOT NULL,
    Price numeric(10,2) NOT NULL,
    Comments character varying(1000)
);

-- Table: SouvenirProcurements
CREATE TABLE SouvenirProcurements (
    ID serial PRIMARY KEY,
    IdProvider integer NOT NULL REFERENCES Providers(ID),
    Date date NOT NULL,
    IdStatus integer NOT NULL REFERENCES ProcurementStatuses(ID)
);

-- Table: ProcurementSouvenirs
CREATE TABLE ProcurementSouvenirs (
    ID serial PRIMARY KEY,
    IdSouvenir bigint NOT NULL REFERENCES Souvenirs(ID),
    IdProcurement integer NOT NULL REFERENCES SouvenirProcurements(ID),
    Amount integer NOT NULL,
    Price numeric(10,2) NOT NULL
);

-- Table: SouvenirStores
CREATE TABLE SouvenirStores (
    ID serial PRIMARY KEY,
    IdSouvenir bigint NOT NULL REFERENCES Souvenirs(ID),
    IdProcurement integer NOT NULL REFERENCES SouvenirProcurements(ID),
    Amount integer NOT NULL,
    Comments character varying(1000)
);