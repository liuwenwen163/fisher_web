# encoding: utf-8
"""
验证url传入参数的有效性
"""
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired

class SearchForm(Form):
    q = StringField(validators=[DataRequired(), Length(min=1, max=20)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)
