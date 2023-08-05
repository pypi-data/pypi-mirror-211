class ThrivveCore:
    __app = None

    @staticmethod
    def get_app():
        """ Static access method. """
        if ThrivveCore.__app == None:
            ThrivveCore()
        return ThrivveCore.__app

    def __init__(self, app=None):
        """ Virtually private constructor. """
        if ThrivveCore.__app != None:
            raise Exception("This class is a singleton!")
        else:
            ThrivveCore.__app = app
            setup_default_routes(app)


def setup_default_routes(app):
    from thrivve_core.app_decorators.app_entry import route
    from thrivve_core.helpers.fetch_relational_data import fetch_relational_data
    @route(
        path='/',
        require_auth=False
    )
    def _health_check_service():
        return dict(name="{} Service".format(app.config.get('SERVICE_NAME')), works=True)

    @route(
        path='/health_check',
        require_auth=False
    )
    def _health_check_with_path_service():
        return dict(name="{} Service".format(app.config.get('SERVICE_NAME')), works=True)

    @route("/fetch_relational_data", methods=["POST"], require_auth=False)
    def _fetch_relational_data_service(validated_data):
        """
        Swagger definition
        """
        return fetch_relational_data(**validated_data)
