import random
from datetime import (datetime, timedelta)
from . import DAOException
from sqlalchemy.orm import load_only

from app import db
from app.models import (User, VerifyCode)
from app.encryption import hashpw


def create_secret_code():
    return ''.join(map(str, random.sample(range(9), 5)))


def save_model_user(usr, update_dict={}):
    if update_dict:
        if update_dict.get('id'):
            del update_dict['id']
        db.session.query(User).filter_by(id=usr.id).update(update_dict)
    else:
        db.session.add(usr)
    db.session.commit()


def create_user_code(user, code, code_type):
    verify_code = VerifyCode(code_type=code_type,
                             expiry_datetime=datetime.now() + timedelta(hours=1),
                             user=user)
    verify_code.code = code
    db.session.add(verify_code)
    db.session.commit()
    return verify_code


def get_user_code(user, code, code_type):
    # Get the most recent codes to try and reduce the
    # time searching for the correct code.
    codes = VerifyCode.query.filter_by(
        user=user, code_type=code_type).order_by(
            VerifyCode.created_at.desc())
    retval = None
    for x in codes:
        if x.check_code(code):
            retval = x
            break
    return retval


def use_user_code(id):
    verify_code = VerifyCode.query.get(id)
    verify_code.code_used = True
    db.session.add(verify_code)
    db.session.commit()


def delete_model_user(user):
    db.session.delete(user)
    db.session.commit()


def get_model_users(user_id=None):
    if user_id:
        return User.query.filter_by(id=user_id).one()
    return User.query.filter_by().all()
