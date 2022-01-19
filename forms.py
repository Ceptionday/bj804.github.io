# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, FileField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    username = StringField("用户名：", validators=[DataRequired()])
    password = PasswordField("密码：", validators=[DataRequired()])
    confirm_password = PasswordField("确认密码：", validators=[DataRequired()])
    # password18 = PasswordField("验证码（输入网址：http://silenthill.python-site.com/register_password来获取验证码。验证码将发到您的邮箱里）：", validators=[Required()])
    submit = SubmitField("立即注册")


class LoginForm(FlaskForm):
    value = StringField("请输入用户名：", validators=[DataRequired()])
    password = PasswordField("请输入密码：", validators=[DataRequired()])
    submit = SubmitField("登录")


class ArticleForm(FlaskForm):
    title = StringField("请输入标题：", validators=[DataRequired()])
    content = TextAreaField("请输入内容：", validators=[DataRequired()])
    submit = SubmitField("发布")

class Net(FlaskForm):
    net = StringField("网址（请输入http://或https://开头的网址）：")
    submit = SubmitField("跳转")


class InfoForm(FlaskForm):
    address = StringField("地址：")
    info = TextAreaField("个人介绍：")
    submit = SubmitField("提交信息")
