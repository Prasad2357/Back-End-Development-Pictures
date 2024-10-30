from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all picture URLs"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture['id'] == id:
            return jsonify(picture), 200

    # If not found, return a 404 error
    return jsonify({"message": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture_data = request.get_json()

    # Check if the required fields are in the incoming data
    if not picture_data or 'id' not in picture_data:
        return jsonify({"message": "Invalid picture data"}), 400

    # Check if a picture with the same ID already exists
    for picture in data:
        if picture['id'] == picture_data['id']:
            return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    # Append the new picture to the data list
    data.append(picture_data)

    # Optionally, you can return the newly created picture with a status code of 201
    return jsonify(picture_data), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_picture_data = request.get_json()

    # Check if the required fields are in the incoming data
    if not updated_picture_data:
        return jsonify({"message": "Invalid picture data"}), 400

    # Find the picture with the given ID in the data list
    for index, picture in enumerate(data):
        if picture['id'] == id:
            # Update the picture data with the incoming request
            data[index] = {**picture, **updated_picture_data}
            return jsonify(data[index]), 200  # Return the updated picture

    # If the picture with the specified ID is not found
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index, picture in enumerate(data):
        if picture['id'] == id:
            del data[index]  # Delete the picture from the list
            return "", 204  # Return an empty body with a 204 No Content status

    # If the picture with the specified ID is not found
    return jsonify({"message": "picture not found"}), 404
