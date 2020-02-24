import re

class Filter:
    attribute = ""
    operator = ""
    value = ""
    def __init__(self, expression):
        self.attribute, self.operator, self.value = re.split('([><=!]+)', expression)

    def apply(self, record):
        self.record_value = record.info.get(self.attribute)
        return eval("{}{}{}".format(self.record_value, self.operator, self.value))
  
    def __str__(self):
        return ("attribute = {}, operator = {}, value = {}"
                .format(self.attribute, self.operator, self.value))
