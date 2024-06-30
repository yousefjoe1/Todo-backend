from passlib.context import CryptContext

secur = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])

def get_password_hash(plain_text_password):
    return secur.hash(plain_text_password)

def verify_password(candidate_password,hashed_password):
    return secur.verify(candidate_password,hashed_password)