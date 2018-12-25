from api.views.red_flags_view import RedFlagsView


class Routes:
    
    @staticmethod
    def fetch_urls(app):
        red_flags_view = RedFlagsView.as_view('redflag')
        app.add_url_rule('/api/v1/red-flags', defaults={'red_flag_id':None},
                            view_func=red_flags_view, methods=['GET'])
        app.add_url_rule('/api/v1/red-flags/<int:red_flag_id>', view_func=red_flags_view, methods=['GET'])
        app.add_url_rule('/api/v1/red-flags', view_func=red_flags_view, methods=['POST'])