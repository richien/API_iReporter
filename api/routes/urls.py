from api.views.red_flags_view import RedFlagsView
from api.auth.signup import Signup


class Routes:
    
    @staticmethod
    def fetch_urls(app):
        red_flags_view = RedFlagsView.as_view('redflag')
        signup = Signup.as_view('signup')
        app.add_url_rule('/api/v1/red-flags', defaults={'red_flag_id':None},
                            view_func=red_flags_view, methods=['GET'])
        app.add_url_rule('/api/v1/red-flags/<int:red_flag_id>', view_func=red_flags_view, methods=['GET'])
        app.add_url_rule('/api/v1/red-flags', view_func=red_flags_view, methods=['POST'])
        app.add_url_rule('/api/v1/red-flags/<int:red_flag_id>/location', view_func=red_flags_view, methods=['PUT'])
        app.add_url_rule('/api/v1/red-flags/<int:red_flag_id>/comment', view_func=red_flags_view, methods=['PUT'])
        app.add_url_rule('/api/v1/red-flags/<int:red_flag_id>', view_func=red_flags_view, methods=['DELETE'])
        app.add_url_rule('/api/v1/auth/signup', view_func=signup, methods=['POST'] )