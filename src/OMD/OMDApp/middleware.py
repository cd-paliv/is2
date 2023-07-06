class DeleteSessionVariableMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Delete the session variable after each request
        if request.session.get('show_finalized_turn_visited'):
            del request.session['show_finalized_turn_visited']
        return response