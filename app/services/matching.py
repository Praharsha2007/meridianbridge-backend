def match_influencers(campaign, influencers):
    results = []

    for inf in influencers:
        score = 0

        # Match platform
        if inf.platform == campaign.platform:
            score += 1

        # Match language
        if set(inf.languages or []).intersection(campaign.languages or []):
            score += 1

        # Match category/genre
        if set(inf.genres or []).intersection(campaign.languages or []):
            score += 1

        results.append((inf, score))

    return sorted(results, key=lambda x: x[1], reverse=True)