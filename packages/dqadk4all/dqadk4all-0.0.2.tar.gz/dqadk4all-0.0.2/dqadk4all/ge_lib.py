import json as J
from datetime import datetime

result_default_pre =  {
  "success" : True,
  "result" : {
      "partial_unexpected_list" : [],
      "unexpected_count" : 0,
      "unexpected_percent" : 0,
      "unexpected_percent_nonmissing" : 0
    }
}
def normalize_json(j_to_normalize):
  j_to_normalize = J.dumps(j_to_normalize, indent=4)
  j_normalized = J.loads(j_to_normalize)
  return j_normalized
  
def result_default():
  result_default_prepare =  {
    "success" : True,
    "result" : {
        "partial_unexpected_list" : [],
        "unexpected_count" : 0,
        "unexpected_percent" : 0,
        "unexpected_percent_nonmissing" : 0
      }
  }
  result_default_prepare["success"] = True
  result_default_prepare["result"]["partial_unexpected_list"]= []
  result_default_prepare["result"]["unexpected_count"]= 0
  result_default_prepare["result"]["unexpected_percent"]= 0
  return result_default_prepare

def result_error_exception(result_error_e,e):
    s = str(e).replace('[','').replace(']','').replace('{','').replace('}','')
    error = "Function error, please check log:  " + s
    if ("UNRESOLVED_COLUMN" in s):
        error = " Check Test Case: A column cannot be resolved"
    result_error_e["success"] = False
    result_error_e["result"]["partial_unexpected_list"].append(error) 
    return result_error_e

def table_columns_correct_nomenclature(geDF,Table,ignore_columns_list):
  column_list=geDF.spark_df.columns
  tableFullName = Table
  Table_columns_correct_nomenclature_result = result_default()
  expected_count = 0
  unexpected_count = 0
  unexpected_percent = 0
  test_count = 0
  error_list = []
  try:  
    ignore_columns_list_main=ignore_columns_list.split(",")
    relevant_columns_list=set(column_list)-set(ignore_columns_list_main)
    for item in relevant_columns_list:
      test_count = test_count +1
      if ('fact' in tableFullName):
        if (item.startswith('SK_')| item.startswith('MTR_')|item.startswith('ATR_')):
          expected_count = expected_count + 1 
        else:
          unexpected_count = unexpected_count + 1 
          error_list.append(item)
      else:
        if (item.startswith('SK_')| item.startswith('COD_')|item.startswith('ATR_')|item.startswith('DSC_') | item.startswith('FLG_')):
          expected_count = expected_count + 1 
        else:
          unexpected_count = unexpected_count + 1
          error_list.append(item)
    if unexpected_count > 0:
      Table_columns_correct_nomenclature_result["success"] = False
      unexpected_percent = (unexpected_count + expected_count) / unexpected_count
      Table_columns_correct_nomenclature_result["result"]["partial_unexpected_list"] =[]
      Table_columns_correct_nomenclature_result["result"]["partial_unexpected_list"].append("Columns don't follow correct Nomenclature")
      Table_columns_correct_nomenclature_result["result"]["unexpected_count"] = unexpected_count
      Table_columns_correct_nomenclature_result["result"]["unexpected_percent"]= unexpected_percent
    Table_columns_correct_nomenclature_result = normalize_json(Table_columns_correct_nomenclature_result)
  except Exception as e:
    result_error = result_error_exception(Table_columns_correct_nomenclature_result,e)
    return result_error  
  return Table_columns_correct_nomenclature_result 

# COMMAND ----------

# MAGIC %md ### Check Nulls in Columns 

# COMMAND ----------

# DBTITLE 0,Check Nulls in Columns 
def table_columns_check_nulls(geDF, Sets):
  Test_Sets = Sets
  column_list = Test_Sets.split(',') 
  error_list = []
  try:
    Table_columns_check_nulls_result = result_default()
    for item in column_list:
      tc_result = geDF.expect_column_values_to_not_be_null(item)
      if  tc_result["success"] == False:
          Table_columns_check_nulls_result["success"] = False
          error_list.append(item)
    if  Table_columns_check_nulls_result["success"] == False:
        Table_columns_check_nulls_result["result"]["partial_unexpected_list"]= []     
        Table_columns_check_nulls_result["result"]["partial_unexpected_list"].append(error_list)
        Table_columns_check_nulls_result["result"]["unexpected_count"]= 1
        Table_columns_check_nulls_result["result"]["unexpected_percent"]= 1
  except Exception as e:
    result_error = result_error_exception(Table_columns_check_nulls_result,e)
    return result_error  
  return Table_columns_check_nulls_result  


# COMMAND ----------

# MAGIC %md ### Check Table Duplicates

# COMMAND ----------

def table_columns_check_duplicates(geDF, Sets):
  Test_Sets = Sets
  column_list = Test_Sets.split(',')
  try:  
    table_columns_check_duplicates_result = result_default()
    tc_dup_result = geDF.expect_compound_columns_to_be_unique(column_list)
    if  tc_dup_result["success"] == False:
        table_columns_check_duplicates_result["success"] = False
        table_columns_check_duplicates_result["result"]["partial_unexpected_list"] = []
        table_columns_check_duplicates_result["result"]["partial_unexpected_list"].append("Duplicates rows found in table")
        table_columns_check_duplicates_result["result"]["unexpected_count"] = tc_dup_result["result"]["unexpected_count"]
        table_columns_check_duplicates_result["result"]["unexpected_percent"] = tc_dup_result["result"]["unexpected_percent"]
    table_columns_check_duplicates_result = normalize_json(table_columns_check_duplicates_result)
  except Exception as e:
    print(e)
    result_error = result_error_exception(table_columns_check_duplicates_result,e)
    return result_error  
  return table_columns_check_duplicates_result 

# COMMAND ----------

# MAGIC %md ### Check Table Columns

# COMMAND ----------

# DBTITLE 0,Check Table Columns
def table_columns_match(geDF, Sets):
  Table_columns_match_result = result_default()
  Test_Sets = Sets
  column_list = Test_Sets.split(',')
  error_list = [] 
  try:
    tc_col_result = geDF.expect_table_columns_to_match_set(column_list)
    if  tc_col_result["success"] == False:
        Table_columns_match_result["success"] = False
        unexpected = tc_col_result["result"]["details"]["mismatched"]["unexpected"]
        if unexpected is not None:
          msg = "Unexpected Columns: " + str(unexpected)
          error_list.append(msg)
        missing = tc_col_result["result"]["details"]["mismatched"]["missing"]
        if missing is not None:
          msg = "Missing Columns: " + str(missing)
          error_list.append(msg)
        Table_columns_match_result["result"]["partial_unexpected_list"]=[]
        Table_columns_match_result["result"]["partial_unexpected_list"].append(error_list)
        Table_columns_match_result["result"]["unexpected_count"] = 1
        Table_columns_match_result["result"]["unexpected_percent"] = 1
  except Exception as e:
    result_error = result_error_exception(Table_columns_match_result,e)
    return result_error   
  return Table_columns_match_result  


# COMMAND ----------

# MAGIC %md ### Check Column value lengths to be between

# COMMAND ----------

def check_column_value_lengths_to_be_between(geDF,parameters,sets):
  check_column_value_lengths_to_be_between_result = result_default()
  column_to_check = parameters
  min_value = sets.split(":")[0]
  max_value = sets.split(":")[1]
  error_list = [] 
  try:
    tc_col_result = geDF.expect_column_value_lengths_to_be_between(column_to_check,min_value,max_value)
    if  tc_col_result["success"] == False:
        error_list.append(list(set(tc_col_result["result"]["partial_unexpected_list"]))) 
        check_column_value_lengths_to_be_between_result["success"] = False
        check_column_value_lengths_to_be_between_result["result"]["partial_unexpected_list"]=[]
        check_column_value_lengths_to_be_between_result["result"]["partial_unexpected_list"].append(error_list)
        check_column_value_lengths_to_be_between_result["result"]["unexpected_count"] = tc_col_result["result"]["unexpected_count"]
        check_column_value_lengths_to_be_between_result["result"]["unexpected_percent"] = tc_col_result["result"]["unexpected_percent"]
  except Exception as e:
    result_error = result_error_exception(check_column_value_lengths_to_be_between_result,e)
    return result_error   
  return check_column_value_lengths_to_be_between_result  

# COMMAND ----------

# MAGIC %md ### Validate Default Values in Static Dimension

# COMMAND ----------

def table_columns_static_dimension_default_values_existence(source_df,Sets):
  table_columns_static_dimension_default_values_existence_result = result_default()
  columns_to_iterate=Sets.split(",")
  tc_sta_result = source_df.expect_column_values_to_not_be_in_set(columns_to_iterate[0],[-1,-2])
  try:
    if  tc_sta_result["success"] == True:
        table_columns_static_dimension_default_values_existence_result["success"] = False
        table_columns_static_dimension_default_values_existence_result["result"]["partial_unexpected_list"] = []
        table_columns_static_dimension_default_values_existence_result["result"]["partial_unexpected_list"].append("Default values -1 or -2 not Found")
        table_columns_static_dimension_default_values_existence_result["result"]["unexpected_count"] = 0
        table_columns_static_dimension_default_values_existence_result["result"]["unexpected_percent"] = 1
  except Exception as e:
    result_error = result_error_exception(table_columns_static_dimension_default_values_existence_result,e)
    return result_error      
  return table_columns_static_dimension_default_values_existence_result

# COMMAND ----------

# MAGIC %md ###Validate Key Value Connections

# COMMAND ----------

def validate_key_value_connections(source_df, Sets, Parameters,db):
  validate_dimension_data_connection_result = result_default()
  columns_to_iterate=Sets.split(",")
  error_list = []
  try:
    for column in columns_to_iterate:
      skFact=column.split(":")[0]
      if(len(column.split(":")[1].split("."))==2):
        table_to_check =column.split(":")[1].split(".")[0]
        column_to_check = column.split(":")[1].split(".")[1]   
        SQL_Column = "Select DISTINCT(" + column_to_check + ") From " + db +"."+ table_to_check 
        dimTable = spark.sql(SQL_Column)
        factTableSK=source_df.select(skFact).distinct()
        differenceFactDim=factTableSK.exceptAll(dimTable)
        if(len(differenceFactDim.head(1))!=0):
          validate_dimension_data_connection_result["success"] = False
          msg_error = skFact + " - " + table_to_check + " : error in mapped values"
          error_list.append(msg_error)
      else:
        msg_error = "The test case for column "+skFact+" is not properly designed."
        error_list.append(msg_error)
    if validate_dimension_data_connection_result["success"] == False:
        validate_dimension_data_connection_result["result"]["partial_unexpected_list"] =[]
        validate_dimension_data_connection_result["result"]["partial_unexpected_list"].append(error_list)
        validate_dimension_data_connection_result["result"]["unexpected_count"]= 1
        validate_dimension_data_connection_result["result"]["unexpected_percent"]= 1  
  except Exception as e:
    result_error = result_error_exception(validate_dimension_data_connection_result,e)
    return result_error         
  return validate_dimension_data_connection_result

# COMMAND ----------

# MAGIC %md ### Validate Percentage of -1 and -2 Values in Columns

# COMMAND ----------

def validate_percentage_of_values_in_columns(geDF,parameters,sets):
  validate_percentage_of_values_in_columns_result = result_default()
  columns_to_iterate = sets.split(",")
  check_percent = int(parameters.replace('%',''))
  error_list = []
  try:  
    for item in columns_to_iterate:
      tc_result = geDF.expect_column_values_to_not_be_in_set(item,[-1,-2])
      if  tc_result["result"]["unexpected_percent_total"] >= check_percent:
          validate_percentage_of_values_in_columns_result["success"] = False
          percent_excess = tc_result["result"]["unexpected_percent_total"]
          msg_error = item + " - " + str("{:.2f}".format(percent_excess)) + "%"
          error_list.append(msg_error)
    if  validate_percentage_of_values_in_columns_result["success"] == False:
        validate_percentage_of_values_in_columns_result["result"]["partial_unexpected_list"]= error_list
        validate_percentage_of_values_in_columns_result["result"]["unexpected_count"]= 1
        validate_percentage_of_values_in_columns_result["result"]["unexpected_percent"]= 1  
  except Exception as e:
    result_error = result_error_exception(validate_percentage_of_values_in_columns_result,e)
    return result_error      
  return validate_percentage_of_values_in_columns_result

# COMMAND ----------

# MAGIC %md ###Validate list of values in column

# COMMAND ----------

def validate_list_of_values_in_column(geDF,parameters,sets):
  validate_list_of_values_in_column_result = result_default()
  error_list = []
  # list_to_check = []  
  list_to_check=sets.split(",")
  try:  
    tc_result = geDF.expect_column_values_to_be_in_set(parameters,list_to_check)
    if  tc_result["success"] == False:
        validate_list_of_values_in_column_result["success"] = False
        validate_list_of_values_in_column_result["result"]["partial_unexpected_list"]= []   
        validate_list_of_values_in_column_result["result"]["partial_unexpected_list"].append(tc_result["result"]["partial_unexpected_list"])
        validate_list_of_values_in_column_result["result"]["unexpected_count"]= tc_result["result"]["unexpected_count"]
        validate_list_of_values_in_column_result["result"]["unexpected_percent"]= tc_result["result"]["unexpected_percent"]  
  except Exception as e:
    print(e)
    result_error = result_error_exception(validate_list_of_values_in_column_result,e)
    return result_error      
  return validate_list_of_values_in_column_result

# COMMAND ----------

# MAGIC %md ###Check orphan values in column table

# COMMAND ----------

def check_orphan_values_in_column_table(sourceDF,Sets,Filter,Parameters):
  columns_to_iterate=Sets.split(",")
  first_table_columns=''
  second_table_columns=''
  cross_check_values_between_tables_result = result_default()
  error_list=[]
  
  if Filter is not None:
    with_filter = " where {Filter}".format(Filter=Filter)
  else:
    with_filter = ""
  
  for columns in columns_to_iterate:
    if(columns==columns_to_iterate[len(columns_to_iterate)-1]):
      first_table_columns+=columns.split(":")[0]
      second_table_columns+=columns.split(":")[1]
    else:
      first_table_columns+=columns.split(":")[0]+","
      second_table_columns+=columns.split(":")[1]+","
  data_to_check="select {second_table_columns} from {Parameters} {with_filter}".format(second_table_columns=second_table_columns,Parameters=Parameters,with_filter=with_filter)
  df_data_to_check=spark.sql(data_to_check)
  df_data_to_check_Values=sourceDF.select(first_table_columns.split(",")).filter("{column} not in (-1,-2)".format(column=first_table_columns.split(",")[0])).dropDuplicates()
  remaining_df_data_origin=df_data_to_check_Values.exceptAll(df_data_to_check)
  try:
    orphan_data_in_origin  = len(remaining_df_data_origin.head(1))
    if(orphan_data_in_origin != 0):
        msg_error = "Orphan data in Table: "  + str(remaining_df_data_origin.collect()).replace("Row","")
        error_list.append(msg_error)
        cross_check_values_between_tables_result["success"] = False
        cross_check_values_between_tables_result["result"]["partial_unexpected_list"]= error_list
        cross_check_values_between_tables_result["result"]["unexpected_count"]= 1
        cross_check_values_between_tables_result["result"]["unexpected_percent"]= 1  
  except Exception as e:
    result_error = result_error_exception(cross_check_values_between_tables_result,e)
    return result_error          
  return cross_check_values_between_tables_result

# COMMAND ----------

# MAGIC %md ### Validate Start Date after End Date

# COMMAND ----------

def validate_if_startdate_after_enddate(geDF, Sets):
  validate_if_startdate_after_enddate_result = result_default()
  columns_to_iterate = Sets.split(",")
  try:
    column_a = columns_to_iterate[0]
    column_b = columns_to_iterate[1]
    tc_dates_result = geDF.expect_column_pair_values_A_to_be_greater_than_B(column_b,column_a, True)
    if  tc_dates_result["success"] == False:
      validate_if_startdate_after_enddate_result["success"] = False
      validate_if_startdate_after_enddate_result["result"]["partial_unexpected_list"] = []
      validate_if_startdate_after_enddate_result["result"]["partial_unexpected_list"].append("Start Date After End Date Dectected")
      validate_if_startdate_after_enddate_result["result"]["unexpected_count"]= tc_dates_result["result"]["unexpected_count"]
      validate_if_startdate_after_enddate_result["result"]["unexpected_percent"]= tc_dates_result["result"]["unexpected_percent"]  
  except Exception as e:
    result_error = result_error_exception(validate_if_startdate_after_enddate_result,e)
    return result_error   
  return validate_if_startdate_after_enddate_result  


# COMMAND ----------

# MAGIC %md ### Validate views in datamart

# COMMAND ----------

# def validate_views_in_datamart(sourceDF):
#   column_list=geDF.spark_df.columns
#   #ADD PARAMETER TO IGNORE COLUMNS
#   tableFullName = Table
#   Validate_views_in_datamart_result = dq.result_default()
#   expected_count = 0
#   unexpected_count = 0
#   unexpected_percent = 0
#   test_count = 0
#   error_list = []
#   try:
#     columns_to_iterate=Sets.split(",")
#     AtrResultMessage = 'Checking views in Synapse \n'
#     #iterate the list of three keywords to consider
#     for column in columns_to_iterate:
#       #the first keyword is the name of the key column of the main table
#       skFact=column.split(":")[0]
#       #checks if the second and third keywords are present. if not present the test is not properly designed.
#       if(len(column.split(":")[1].split("."))==2):
#         #the second keyword is the name of the table with which there is an established connection.
#         tableDim=column.split(":")[1].split(".")[0]
#         #the third keyword is the name of the key column present in the table with which there is an established connection.
#         skDim=column.split(":")[1].split(".")[1]
#         #load a table with which there is an established connection in a dataframe 
#         dimTable=LoadTableToCheck(db+"."+tableDim,Parameters)
#         #load the key column of the main table in a dataframe 
#         factTableSK=sourceDF.select("{sk}".format(sk=skFact)).distinct()
#         #load the key column of the table with  which there is an established connection in a dataframe 
#         dimTableSK=dimTable.select("{sk}".format(sk=skDim)).distinct()
#         #get the difference between the 2 previous dataframes in terms of data
#         differenceFactDim=factTableSK.exceptAll(dimTableSK)
#         #if the dataframe with the differences has no data then the connection is done properly else it is not and it is displayed
#         #the information about the differences
#         if(len(differenceFactDim.head(1))==0):
#           AtrResultMessage = AtrResultMessage+"- The column "+skFact+" of the table contains values properly mapped to: "+tableDim+"."
#         else:
#           AtrResultMessage = AtrResultMessage+"- The column "+skFact+" of the table does not contain properly mapped values: "+tableDim+":  "+str(differenceFactDim.rdd.collect()).replace("Row","")
#       else:
#         AtrResultMessage = AtrResultMessage+"- The test case for column "+skFact+" is not properly designed."   
#   except Exception as e:
#     result_error = result_error_exception(validate_if_startdate_after_enddate_result,e)
#     return result_error     
#   return AtrResultMessage

# COMMAND ----------

# MAGIC %md ### Check table row count with source table

# COMMAND ----------

def check_table_row_count_with_source_table(Table, SourcePath, Parameters):
  tc_Parameters = Parameters
  tc_table = SourcePath + '.' + Table
  check_table_row_count_with_table_result = result_default()
  try:
    sql_count = "SELECT COUNT(*) as table_a_count FROM " + tc_table
    table_a_count = spark.sql(sql_count)
    a_count = table_a_count.first().table_a_count
    sql_count_raw = "SELECT COUNT(*) as table_b_count FROM " + tc_Parameters
    table_b_count = readSql(sql_count_raw)
    b_count = table_b_count.first().table_b_count
    if a_count != b_count:
        check_table_row_count_with_table_result["success"] = False
        check_table_row_count_with_table_result["result"]["partial_unexpected_list"] =[]
        check_table_row_count_with_table_result["result"]["partial_unexpected_list"].append(tc_table + ": " + str(a_count) + " - " + tc_Parameters + ": " + str(b_count))
        check_table_row_count_with_table_result["result"]["unexpected_count"]= 1
        check_table_row_count_with_table_result["result"]["unexpected_percent"]= 1
  except Exception as e:
    result_error = result_error_exception(check_table_row_count_with_table_result,e)
    return result_error  
  return check_table_row_count_with_table_result

def execute_tc(TestSuiteCode, TestCaseCode, Model, TestCase, Table, Filter, Parameters, Sets, geDF, Sourcepath, source_df):
  test_start_time = set_time_now()
  tc_TestSuiteCode = TestSuiteCode
  tc_TestCaseCode = TestCaseCode
  tc_Table = Table
  tc_Sets = Sets 
  tc_Model = Model
  tc_TestCase = TestCase
  tc_Filter = Filter
  tc_Parameters = Parameters
  tc_sourcepath = Sourcepath
  ResultData = result_default()
  if (tc_TestCase == 'Check Columns'): 
    ResultData = table_columns_match(geDF, tc_Sets)
  elif (tc_TestCase == 'Check Nulls'): 
    ResultData = table_columns_check_nulls(geDF, tc_Sets)
  elif (tc_TestCase == 'Validate Nomenclature'): 
    ResultData = table_columns_correct_nomenclature(geDF,Table,tc_Sets)
  elif (tc_TestCase == 'Check Duplicates'): 
    ResultData = table_columns_check_duplicates(geDF,tc_Sets)
  elif tc_TestCase == 'Validate Default Values in Static Dimension':
    ResultData = table_columns_static_dimension_default_values_existence(geDF,Sets)
  elif tc_TestCase == 'Validate -1 and -2 Values Percentage':
    ResultData = validate_percentage_of_values_in_columns(geDF,tc_Parameters,tc_Sets)
  elif tc_TestCase == 'Validate Key Value Connection':
    ResultData = validate_key_value_connections(source_df, tc_Sets, tc_Parameters, tc_sourcepath)
  elif tc_TestCase == 'Validate if start date after end date':
    ResultData = validate_if_startdate_after_enddate(geDF, tc_Sets)
  elif tc_TestCase == 'Check orphan values in column table':
    ResultData = check_orphan_values_in_column_table(source_df,Sets,Filter,Parameters)  
  elif tc_TestCase == 'Check table row count with source table':
    ResultData = check_table_row_count_with_source_table(Table,Sourcepath,Parameters)
  elif tc_TestCase == 'Validate list of values in column':    
    ResultData = validate_list_of_values_in_column(geDF,tc_Parameters,tc_Sets)
  elif tc_TestCase == 'Check column value lengths to be between':      
    ResultData = check_column_value_lengths_to_be_between(geDF,tc_Parameters,tc_Sets)
#   elif tc_TestCase == 'Validate views in datamart':
#     ResultData = Validate_views_in_datamart(source_df)  
  else:
    ResultData = result_default()
    ResultData["success"] = False
    ResultData["result"]["partial_unexpected_list"].append(tc_TestCase + " - Not Implemented")
  test_end_time = set_time_now()
  # display(ResultData)
  Result_TestCase_Execution = FormatResult(tc_TestSuiteCode, tc_TestCaseCode, tc_Model, tc_TestCase, tc_Table, test_start_time, test_end_time, ResultData)
  Result_TestCase_Execution = normalize_json(Result_TestCase_Execution)
#   display(Result_TestCase_Execution)
  return Result_TestCase_Execution  

def set_time_now():
    now = datetime.now()
    current_time = now.time().isoformat(timespec='seconds')
    return current_time

# Add itens TestSuite and TestCase to test result
def FormatResult(testsuite, testcase, test_model, test, test_table, start_time, end_time, f_result):
  f_result['testsuite'] = testsuite
  f_result['testcase'] = testcase
  f_result['test_model'] = test_model
  f_result['test_table'] = test_table
  f_result['test'] = test
  f_result['test_start_time'] = start_time
  f_result['test_end_time'] = end_time
  return f_result

def AddResult(j_testrun,j_testcase_result):
  j_testrun['run_result'].append(j_testcase_result)
  return j_testrun
