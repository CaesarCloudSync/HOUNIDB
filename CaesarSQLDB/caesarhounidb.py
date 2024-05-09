import uuid
import hashlib
class CaesarHOUNIDB:
    def __init__(self) -> None:
        self.create_independent_tables = f"""
        
            CREATE TABLE IF NOT EXISTS nationality (
            nationality_uuid UUID NOT NULL PRIMARY KEY,
            nationality VARCHAR(255) NOT NULL,
            language VARCHAR(255) NOT NULL,
            language_code CHAR(5) NOT NULL);
            
            CREATE TABLE IF NOT EXISTS applicants (
            applicant_uuid UUID NOT NULL PRIMARY KEY, 
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            date_of_birth DATE NOT NULL,
            income DECIMAL NOT NULL,
            assets DECIMAL NOT NULL,
            liabilities DECIMAL NOT NULL,
            nationality_uuid UUID REFERENCES nationality(nationality_uuid) NOT NULL);
            

                              
            CREATE TABLE IF NOT EXISTS criminal_offenses (
            criminal_offense_uuid UUID NOT NULL PRIMARY KEY, 
            offence VARCHAR(255) NOT NULL);
                              
            CREATE TABLE IF NOT EXISTS work_places (
            work_place_uuid UUID NOT NULL PRIMARY KEY, 
            employer_name VARCHAR(255) NOT NULL);
            
            CREATE TABLE IF NOT EXISTS educational_institutes (
            educational_institute_uuid UUID NOT NULL PRIMARY KEY, 
            institute_name VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL);
            
            CREATE TABLE IF NOT EXISTS visa_categories (
            visa_categorie_uuid UUID NOT NULL PRIMARY KEY, 
            category_name VARCHAR(255) NOT NULL,
            eligibility_category VARCHAR(255) NOT NULL);
            
           
        """
        self.create_relationships= f"""
        CREATE TABLE IF NOT EXISTS work_place_applicant (
            work_place_uuid UUID REFERENCES work_places(work_place_uuid) NOT NULL,
            applicant_uuid UUID REFERENCES applicants(applicant_uuid) NOT NULL, 
            job_title VARCHAR(255) NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL);
        CREATE TABLE IF NOT EXISTS visa_category_applicant (
            visa_categorie_uuid UUID REFERENCES visa_categories(visa_categorie_uuid) NOT NULL,
            applicant_uuid UUID REFERENCES applicants(applicant_uuid) NOT NULL
            );
        CREATE TABLE IF NOT EXISTS applicant_offenses (
            criminal_offense_uuid UUID REFERENCES criminal_offenses(criminal_offense_uuid) NOT NULL,
            applicant_uuid UUID REFERENCES applicants(applicant_uuid) NOT NULL,
            conviction_date DATE NOT NULL,
            conviction VARCHAR(255)
            );
        CREATE TABLE IF NOT EXISTS applicants_education (
            educational_institute_uuid UUID REFERENCES educational_institutes(educational_institute_uuid) NOT NULL,
            applicant_uuid UUID REFERENCES applicants(applicant_uuid) NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            major VARCHAR(255) NOT NULL,
            degree VARCHAR(255) NOT NULL
            );
        CREATE TABLE IF NOT EXISTS users_cleared (
            users_cleared_uuid UUID NOT NULL PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL
            );
    """
        users_cleared_uuid = uuid.uuid4()
        salt = "7518c3247b86484e9f20725c90530d3f"
        password = "test123"
        hashed_password = hashlib.sha512((password + salt).encode()).hexdigest()
        self.insert_user_auth = f"""
        -- INSERT INTO users_cleared (users_cleared_uuid,email,password,salt) VALUES ('{users_cleared_uuid}','bill@gmail.com','{hashed_password}','{salt}');
        """
        self.create_view =f"""
    CREATE OR REPLACE VIEW user_applicant_view as
        SELECT applicants.applicant_uuid, applicants.first_name, applicants.last_name,
            nationality.nationality,nationality.language,nationality.language_code,
            work_place_applicant.job_title,work_places.employer_name,
            applicant_offenses.conviction,criminal_offenses.offence,
            applicants_education.major,applicants_education.degree,
            educational_institutes.institute_name,educational_institutes.location,
            visa_categories.category_name,visa_categories.eligibility_category
            FROM applicants
            INNER JOIN nationality ON applicants.nationality_uuid = nationality.nationality_uuid
            INNER JOIN work_place_applicant ON applicants.applicant_uuid = work_place_applicant.applicant_uuid
            INNER JOIN work_places ON work_place_applicant.work_place_uuid = work_places.work_place_uuid
            INNER JOIN applicant_offenses  ON applicants.applicant_uuid = applicant_offenses.applicant_uuid
            INNER JOIN criminal_offenses ON applicant_offenses.criminal_offense_uuid = criminal_offenses.criminal_offense_uuid
            INNER JOIN applicants_education ON applicants.applicant_uuid = applicants_education.applicant_uuid
            INNER JOIN educational_institutes ON applicants_education.educational_institute_uuid = educational_institutes.educational_institute_uuid
            INNER JOIN visa_category_applicant ON applicants.applicant_uuid = visa_category_applicant.applicant_uuid
            INNER JOIN visa_categories ON visa_category_applicant.visa_categorie_uuid = visa_categories.visa_categorie_uuid;
"""
        self.user_auth_get = f"""
        SELECT user_applicant_view.applicant_uuid, user_applicant_view.first_name, user_applicant_view.last_name,
        user_applicant_view.nationality,user_applicant_view.language,user_applicant_view.language_code,
        user_applicant_view.job_title,user_applicant_view.employer_name,
        user_applicant_view.conviction,user_applicant_view.offence,
        user_applicant_view.major,user_applicant_view.degree,
        user_applicant_view.institute_name,user_applicant_view.location,
        user_applicant_view.category_name,user_applicant_view.eligibility_category
        FROM users_cleared,user_applicant_view
        WHERE email = '%s' AND password = '%s';
        """
        self.update_record = f"""
        UPDATE work_place_applicant
        SET job_title = '%s'
        WHERE work_place_applicant.applicant_uuid = (SELECT applicant_uuid FROM applicants
        WHERE applicants.first_name= '%s')
        RETURNING *;
    """
        self.get_updated_record = f"""

        SELECT * FROM user_applicant_view
        WHERE user_applicant_view.applicant_uuid = (SELECT applicant_uuid FROM applicants
        WHERE applicants.first_name= '%s')
        """
        nationality_uuid = "6737b17c-08ad-4f59-ae9c-b3ca49657bc7" #uuid.uuid4()
        applicant_uuid = "d41eca28-bcbf-4742-a657-be642daf18f1" #uuid.uuid4()
        criminal_offense_uuid = "ff95a155-8893-4f90-95a9-967273fb815d"
        work_place_uuid = "397a2bfc-02f5-4e53-bd87-f1490cd3f3b3" #uuid.uuid4()
        educational_institute_uuid = "d6822cf8-a27c-455f-88ff-142fa320a5bf" #uuid.uuid4()
        visa_categorie_uuid = "7c3aff23-6fd2-4138-a8ff-c8b6a769ea42" #uuid.uuid4()
        self.insert_sample_independant = f"""
        -- INSERT INTO visa_categories (visa_categorie_uuid,category_name,eligibility_category) VALUES ('{visa_categorie_uuid}','6 months','Tier 1');
        -- INSERT INTO educational_institutes (educational_institute_uuid,institute_name,location) VALUES ('{educational_institute_uuid}','Truro School','Truro');
        -- INSERT INTO work_places (work_place_uuid,employer_name) VALUES ('{work_place_uuid}','PA Consulting');
        -- INSERT INTO criminal_offenses (criminal_offense_uuid,offence) VALUES ('{criminal_offense_uuid}','murder');
        -- INSERT INTO nationality (nationality_uuid,nationality,language,language_code) VALUES ('{nationality_uuid}','British','English','en-gb');
        -- INSERT INTO applicants (applicant_uuid,first_name,last_name,date_of_birth,income,assets,liabilities, nationality_uuid) VALUES ('{applicant_uuid}','Amari','Lawal','2005-01-07',50000,20000,30000,'{nationality_uuid}');
    """
        self.insert_relationships = f"""
        -- INSERT INTO applicants_education (educational_institute_uuid,applicant_uuid,start_date,end_date,major,degree) VALUES ('{educational_institute_uuid}','{applicant_uuid}','2016-09-01','2023-09-01','Computer Science','A Level');
        -- INSERT INTO applicant_offenses (criminal_offense_uuid,applicant_uuid,conviction_date,conviction) VALUES ('{criminal_offense_uuid}','{applicant_uuid}','2010-01-03','2 years');
        -- INSERT INTO visa_category_applicant (visa_categorie_uuid,applicant_uuid) VALUES ('{visa_categorie_uuid}','{applicant_uuid}');
        -- INSERT INTO work_place_applicant (work_place_uuid,applicant_uuid,job_title,start_date,end_date) VALUES ('{work_place_uuid}','{applicant_uuid}','Software Engineer','2023-09-01','2026-09-01');
    """
        self.get_all = f"""
        SELECT applicants.applicant_uuid, applicants.first_name, applicants.last_name,
        nationality.nationality,nationality.language,nationality.language_code,
        work_place_applicant.job_title,work_places.employer_name,
        applicant_offenses.conviction,criminal_offenses.offence,
        applicants_education.major,applicants_education.degree,
        educational_institutes.institute_name,educational_institutes.location,
        visa_categories.category_name,visa_categories.eligibility_category
        FROM applicants
        INNER JOIN nationality ON applicants.nationality_uuid = nationality.nationality_uuid
        INNER JOIN work_place_applicant ON applicants.applicant_uuid = work_place_applicant.applicant_uuid
        INNER JOIN work_places ON work_place_applicant.work_place_uuid = work_places.work_place_uuid
        INNER JOIN applicant_offenses  ON applicants.applicant_uuid = applicant_offenses.applicant_uuid
        INNER JOIN criminal_offenses ON applicant_offenses.criminal_offense_uuid = criminal_offenses.criminal_offense_uuid
        INNER JOIN applicants_education ON applicants.applicant_uuid = applicants_education.applicant_uuid
        INNER JOIN educational_institutes ON applicants_education.educational_institute_uuid = educational_institutes.educational_institute_uuid
        INNER JOIN visa_category_applicant ON applicants.applicant_uuid = visa_category_applicant.applicant_uuid
        INNER JOIN visa_categories ON visa_category_applicant.visa_categorie_uuid = visa_categories.visa_categorie_uuid;

        """
        self.get_user_data = f"""
        SELECT applicants.applicant_uuid, applicants.first_name, applicants.last_name,
        nationality.nationality,nationality.language,nationality.language_code,
        work_place_applicant.job_title,work_places.employer_name,
        applicant_offenses.conviction,criminal_offenses.offence,
        applicants_education.major,applicants_education.degree,
        educational_institutes.institute_name,educational_institutes.location,
        visa_categories.category_name,visa_categories.eligibility_category
        FROM applicants
        INNER JOIN nationality ON applicants.nationality_uuid = nationality.nationality_uuid
        INNER JOIN work_place_applicant ON applicants.applicant_uuid = work_place_applicant.applicant_uuid
        INNER JOIN work_places ON work_place_applicant.work_place_uuid = work_places.work_place_uuid
        INNER JOIN applicant_offenses  ON applicants.applicant_uuid = applicant_offenses.applicant_uuid
        INNER JOIN criminal_offenses ON applicant_offenses.criminal_offense_uuid = criminal_offenses.criminal_offense_uuid
        INNER JOIN applicants_education ON applicants.applicant_uuid = applicants_education.applicant_uuid
        INNER JOIN educational_institutes ON applicants_education.educational_institute_uuid = educational_institutes.educational_institute_uuid
        INNER JOIN visa_category_applicant ON applicants.applicant_uuid = visa_category_applicant.applicant_uuid
        INNER JOIN visa_categories ON visa_category_applicant.visa_categorie_uuid = visa_categories.visa_categorie_uuid
        WHERE applicants.first_name = '?';

        """
        self.count_num_category = f"""
        SELECT COUNT(*)
        FROM applicants
        INNER JOIN visa_category_applicant ON applicants.applicant_uuid = visa_category_applicant.applicant_uuid
        INNER JOIN visa_categories ON visa_category_applicant.visa_categorie_uuid = visa_categories.visa_categorie_uuid
        WHERE visa_categories.category_name = '6 months';


        """
        self.sub_query = f"""
        SELECT applicants.first_name,visa_categories.category_name,visa_categories.eligibility_category,nationality.nationality
        FROM applicants
        INNER JOIN nationality ON applicants.nationality_uuid = nationality.nationality_uuid
        INNER JOIN visa_category_applicant ON applicants.applicant_uuid = visa_category_applicant.applicant_uuid
        INNER JOIN visa_categories ON visa_category_applicant.visa_categorie_uuid = visa_categories.visa_categorie_uuid
        WHERE nationality.nationality IN (
                SELECT 
                nationality.nationality
                FROM 
                nationality
                WHERE 
                nationality.nationality = 'German'
            ) ;

        
        """
  