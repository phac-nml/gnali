import re

class Filter:
    attribute = ""
    operator = ""
    value = ""
    def __init__(self, expression):
        print("type of exp: " + str(type(expression)))
        self.attribute = re.split('([><=!]+)', expression)[0]
        self.operator = re.split('([><=!]+)', expression)[1]
        self.value = re.split('([><=!]+)', expression)[2]

    def apply(self, record):
        record_value = record.split("{}=".format(self.attribute))[1]
        record_value = record_value.split(";")[0]
        return eval("{}{}{}".format(record_value, self.operator, self.value))
  
    def __str__(self):
        return ("attribute = {}, operator = {}, value = {}"
                .format(self.attribute, self.operator, self.value))
        