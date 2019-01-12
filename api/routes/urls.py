from api.auth.signin import Signin
from api.auth.signup import Signup
from api.views.red_flags_view import RedFlagsView
from api.views.users_view import UsersView
from api.views.interventions_view import InterventionsView


class Routes:
    
    
    @staticmethod
    def fetch_urls(app):
        red_flags_view = RedFlagsView.as_view('redflag')
        signup = Signup.as_view('signup')
        signin = Signin.as_view('signin')
        users_view = UsersView.as_view('user')
        interventions_view = InterventionsView.as_view('intervention')

        app.add_url_rule('/api/v1/red-flags', defaults={'red_flag_id':None}, view_func=red_flags_view, methods=['GET'])
        app.add_url_rule('/api/v1/red-flags/<int:red_flag_id>', view_func=red_flags_view, methods=['GET'])
        app.add_url_rule('/api/v1/red-flags', view_func=red_flags_view, methods=['POST'])
        app.add_url_rule('/api/v1/red-flags/<int:red_flag_id>/location', view_func=red_flags_view, methods=['PUT'])
        app.add_url_rule('/api/v1/red-flags/<int:red_flag_id>/comment', view_func=red_flags_view, methods=['PUT'])
        app.add_url_rule('/api/v1/red-flags/<int:red_flag_id>', view_func=red_flags_view, methods=['DELETE'])
        app.add_url_rule('/api/v1/auth/signup', view_func=signup, methods=['POST'])
        app.add_url_rule('/api/v1/auth/signin', view_func=signin, methods=['POST'])
        app.add_url_rule('/api/v1/users', view_func=users_view, methods=['GET'])
        app.add_url_rule('/api/v1/users/<int:user_id>', view_func=users_view, methods=['GET'])
        app.add_url_rule('/api/v1/interventions', defaults={'intervention_id':None}, view_func=interventions_view, methods=['GET'])
        app.add_url_rule('/api/v1/interventions/<int:intervention_id>', view_func=interventions_view, methods=['GET'])
        app.add_url_rule('/api/v1/interventions', view_func=interventions_view, methods=['POST'])
        