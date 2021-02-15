from dataclasses import fields, asdict

import datatypes

__all__ = ['count_avg_rating']


def count_avg_rating(reviews: list[datatypes.Review]) -> dict:
    """Count average user's rating dict from reviews."""
    avg_rating = {field.name: 0 for field in fields(datatypes.Rating)}
    for review in reviews:
        rating_dict = asdict(review.rating)
        for rate, amount in rating_dict.items():
            avg_rating[rate] += amount

    reviews_amount = len(reviews) or 1
    for rate, amount in avg_rating.items():
        avg_rating[rate] /= reviews_amount

    return avg_rating
