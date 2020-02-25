import re


class Filter:
    attribute = ""
    operator = ""
    value = ""

    def __init__(self, expression):
        self.attribute, self.operator, \
                        self.value = re.split('(>|>=|<|<=|==|!=)', expression)

    def apply(self, record):
        self.record_value = record.info[self.attribute]
        return eval("self.record_value {operator} self.value"
                    .format(operator=self.operator))

    def __str__(self):
        return ("attribute = {}, operator = {}, value = {}"
                .format(self.attribute, self.operator, self.value))
