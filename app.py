import requests
from flask import Flask, json, Response, send_from_directory, send_file

MIME_JSON = 'application/json'

def create_app() -> Flask:
    """Create a configured Flash app instance."""
    app = Flask(__name__, instance_relative_config=True)
    app.config['FSA_API_URI'] = "http://api.ratings.food.gov.uk"

    @app.route('/assets/<path:path>')
    def send_js(path) -> None:
        """Send assets (JS, CSS, etc."""
        return send_from_directory('static/assets', path)

    @app.route('/')
    def send_index() -> None:
        """Send static HTML page for the front-end."""
        return send_file('static/index.html')

    @app.route('/api')
    def get_authorities() -> Response:
        """Fetch authorities and return a list of their IDs and name."""
        uri = app.config['FSA_API_URI'] + '/Authorities'
        resp = requests.get(uri, headers={'x-api-version': '2'})

        if resp.status_code != requests.codes.ok:
            raise requests.HTTPError('FSA API call to {} returned error {}'.format(uri, resp.status_code))

        authorities = []
        for authority in resp.json()['authorities']:
            authorities.append(
                {
                    'id': authority['LocalAuthorityId'],
                    'name': authority['Name']
                }
            )

        return Response(json.dumps(authorities), mimetype=MIME_JSON)

    @app.route('/api/<int:authority_id>')
    def get_authority(authority_id: int) -> Response:
        """Fetch ratings for an establishment and return summary information."""
        # This is just sample data to demonstrate what the front-end is expecting
        if authority_id == 1:  # Cambridge City
            demo = [
                {'name': '5-star', 'value': 22.41},
                {'name': '4-star', 'value': 43.13},
                {'name': '3-star', 'value': 12.97},
                {'name': '2-star', 'value': 1.54},
                {'name': '1-star', 'value': 17.84},
                {'name': 'Exempt', 'value': 2.11}
            ]
        else:
            demo = [
                {'name': '5-star', 'value': 50},
                {'name': '4-star', 'value': 0},
                {'name': '3-star', 'value': 0},
                {'name': '2-star', 'value': 0},
                {'name': '1-star', 'value': 25},
                {'name': 'Exempt', 'value': 25}
            ]

        return Response(json.dumps(demo), mimetype=MIME_JSON)

    return app


if __name__ == '__main__':
    create_app().run()
