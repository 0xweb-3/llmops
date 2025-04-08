from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Length


class CompletionRequest(FlaskForm):
    """基础聊天接口请求验证"""
    query = StringField('query',
                        validators=[DataRequired(message="问题必须填写"),
                                    Length(max=2000, message="最大2000个字")]
                        )
