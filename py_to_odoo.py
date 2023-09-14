import xmlrpc.client

data_url = 'http://localhost:8069'  # odoo instance url
database = 'school_db'  # database name
user = 'admin'  # username
password = 'e6b94dbed9122da19e6b9e24449226387459a8da'  # api key
common_auth = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(data_url))
uid = common_auth.authenticate(database, user, password, {})
print("Connection Successfull. UID", uid)

data_model = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(data_url))
print(data_model)

search_admission_conf_ids = data_model.execute_kw(
    database, uid, password, 'students.profile', 'search', [[['admission_status', '=', 'Confirmed']]])
# search_admission_conf_ids = data_model.execute_kw(database, uid, password, 'students.profile', 'search_count',[[['admission_status', '=', 'Confirmed']]])
search_admission_conf_ids_limit = data_model.execute_kw(database, uid, password, 'students.profile', 'search_count', [
                                                        [['admission_status', '=', 'Confirmed']]], {'limit': 1})
search_admission_conf_ids_offset = data_model.execute_kw(database, uid, password, 'students.profile', 'search', [
                                                         [['admission_status', '=', 'Confirmed']]], {'offset': 2})
print(search_admission_conf_ids)
print("*****************")
print(search_admission_conf_ids_limit)
print("*****************")
print(search_admission_conf_ids_offset)
print("*****************")
read_particular_field = data_model.execute_kw(database, uid, password, 'students.profile', 'read', [
                                              search_admission_conf_ids], {'fields': ['name', 'standard']})
print(read_particular_field)
print("*****************")
search_and_read = data_model.execute_kw(database, uid, password, 'students.profile', 'search_read', [
                                        [['admission_status', '=', 'Confirmed']]], {'fields': ['name', 'standard']})
print(search_and_read)
print("*****************")
# new_record_student = data_model.execute_kw(database, uid, password, 'students.profile', 'create', [{'name': 'Test Partner', 'email': 'test@test.com'}])
# print(new_record_student)
# print("*****************")