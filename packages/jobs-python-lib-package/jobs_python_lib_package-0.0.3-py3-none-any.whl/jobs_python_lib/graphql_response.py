class GraphQLResponse:
    def __init__(self, success: bool, payload) -> None:
        self.success = success
        self.payload = payload

    def __iter__(self):
        yield 'success', self.success
        yield 'payload', self.payload

    def as_dict(self):
        return dict(self)


class GraphQLError:
    def __init__(self, error) -> None:
        self.error = error

    def response(self) -> dict:
        data = {
            'errorMessage': self.get_error_message(),
            'errorType': type(self.error).__name__,
            'errorData': None
        }

        return GraphQLResponse(False, data).as_dict()

    def get_error_message(self):
        return str(self.error)