from psycopg import ProgrammingError
from CaesarSQLDB.caesarsql import CaesarSQL
from CaesarJWT.caesarjwt import CaesarJWT
from CaesarSQLDB.caesar_create_tables import CaesarCreateTables
import uuid
from psycopg.errors import UniqueViolation
from CaesarSQLDB.caesarhounidb import CaesarHOUNIDB
import hashlib

class HOUNIDBExplore:
    def __init__(self) -> None:
        self.caesarsql = CaesarSQL()
        self.caesarhounidb = CaesarHOUNIDB()
    def tuple_to_json(self,fields:tuple,result:tuple):
        if type(result[0]) == tuple:
            final_result = []
            for entry in result:
                entrydict = dict(zip(fields,entry))
                final_result.append(entrydict)
            return final_result
        elif type(result[0]) == str:
            final_result = dict(zip(fields,result))
            return final_result 
    def create_tables(self):
        try:
            # Create Criminal Offenses
            #  + 
            res = self.caesarsql.run_command(self.caesarhounidb.create_independent_tables + self.caesarhounidb.create_relationships + self.caesarhounidb.insert_sample_independant + self.caesarhounidb.insert_relationships + self.caesarhounidb.insert_user_auth + self.caesarhounidb.create_view,result_function=self.caesarsql.fetch)
            #print(res)

        except ProgrammingError as pex:
            if "didn't produce a result" in str(pex):
                print({"message":f"table was created."})
            else:
                raise ProgrammingError(pex)
    def get_all(self):
        res = self.caesarsql.run_command(self.caesarhounidb.get_all,result_function=self.caesarsql.fetch)
        fields = ("applicant_uuid", "first_name", "last_name",
        "nationality","language","language_code",
        "job_title","employer_name",
        "conviction","offence",
        "major","degree",
        "institute_name","location",
        "category_name","eligibility_category")
        return self.tuple_to_json(fields,res)
    def get_user_data(self,first_name):
        try:
            res = self.caesarsql.run_command(self.caesarhounidb.get_user_data.replace("?",first_name),result_function=self.caesarsql.fetch)
            fields = ("applicant_uuid", "first_name", "last_name",
            "nationality","language","language_code",
            "job_title","employer_name",
            "conviction","offence",
            "major","degree",
            "institute_name","location",
            "category_name","eligibility_category")
            return self.tuple_to_json(fields,res)
        except IndexError as iex:
            return False
    def count_visa_category(self):
        res = self.caesarsql.run_command(self.caesarhounidb.count_num_category,result_function=self.caesarsql.fetch)

        return self.tuple_to_json(("count_visa_category",),res)
    def sub_query(self):
        res = self.caesarsql.run_command(self.caesarhounidb.sub_query,result_function=self.caesarsql.fetch)
        return self.tuple_to_json(("first_name","visa_category","elgibility category","nationality"),res)
    def user_auth_select(self):
        salt = "7518c3247b86484e9f20725c90530d3f"
        password = "test1234"
        hashed_password = hashlib.sha512((password + salt).encode()).hexdigest()
        res = self.caesarsql.run_command(self.caesarhounidb.user_auth_get % ("bill@gmail.com",hashed_password),result_function=self.caesarsql.fetch)
        fields = ("applicant_uuid", "first_name", "last_name",
            "nationality","language","language_code",
            "job_title","employer_name",
            "conviction","offence",
            "major","degree",
            "institute_name","location",
            "category_name","eligibility_category")
        try:
            val = self.tuple_to_json(fields,res)
            return val
        except IndexError as iex:
            return []
        return 
        #return self.tuple_to_json(("first_name","visa_category","elgibility category","nationality"),res)
houni = HOUNIDBExplore()
print("email:bill@gmail.com","password:test1234","salt:7518c3247b86484e9f20725c90530d3f")
print("""
SELECT user_applicant_view.applicant_uuid, user_applicant_view.first_name, user_applicant_view.last_name,
user_applicant_view.nationality,user_applicant_view.language,user_applicant_view.language_code,
user_applicant_view.job_title,user_applicant_view.employer_name,
user_applicant_view.conviction,user_applicant_view.offence,
user_applicant_view.major,user_applicant_view.degree,
user_applicant_view.institute_name,user_applicant_view.location,
user_applicant_view.category_name,user_applicant_view.eligibility_category
FROM users_cleared,user_applicant_view
WHERE email = '%s' AND password = '%s';""")
#houni.create_tables()
import json
#print("Get Applicants eligible for 6 Month Visa that are German...")
#print(f"Applicants eligible for 6 month Visa that are German: {json.dumps(houni.sub_query(), indent=2)}")
final = []
for x in houni.user_auth_select():
    x["applicant_uuid"] = str(x["applicant_uuid"])
    final.append(x)
print(json.dumps(final, indent=2))

#houni.caesarsql.run_command("DELETE FROM nationality;",result_function=houni.caesarsql.fetch)




