from flask import Blueprint, jsonify

core_bp = Blueprint(
    "core_bp", __name__, template_folder="templates", static_folder="static"
)


@core_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Server is up and running!"}), 200
