from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.campaign import Campaign

campaign_bp = Blueprint("campaign", __name__)

@campaign_bp.route("/", methods=["POST"])

def create_campaign():
    data = request.get_json()
    user_id = get_jwt_identity()

    campaign = Campaign(
        brand_id=user_id,
        goal=data.get("goal"),
        platform=data.get("platform"),
        languages=data.get("languages"),
        budget=data.get("budget"),
        follower_range=data.get("follower_range")
    )

    db.session.add(campaign)
    db.session.commit()

    return jsonify({"message": "Campaign created"}), 201