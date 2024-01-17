import rules


@rules.predicate
def is_author(user, obj, *args):
    return obj.author == user


@rules.predicate
def is_user_authenticated(user):
    return user.is_authenticated


@rules.predicate
def is_odj_private(user, obj):

    if obj.is_privat:
        return obj.author == user
    return True


rules.add_perm('is_author', is_author)
rules.add_perm('is_user_authenticated', is_user_authenticated)
rules.add_perm('is_odj_private', is_odj_private)
