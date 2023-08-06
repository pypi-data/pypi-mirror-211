def add(a, b):
    return a + b

result_default_pre =  {
  "success" : True,
  "result" : {
      "partial_unexpected_list" : [],
      "unexpected_count" : 0,
      "unexpected_percent" : 0,
      "unexpected_percent_nonmissing" : 0
    }
}
  
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