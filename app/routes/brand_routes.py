from flask import Blueprint, request, jsonify
from app import db
from app.models.brand import BrandProfile
from app.models.campaign import Campaign
from app.utils.excel import save_to_excel
from app.utils.validators import validate_brand

brand_bp = Blueprint("brand", __name__)


# ─────────────────────────────────────────────────────────────
# SUBMIT BRAND + CAMPAIGN
# ─────────────────────────────────────────────────────────────
@brand_bp.route("/profile", methods=["POST"])
def submit_brand_profile():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate
        error = validate_brand(data)
        if error:
            return jsonify({"error": error}), 400

        company_name = data.get("company_name")

        # ✅ CHECK BEFORE INSERT
        existing = BrandProfile.query.filter_by(company_name=company_name).first()
        if existing:
            return jsonify({"error": "Brand already exists"}), 400

        # STEP 1: Create profile
        profile = BrandProfile(
            user_id=None,  # keep nullable
            name=data.get("name"),
            company_name=company_name,
            phone=data.get("phone")
        )

        db.session.add(profile)
        db.session.flush()

        # STEP 2: Create campaign
        campaign = Campaign(
            brand_id=profile.id,
            goal=data.get("goal"),
            platform=data.get("platform"),
            languages=data.get("languages") or [],
            budget=data.get("budget"),
            follower_range=data.get("follower_range")
        )

        db.session.add(campaign)
        db.session.commit()

        # ✅ Safe Excel write
        try:
            save_to_excel(
                "Brands",
                [
                    "Name", "Company", "Phone",
                    "Goal", "Platform", "Languages",
                    "Budget", "Follower Range"
                ],
                [
                    profile.name,
                    profile.company_name,
                    profile.phone,
                    campaign.goal,
                    campaign.platform,
                    ", ".join(campaign.languages or []),
                    campaign.budget,
                    campaign.follower_range
                ]
            )
        except Exception as e:
            print("Excel Error:", str(e))

        return jsonify({
            "message": "Submitted successfully",
            "data": {
                "profile": {
                    "name": profile.name,
                    "company_name": profile.company_name,
                    "phone": profile.phone
                },
                "campaign": {
                    "goal": campaign.goal,
                    "platform": campaign.platform,
                    "languages": campaign.languages,
                    "budget": campaign.budget,
                    "follower_range": campaign.follower_range
                }
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────────────────────
# GET ALL CAMPAIGNS
# ─────────────────────────────────────────────────────────────
@brand_bp.route("/campaigns", methods=["GET"])
def get_campaigns():
    try:
        campaigns = Campaign.query.all()

        return jsonify([
            {
                "id": c.id,
                "goal": c.goal,
                "platform": c.platform,
                "budget": c.budget
            } for c in campaigns
        ])

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Internal server error"}), 500


# ─────────────────────────────────────────────────────────────
# GET BRAND PROFILE
# ─────────────────────────────────────────────────────────────
@brand_bp.route("/me", methods=["GET"])
def get_brand():
    try:
        company = request.args.get("company")

        if not company:
            return jsonify({"error": "Company is required"}), 400

        profile = BrandProfile.query.filter_by(company_name=company).first()

        if not profile:
            return jsonify({"error": "Brand not found"}), 404

        campaign = Campaign.query.filter_by(brand_id=profile.id).first()

        return jsonify({
            "profile": {
                "name": profile.name,
                "company": profile.company_name
            },
            "campaign": {
                "goal": campaign.goal if campaign else None,
                "budget": campaign.budget if campaign else None
            }
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Internal server error"}), 500