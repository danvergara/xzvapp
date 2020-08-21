"""app.py"""
import os

from flask import Flask, jsonify, request
import boto3

app = Flask(__name__)

USERS_TABLE = os.environ.get("USER_TABLE", "users")
IS_OFFLINE = os.environ.get('IS_OFFLINE')


def client():
    """returns a s3 bucket"""
    if IS_OFFLINE:
        return boto3.client(
            'dynamodb',
            region_name='localhost',
            endpoint_url='http://localhost:8000'
        )
    else:
        return boto3.client('dynamodb')


@app.route("/")
def index():
    """index"""
    return "ok"


@app.route("/users/<string:user_id>")
def get_user(user_id):
    """
    Get a user from the dynamodb
    """
    resp = client().get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': {'S': user_id}
        }
    )
    item = resp.get('Item')
    if item is None:
        return jsonify({'error': 'User does not exist'}), 404

    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S')
    })


@app.route("/users", methods=["POST"])
def create_user():
    """
    create a user in dynamodb
    """
    user_id = request.json.get('userId')
    name = request.json.get('name')
    if not user_id or not name:
        return jsonify({'error': 'Please provide userId and name'}), 400

    client().put_item(
        TableName=USERS_TABLE,
        Item={
            'userId': {'S': user_id},
            'name': {'S': name}
        }
    )

    return jsonify({
        'userId': user_id,
        'name': name
    })


@app.route("/users/<string:user_id>", methods=["PATCH"])
def update_user(user_id):
    """
    Update a user from the dynamodb
    """
    name = request.json.get('name')

    resp = client().get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': {'S': user_id}
        }
    )

    item = resp.get('Item')
    if item is None:
        return jsonify({'error': 'User does not exist'}), 404

    resp = client().update_item(
        TableName=USERS_TABLE,
        Key={
            'userId': {'S': user_id}
        },
        AttributeUpdates={
            'name': {'S': name}
        },
    )

    attrs = resp.get('Attributes')
    if attrs is None:
        return jsonify({'error': 'Something went wrong'}), 500

    return jsonify({
        'userId': attrs.get('userId').get('S'),
        'name': attrs.get('name').get('S')
    })


@app.route("/users/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete a user from the dynamodb
    """
    resp = client().get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': {'S': user_id}
        }
    )
    item = resp.get('Item')
    if item is None:
        return jsonify({'error': 'User does not exist'}), 404

    resp = client().delete_item(
        TableName=USERS_TABLE,
        Key={
            'userId': {'S': user_id}
        },
    )

    attrs = resp.get('Attributes')
    if attrs is None:
        return jsonify({'error': 'Something went wrong'}), 500

    return jsonify({
        'userId': attrs.get('userId').get('S'),
        'name': attrs.get('name').get('S')
    })
