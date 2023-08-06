class HttpResponseException(Exception):
    def __init__(self, status, statusText, body):
        super().__init__(f"HTTP Error Response: {status} {statusText}")
        self.status = status
        self.statusText = statusText
        self.body = body

    def to_json(self):
        return {
            'status': self.status,
            'statusText': self.statusText,
            'message': self.body['message'] if self.body and 'message' in self.body.keys() else None,
            'body': self.body,
        }
