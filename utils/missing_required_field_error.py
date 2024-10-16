"""Exception raised for custom error in the application."""
from flask import jsonify


class CustomError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"

    def jsonify(self):
        return jsonify(self.message, status=400, mimetype='application/json')

    def message(self):
        return self.message

    def error_code(self):
        return self.error_code