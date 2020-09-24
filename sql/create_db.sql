CREATE TABLE bb_combo (id SERIAL NOT NULL,
	body_builds CHAR(10) PRIMARY KEY NOT NULL);
CREATE TABLE coc_combo (id SERIAL NOT NULL,
	class_of_crimes VARCHAR(21) PRIMARY KEY NOT NULL);
CREATE TABLE states_combo (id SERIAL NOT NULL,
	states CHAR(20) PRIMARY KEY NOT NULL);
CREATE TABLE gender_combo (id SERIAL NOT NULL,
	gender CHAR(7) PRIMARY KEY NOT NULL);

INSERT INTO bb_combo (body_builds) VALUES ('Unknown'), ('Ectomorph'), ('Endomorph'), ('Mesomorph');

INSERT INTO coc_combo (class_of_crimes)	VALUES ('Unknown'), ('Felony'), ('Misdemeanors'), 
	('Felony-Misdemeanors'), ('Infractions');

INSERT INTO states_combo (states) VALUES ('Unknown'), ('Abia'), ('Akwa Ibom'), ('Adamawa'),
	('Anambra'), ('Bauchi'), ('Bayelsa'), ('Benue'),
	('Borno'), ('Cross River'), ('Delta'), ('Ebonyi'),
	('Enugu'), ('Ekiti'), ('Gombe'), ('Imo'), ('Jigawa'), 
	('Kaduna'), ('Kano'), ('Katsina'), ('Kebbi'),
	('Kogi'), ('Kwara'), ('Lagos'), ('Niger'), ('Ogun'),
	('Ondo'), ('Osun'), ('Oyo'), ('Plateau'), ('Rivers'),
	('Sokoto'), ('Taraba'), ('Yobe'), ('Zamfara');

INSERT INTO gender_combo (gender) VALUES ('Male'), ('Female'), ('Other');

CREATE TABLE cases ( 
	case_numbers INT NOT NULL UNIQUE,
	dates_of_registration DATE NOT NULL,
	PRIMARY KEY(case_numbers, dates_of_registration));
	
CREATE TABLE personal_information (cases_number INT NOT NULL, 
	PRIMARY KEY (cases_number),
	FOREIGN KEY (cases_number) REFERENCES cases(case_numbers),
	first_name VARCHAR(200) NOT NULL,
	last_name VARCHAR(200) NOT NULL,
	aliases VARCHAR(200) NOT NULL,
	birth_date DATE NOT NULL,
	age INT NOT NULL,
	gender CHAR(7) NOT NULL REFERENCES gender_combo(gender),
	height VARCHAR(3) NOT NULL,
	weight INT NOT NULL,
	eye_color VARCHAR(50) NOT NULL,
	hair_color VARCHAR(12) NOT NULL,
	body_build CHAR(10) NOT NULL REFERENCES bb_combo(body_builds),
	mutation TEXT NOT NULL,
	scars_and_marks TEXT NOT NULL,
	nationality VARCHAR(100) NOT NULL,
	state VARCHAR(100) NOT NULL,
	lga VARCHAR(50) NOT NULL,
	residence_address TEXT NOT NULL);

CREATE TABLE official_information (case_number INT NOT NULL,
	date_of_registration DATE NOT NULL, 
	date_of_arrest DATE NOT NULL, 
	PRIMARY KEY (case_number, date_of_registration),
	FOREIGN KEY (case_number, date_of_registration) REFERENCES cases(case_numbers, dates_of_registration),
	arresting_officer CHAR(100) NOT NULL, 
	place_of_arrest TEXT NOT NULL,
	area CHAR(50) NOT NULL,
	division CHAR(50) NOT NULL,
	class_of_crime VARCHAR(50) NOT NULL REFERENCES coc_combo(class_of_crimes),
	crime TEXT NOT NULL,
	ex_convict BOOLEAN,
	violent BOOLEAN,
	known_gang TEXT NOT NULL);

CREATE TABLE incidence_information (case_id INT PRIMARY KEY NOT NULL UNIQUE,
	registration_date DATE NOT NULL,
	fullname CHAR(200) NOT NULL,
	contact VARCHAR(100) NOT NULL,
	officer_in_charge CHAR(100) NOT NULL,
	district CHAR(100) NOT NULL,
	statement VARCHAR(2000)	NOT NULL,
	type_of_incidence VARCHAR(100) NOT NULL,
	evidence VARCHAR(500) NOT NULL,
	witness VARCHAR(100),
	other_info VARCHAR(1000) NOT NULL

	);

CREATE VIEW data_record_view AS (
	SELECT c.case_numbers AS "Case Number", 
	pi.first_name AS "First Name", pi.last_name AS "Last Name", pi.aliases AS "Aliases", pi.birth_date AS "Birth Date", 
	pi.age AS "Age", pi.gender AS "Gender", pi.height AS "Height", pi.weight AS "Weight", 
	pi.eye_color AS "Eye Color", pi.hair_color AS "Hair Color", pi.body_build AS "Body Build", pi.mutation AS "Mutation", 
	pi.scars_and_marks AS "Scars and Marks", pi.nationality AS "Nationality", pi.state AS "State",
	pi.lga AS "LGA", pi.residence_address AS "Residence Address", 
	oi.date_of_arrest AS "Date of Arrest", oi.date_of_registration AS "Date of Registration",
	oi.arresting_officer AS "Arresting Officer", oi.place_of_arrest AS "Place of Arrest", oi.area AS "Area",
	oi.division AS "Division", oi.class_of_crime AS "Class of Crime", oi.crime AS "Crime", 
	oi.ex_convict AS "Ex-Convict", oi.violent AS "Violent", oi.known_gang AS "Known Gang"

	FROM cases AS c JOIN personal_information AS pi ON c.case_numbers = pi.cases_number JOIN official_information AS oi ON c.case_numbers = oi.case_number AND c.dates_of_registration = oi.date_of_registration
	);


CREATE VIEW incidence_view AS ( SELECT ii.case_id AS "CaseID", 
	ii.registration_date AS "Registration Date", ii.fullname AS "Full Name", 
	ii.contact AS "Contact", ii.officer_in_charge AS "Officer in Charge", 
	ii.district AS "District", ii.statement AS "Statement", 
	ii.type_of_incidence AS "Type of Incidence", ii.evidence AS "Evidence", 
	ii.witness AS "Witness", ii.other_info AS "Other Info" 

	FROM incidence_information AS ii
	);
