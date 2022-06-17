from application.server.instance import server

from application.rest.movie import Movie


application = server.app

application.run(debug=True)