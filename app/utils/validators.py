def validate_brand(data):
    required = ["name", "company_name", "goal", "platform", "budget"]
    for field in required:
        if not data.get(field):
            return f"{field} is required"
    return None


def validate_influencer(data):
    required = ["full_name", "platform", "username", "followers"]
    for field in required:
        if not data.get(field):
            return f"{field} is required"
    return None