# test fncs for gtfs-csv-validator


import os as os
import gcv_support as gcv

def test_script(data_schema, version, schema_table, con):
    # read all files from directory test_files/data_schema/version
    dir_name = 'test_files/' + data_schema + '/' + version
    file_list = os.listdir(path = dir_name)

    for file_name in file_list:
        # check schema
        # loads file_name into schema_table checks for errors
        gcv.check_schema(dir_name, file_name, schema_table, con)
        gcv.check_rules(schema_table, file_name, con)

    # when all tests are done, drop tuples from the table
    cur = con.cursor()
    cur.execute("delete from '" + schema_table + "'")





