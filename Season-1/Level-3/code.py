import os
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    TaxPayer('foo', 'bar').get_tax_form_attachment(request.args["input"])
    TaxPayer('foo', 'bar').get_prof_picture(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

class TaxPayer:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.prof_picture = None
        self.tax_form_attachment = None

    # Returns the path of an optional profile picture that users can set.
    def get_prof_picture(self, path=None):
        # Setting a profile picture is optional.
        if not path:
            return None

        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Build the full path using the base directory regardless of user input.
        prof_picture_path = os.path.normpath(os.path.join(base_dir, path))
        # Ensure that the resolved path is within the base directory.
        if not prof_picture_path.startswith(base_dir):
            return None

        try:
            with open(prof_picture_path, 'rb') as pic:
                picture = bytearray(pic.read())
        except IOError:
            return None

        return prof_picture_path

    # Returns the path of an attached tax form that every user should submit.
    def get_tax_form_attachment(self, path=None):
        if not path:
            raise Exception("Error: Tax form is required for all users")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Build the full path using the base directory.
        attachment_path = os.path.normpath(os.path.join(base_dir, path))
        # Ensure that the resolved path is within the base directory.
        if not attachment_path.startswith(base_dir):
            return None

        try:
            with open(attachment_path, 'rb') as form:
                tax_data = bytearray(form.read())
        except IOError:
            return None

        return attachment_path
