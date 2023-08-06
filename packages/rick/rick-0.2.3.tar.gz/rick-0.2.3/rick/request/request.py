
class Request:
    pass


class MyRequest(Request):
    field1 = Text('validation_rules')
    field2 = Int()
    field3 = Field(TypeClass, 'validation_rules') # <-- good approach

class MyOtherRequest(Request):
    field2 = SetOf(MyRequest, required=True, empty=False, count=5)


