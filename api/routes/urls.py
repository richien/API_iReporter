from api.auth.signin import Signin
from api.auth.signup import Signup
from api.views.red_flags_view import RedFlagsView
from api.views.users_view import UsersView
from api.views.interventions_view import InterventionsView
from api.views.user_incidents import UserRedFlagsView, UserInterventionsView
from api.views.update_incidents import UpdateRedFlagStatusView, UpdateInterventionStatusView, UpdateInterventionCommentView
from api.views.update_incidents import UpdateRedFlagCommentView, UpdateInterventionLocationView, UpdateRedFlagLocationView

class Routes:

    @staticmethod
    def fetch_urls(app):
        red_flags_view = RedFlagsView.as_view('redflag')
        signup = Signup.as_view('signup')
        signin = Signin.as_view('signin')
        users_view = UsersView.as_view('user')
        interventions_view = InterventionsView.as_view('intervention')
        user_red_flags_view = UserRedFlagsView.as_view('user_redflags')
        user_interventions_view = UserInterventionsView.as_view('user_interventions')
        update_red_flag_status_view = UpdateRedFlagStatusView.as_view('update_redflag_status')
        update_intervention_status_view = UpdateInterventionStatusView.as_view('update_intervention_status')
        update_intervention_comment_view = UpdateInterventionCommentView.as_view('update_intervention_comment')
        update_redflag_comment_view = UpdateRedFlagCommentView.as_view('update_redflag_comment')
        update_intervention_location_view = UpdateInterventionLocationView.as_view('update_intervention_location')
        update_redflag_location_view = UpdateRedFlagLocationView.as_view('update_redflag_location')

        app.add_url_rule(
            '/api/v1/red-flags',
            defaults={'red_flag_id': None},
            view_func=red_flags_view,
            methods=['GET'])
        app.add_url_rule(
            '/api/v1/red-flags/<int:red_flag_id>',
            view_func=red_flags_view, 
            methods=['GET'])
        app.add_url_rule(
            '/api/v1/red-flags',
            view_func=red_flags_view, 
            methods=['POST'])
        app.add_url_rule(
            '/api/v1/red-flags/<int:incident_id>/location',
            view_func=update_redflag_location_view, 
            methods=['PATCH'])
        app.add_url_rule(
            '/api/v1/red-flags/<int:incident_id>/comment',
            view_func=update_redflag_comment_view, 
            methods=['PATCH'])
        app.add_url_rule(
            '/api/v1/red-flags/<int:incident_id>/status',
            view_func=update_red_flag_status_view, 
            methods=['PATCH'])
        app.add_url_rule(
            '/api/v1/red-flags/<int:red_flag_id>',
            view_func=red_flags_view, 
            methods=['DELETE'])
        app.add_url_rule(
            '/api/v1/red-flags/<int:user_id>/users',
            view_func=user_red_flags_view, 
            methods=['GET'])
        app.add_url_rule(
            '/api/v1/auth/signup',
            view_func=signup, 
            methods=['POST'])
        app.add_url_rule(
            '/api/v1/auth/login',
            view_func=signin, 
            methods=['POST'])
        app.add_url_rule(
            '/api/v1/users', 
            view_func=users_view, 
            methods=['GET'])
        app.add_url_rule(
            '/api/v1/users/<int:user_id>',
            view_func=users_view, 
            methods=['GET'])
        app.add_url_rule(
            '/api/v1/interventions',
            defaults={'intervention_id': None},
            view_func=interventions_view,
            methods=['GET'])
        app.add_url_rule(
            '/api/v1/interventions/<int:intervention_id>',
            view_func=interventions_view, 
            methods=['GET'])
        app.add_url_rule(
            '/api/v1/interventions',
            view_func=interventions_view, 
            methods=['POST'])
        app.add_url_rule(
            '/api/v1/interventions/<int:incident_id>/location',
            view_func=update_intervention_location_view, 
            methods=['PATCH'])
        app.add_url_rule(
            '/api/v1/interventions/<int:incident_id>/comment',
            view_func=update_intervention_comment_view, 
            methods=['PATCH']),
        app.add_url_rule(
            '/api/v1/interventions/<int:incident_id>/status',
            view_func=update_intervention_status_view, 
            methods=['PATCH'])
        app.add_url_rule(
            '/api/v1/interventions/<int:intervention_id>',
            view_func=interventions_view, 
            methods=['DELETE'])
        app.add_url_rule(
            '/api/v1/interventions/<int:user_id>/users',
            view_func=user_interventions_view, 
            methods=['GET']) 
