"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

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
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():

    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }

    return jsonify(response_body), 200
    
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):

    member = jackson_family.get_member(member_id)

    if not member:
        return jsonify({"Error": "Member does not exist"}), 404

    return jsonify(member), 200    

@app.route('/member', methods=['POST'])
def add_member():

    request_data = request.get_json()
    added_member = {
    "first_name": request_data['first_name'],
    "age": request_data['age'],
    "lucky_numbers": request_data['lucky_numbers']
    }
    jackson_family.add_member(added_member)
    return jsonify(added_member), 200    

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):

    try:
        member_index = next(i for i, member in enumerate(jackson_family) if member['id'] == member_id)
        del jackson_family[member_index]

        return jsonify({'status': 'success', 'message': 'Member deleted successfully'}), 200
    except StopIteration:
        # Member not found
        return jsonify({'status': 'error', 'message': "Member with ID {member_id} not found"}), 404
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'status': 'error', 'message': "An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
