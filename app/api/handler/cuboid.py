from http import HTTPStatus
from flask import Blueprint, jsonify, request
from app.api.model.cuboid import Cuboid
from app.api.model.bag import Bag
from app.api.schema.cuboid import CuboidSchema
from app.api.db import db

cuboid_api = Blueprint("cuboid_api", __name__)


@cuboid_api.route("/", methods=["GET"])
def list_cuboids():
    cuboid_ids = request.args.getlist("cuboid_id")
    cuboid_schema = CuboidSchema(many=True)
    cuboids = Cuboid.query.filter(Cuboid.id.in_(cuboid_ids)).all()

    return jsonify(cuboid_schema.dump(cuboids)), HTTPStatus.OK


@cuboid_api.route("/<int:cuboid_id>", methods=["GET"])
def get_cuboid():
    return "", HTTPStatus.OK


@cuboid_api.route("/", methods=["POST"])
def create_cuboid():
    content = request.json

    cuboid_schema = CuboidSchema()
    cuboid = Cuboid(
        width=content["width"],
        height=content["height"],
        depth=content["depth"],
        bag_id=content["bag_id"],
    )
    db.session.add(cuboid)
    db.session.commit()

    return jsonify(cuboid_schema.dump(cuboid)), HTTPStatus.CREATED


@cuboid_api.route("/update", methods=["POST"])
def update_cuboid():
    content = request.json
    status_code = HTTPStatus.OK
    cuboid_schema = CuboidSchema()

    cuboid = Cuboid.query.get(content["cuboid_id"])
    if not cuboid:
        return {}, HTTPStatus.NOT_FOUND

    cuboid.width = content["width"]
    cuboid.height = content["height"]
    cuboid.depth = content["depth"]
    cuboid.bag_id = content["bag_id"]
    bag = Bag.query.get(content["bag_id"])

    current_volume = 0
    for cubo in bag.cuboids:
        current_volume += cubo.width * cubo.height * cubo.depth

    if (
        bag.volume - current_volume
        >= content["width"] * content["height"] * content["depth"]
    ):

        cuboid.query.update(
            {
                "width": content["width"],
                "height": content["height"],
                "depth": content["depth"],
            }
        )
    else:
        status_code = HTTPStatus.UNPROCESSABLE_ENTITY

    db.session.commit()

    return (
        jsonify(cuboid_schema.dump(cuboid.query.get(content["cuboid_id"]))),
        status_code,
    )
