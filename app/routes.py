from flask import Blueprint, jsonify, render_template
from .services import CloudService

main = Blueprint("main", __name__)
api = Blueprint("api", __name__)
service = CloudService()


@main.route("/")
def index():
    return render_template("index.html")


@api.route("/resources")
def resources():
    return jsonify(service.get_all_resources())


@api.route("/costs")
def costs():
    return jsonify(service.get_cost_summary())


@api.route("/optimisations")
def optimisations():
    return jsonify(service.get_optimisation_recommendations())


@api.route("/patterns")
def patterns():
    return jsonify(service.get_architecture_patterns())


@api.route("/health")
def health():
    return jsonify({"status": "ok", "version": "1.0.0"})
