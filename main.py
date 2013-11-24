import webapp2
from webapp2_extras import json


class MainHandler(webapp2.RequestHandler):
    '''
    handle request to root and share json with user ip, and location
    '''

    def get(self):
        request = self.request
        response = self.response

        location = [coord.strip() for coord in str(request.headers.get("X-AppEngine-CityLatLong")).split(',')]

        #allow all CORS requests
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        response.headers['Content-Type'] = 'application/json'
        response.write(json.encode({
            'ip': str(request.remote_addr),
            'country': str(request.headers.get("X-AppEngine-Country")),
            'region': str(request.headers.get("X-AppEngine-Region")),
            'city': str(request.headers.get("X-AppEngine-City")),
            'coords': {
                'latitude': safe_list_get(location, 0, 0),
                'longitude': safe_list_get(location, 1, 0)
            },
            'sources': 'https://github.com/hyzhak/get-current-position',
            'author': 'https://github.com/hyzhak',
            'licence': 'MIT'
        }))


def safe_list_get(l, idx, default=None):
    '''
    safe get element from list

    :param l:
    :param idx:
    :param default:
    :return:
    '''

    if len(l) > idx:
        return l[idx]
    else:
        return default

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
