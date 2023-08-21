import os
from flask import Flask, request
from flask_restx import Resource, Api
from teamsproxy import TeamsProxy


app = Flask(__name__)
api = Api(app)
apitoken = os.getenv("AUTH_TOKEN")
teams_url = os.getenv("TEAMS_URL")


def requires_auth(f):
    def decorated(*args, **kwargs):
        xauthtoken = request.headers.get('X-Auth-Token')
        if xauthtoken and xauthtoken == apitoken:
            return f(*args, **kwargs)
        else:
            return {'message': 'Unauthorized'}, 401
    return decorated


@api.route('/prod/dnac2teams')
class Dnac(Resource):
    @requires_auth
    def post(self):
        payload = request.json
        url = teams_url
        tp = TeamsProxy(payload)
        if tp.send2teams(url):
            return "Successfully forwarded to teams", 202
        
        return "Something went wrong", 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")