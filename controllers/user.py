from flask_restful import Resource, reqparse


class User(Resource):
    users = [
        {
            'name': 'Alexander',
            'age': '42',
            'occupation': 'Network Engineer'
        },
        {
            'name': 'Graham',
            'age': '34',
            'occupation': 'Doctor'
        },
        {
            'name': 'Watson',
            'age': '22',
            'occupation': 'Web Developer'
        }
    ]

    def get(self, name):
        for user in self.users:
            if (name == user["name"]):
                return user, 200
        return "user not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in self.users:
            if (name == user["name"]):
                return "user with name {} already exists".format(name), 400

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        self.users.append(user)
        return user, 201

    def delete(self, name):
        global users
        users = [user for user in self.users if user["name"] == name]
        return "{} has been deleted".format(name), 200
