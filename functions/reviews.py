from typing import List


def count_avg_rating(reviews: List[dict]) -> dict:
    quality, contact, terms = 0, 0, 0
    for review in reviews:
        rating = review['rating']
        quality += rating['quality']
        contact += rating['contact']
        terms += rating['terms']

    reviews_amount = len(reviews) or 1
    quality /= reviews_amount
    contact /= reviews_amount
    terms /= reviews_amount
    return {
        'quality': round(quality, 1),
        'contact': round(contact, 1),
        'terms': round(terms, 1)
    }
