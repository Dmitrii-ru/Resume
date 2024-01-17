
import random


def random_posts(posts):
    random_count = 8
    if len(posts) < random_count:
        random_count = len(posts)
    return random.sample(list(posts), random_count)
