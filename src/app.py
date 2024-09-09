import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route("/")
def sitemap():
    return generate_sitemap(app)


@app.route("/members", methods=["GET"])
def show_members():
    try:
        members = jackson_family.get_all_members()
        response_body = {"family": members}
        return jsonify(response_body), 200
    except Exception as e:
        raise APIException(
            f"An error occurred while retrieving members: {str(e)}", status_code=500
        )


@app.route("/members", methods=["POST"])
def create_member():
    try:
        request_json = request.json

        if not request_json.get("name") or not request_json["name"].isalpha():
            raise APIException(
                "First name must contain only alphabetic characters and cannot be empty",
                status_code=400,
            )

        if (
            not request_json.get("age")
            or not str(request_json["age"]).isdigit()
            or int(request_json["age"]) <= 0
        ):
            raise APIException(
                "Age must be a positive integer and cannot be empty", status_code=400
            )

        if (
            not request_json.get("lucky_numbers")
            or len(request_json["lucky_numbers"]) <= 0
        ):
            raise APIException(
                "Lucky numbers must be a list of positive integers and cannot be empty",
                status_code=400,
            )

        new_member = jackson_family.add_member(request_json)
        return jsonify(new_member), 201
    except APIException as api_error:
        raise api_error
    except Exception as e:
        raise APIException(
            f"An error occurred while creating the member: {str(e)}", status_code=500
        )


@app.route("/members/<int:id>", methods=["DELETE"])
def delete_member(id):
    try:
        erase_member = jackson_family.delete_member(id)
        if erase_member is None:
            raise APIException(
                f"No such family member, cannot delete member with id {id}",
                status_code=404,
            )
        return jsonify({"msg": "Member deleted successfully", "id": id}), 200
    except APIException as api_error:
        raise api_error
    except Exception as e:
        raise APIException(
            f"An error occurred while deleting the member: {str(e)}", status_code=500
        )


@app.route("/member/<int:id>", methods=["GET"])
def show_member(id):
    try:
        member = jackson_family.get_member(id)
        if member is None:
            raise APIException(
                f"Cannot find family member with id {id}", status_code=404
            )
        return jsonify(member), 200
    except APIException as api_error:
        raise api_error
    except Exception as e:
        raise APIException(
            f"An error occurred while retrieving the member: {str(e)}", status_code=500
        )


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
