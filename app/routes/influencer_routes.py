from flask import Blueprint, request, jsonify
from app import db
from app.models.influencer import InfluencerProfile
from app.models.audience import Audience
from app.models.partnership import Partnership
from app.utils.excel import save_to_excel
from app.utils.validators import validate_influencer

influencer_bp = Blueprint("influencer", __name__)


# ─────────────────────────────────────────────────────────────
# APPLY ROUTE
# ─────────────────────────────────────────────────────────────
@influencer_bp.route("/apply", methods=["POST"])
def apply_influencer():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate input
        error = validate_influencer(data)
        if error:
            return jsonify({"error": error}), 400

        email = data.get("email")

        # ✅ CHECK BEFORE INSERT
        existing = InfluencerProfile.query.filter_by(email=email).first()
        if existing:
            return jsonify({"error": "Profile already exists"}), 400

        # ✅ SAFE NUMBER CONVERSION
        followers = int(data.get("followers") or 0)
        avg_views = int(data.get("avg_views") or 0)

        # STEP 1: Profile
        profile = InfluencerProfile(
            user_id=None,
            full_name=data.get("full_name"),
            email=email,
            platform=data.get("platform"),
            username=data.get("username"),
            profile_link=data.get("profile_link"),
            phone=data.get("phone")
        )

        db.session.add(profile)
        db.session.flush()

        # STEP 2: Audience
        audience = Audience(
            influencer_id=profile.id,
            followers=followers,
            avg_views=avg_views,
            genres=data.get("genres") or [],
            languages=data.get("languages") or []
        )

        db.session.add(audience)

        # STEP 3: Partnership
        partnership = Partnership(
            influencer_id=profile.id,
            experience=data.get("experience"),
            fee=data.get("fee"),
            categories=data.get("categories") or [],
            long_term=bool(data.get("long_term"))
        )

        db.session.add(partnership)

        db.session.commit()

        # ✅ SAFE EXCEL SAVE (won’t crash API)
        try:
            save_to_excel(
                "Influencers",
                [
                    "Name", "Email", "Platform", "Username",
                    "Followers", "Avg Views", "Genres", "Languages",
                    "Experience", "Fee", "Categories", "Long Term"
                ],
                [
                    profile.full_name,
                    profile.email,
                    profile.platform,
                    profile.username,
                    audience.followers,
                    audience.avg_views,
                    ", ".join(audience.genres or []),
                    ", ".join(audience.languages or []),
                    partnership.experience,
                    partnership.fee,
                    ", ".join(partnership.categories or []),
                    str(partnership.long_term)
                ]
            )
        except Exception as excel_error:
            print("Excel Error:", str(excel_error))

        return jsonify({
            "message": "Application submitted",
            "data": {
                "profile": {
                    "full_name": profile.full_name,
                    "email": profile.email,
                    "platform": profile.platform,
                    "username": profile.username
                },
                "audience": {
                    "followers": audience.followers,
                    "avg_views": audience.avg_views,
                    "genres": audience.genres,
                    "languages": audience.languages
                },
                "partnership": {
                    "experience": partnership.experience,
                    "fee": partnership.fee,
                    "categories": partnership.categories,
                    "long_term": partnership.long_term
                }
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────────────────────
# GET PROFILE
# ─────────────────────────────────────────────────────────────
@influencer_bp.route("/me", methods=["GET"])
def get_profile():
    try:
        email = request.args.get("email")

        if not email:
            return jsonify({"error": "Email is required"}), 400

        profile = InfluencerProfile.query.filter_by(email=email).first()

        if not profile:
            return jsonify({"error": "Profile not found"}), 404

        audience = Audience.query.filter_by(influencer_id=profile.id).first()
        partnership = Partnership.query.filter_by(influencer_id=profile.id).first()

        return jsonify({
            "profile": {
                "name": profile.full_name,
                "platform": profile.platform,
                "username": profile.username
            },
            "audience": {
                "followers": audience.followers if audience else 0,
                "avg_views": audience.avg_views if audience else 0
            },
            "partnership": {
                "fee": partnership.fee if partnership else None
            }
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500