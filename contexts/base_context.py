class BaseContext(object):
    def __init__(self, req):
        if req.is_json:
            self.__initialize(req)
        else:
            raise ValueError("Not JSON")

    def __initialize(self, request):
        content = request.get_json()

        if content["user_id"] is None:
            raise ValueError("User ID is missing")
        
        if content["password"] is None:
            raise ValueError("Password is missing")

        self.userId = content["user_id"]
        self.password = content["password"]
        