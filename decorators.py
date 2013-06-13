def user_required(func):
    def wrapper(*args):
        user = args[0].user
        if not user:
            args[0].redirect('/login/')
            return
        return func(*args)
    return wrapper
