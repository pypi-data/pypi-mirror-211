import bcrypt


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
