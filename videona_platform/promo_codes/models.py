# -*- coding: utf-8 -*-
"""
    videona_platform/promo_codes/models.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Promo Codes model
"""
from datetime import datetime
from videona_platform.core import db


class PromoCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    campaign = db.Column(db.String(50))
    redeemed = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    expires_at = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<PromoCode %s>' % self.code

