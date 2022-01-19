# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request, session, current_app
from flask_bootstrap import Bootstrap
from forms import UserForm, LoginForm, ArticleForm, InfoForm, Net
from model import User, Article, Comment
from exts import db
import os
import random
from hello_time import hello_time_hour
word = ['不要只为一时的气氛，搞一肚子的气愤', '我可以给你我们的数据库文件，但你可能也不会用！', '你能用输入法打出 瓅 这个字的简笔吗？', '逐梦，无惧', '观三国烽烟，识梁山好汉，叹取经艰难，惜红楼梦断', '夕阳西下，断肠人在天涯。', '一曲新词酒一杯，去年天气旧亭台。夕阳西下几时回？无可奈何花落去，似曾相识燕归来。小园香径独徘徊。', '我独自在河边彳亍， 走走停停， 走走停停。', '你认识biǎng字吗？', 'Gospel of dismay!!!', '我就在那不冷不热的地方等着你！！！', '"a × b 是否一定等于 b × a"?', '"e ^ π ? π ^ e"   ?']
word_len = len(word)

app = Flask(__name__)
bootstrap = Bootstrap(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{os.path.join(basedir, 'database.sqlite')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


# app.config['MAIL_SERVER'] = 'smtp.qq.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USERNAME'] = '2395319863@qq.com'
# app.config['MAIL_PASSWORD'] = 'Nicholas007'
# mail = Mail(app)
# mail.init_app(app)
# YZM = random.randint(100000, 999999)

db.init_app(app)
@app.route("/")
def index():
    db.create_all()
    if session.get('user_id'):
        tip = ''
        user = User.query.filter_by(id=session.get("user_id")).first().username
        if hello_time_hour >= 23 or hello_time_hour <= 4:
            tip = '~时间不早了，该睡觉了！'
        elif hello_time_hour <= 8:
            tip = '~早上好~'
        elif hello_time_hour <= 11:
            tip = '~上午好~'
        elif hello_time_hour <= 13:
            tip = '~中午好~'
        elif hello_time_hour <= 17:
            tip = '~下午好~'
        elif hello_time_hour <= 23:
            tip = '~晚上好~'
        words = random.choice(word)
        return render_template('index02.html', tip=tip, user=user, words=words)

    return render_template('index.html')

# @app.route('/register_password')
# def register_password():
#     msg = Message(subject='验证码为：' + YZM + '，请尽快登录，防止验证码泄露。',
#                   recipients=register.real_email)
#     mail.send(msg)

@app.route("/blog")
def blog():
    if session.get('user_id'):
        articles = Article.query.all()
        return render_template("blog.html", articles=articles[::-1])
    else:
        return redirect(url_for('login'))
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    tip = ""
    if request.method == "POST":
        value = form.value.data
        password = form.password.data
        user1 = User.query.filter_by(username=value).first()
        if user1 and password == user1.password:
            session["user_id"] = user1.id
            session.permanent = True
            return redirect(url_for("index"))
        else:
            tip = "账号或密码输入错误，请确定后再登录！"
    return render_template("login.html", form=form, tip=tip)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = UserForm()
    tip = ""
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        # email = form.email.data
        # yzm = form.password18.data
        confirm_password = form.confirm_password.data
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            tip = "用户名已存在！"
        elif password != confirm_password:
            tip = "两次密码不一致，请核对后再填写！"
        # elif re.match('^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email) == None:
            # tip = '邮箱号码输入错误，请确定后再输入！'
        # elif yzm != YZM:
        #     tip = '验证码错误！'
        else:
            # real_email = email
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
    return render_template("register.html", form=form, tip=tip)


# @app.route('/adding', methods=['GET', 'POST'])
# def adding():
#     if session.get('user_id'):
#         form = Adding()
#         if request.method == 'POST':
#             add = request.form.get('add')
#             word.append(add)
#             word_ = join.join(word)
#             return render_template('public_tip.html', word_len=word_len, word_screen=word_)
#         return render_template('adding.html', form=form)
#     else:
#         return redirect(url_for('login'))
#
# @app.route('/delete_words', methods=['GET', 'POST'])
# def delete_words():
#     if session.get('user_id'):
#         form = Delete()
#         if request.method == 'POST':
#             delete = request.form.get('delete')
#             tip = ''
#             try:
#                 word.remove(delete)
#             except ValueError:
#                 tip = '存储表中没有这段文字！'
#                 return render_template('delete_wrong.html', tip=tip)
#             word_ = join.join(word)
#             return render_template('public_tip.html', word_len=word_len, word_screen=word_)
#         return render_template('delete.html', form=form)
#     else:
#         return redirect(url_for('login'))


@app.route("/logout")
def logout():
    if session.get("user_id"):
        session.pop("user_id")
    return redirect(url_for("index"))


@app.route("/article", methods=["GET", "POST"])
def article():
    if session.get("user_id"):
        form = ArticleForm()
        if request.method == "POST":
            text = ""
            content = form.content.data.replace(" ", "__S__").split()
            for t in content:
                text += t + "__N__"
            article = Article(title=form.title.data, content=text)
            article.author_id = session.get("user_id")
            db.session.add(article)
            db.session.commit()
            return redirect(url_for("blog"))
        else:
            return render_template("article.html", form=form)
    else:
        return redirect(url_for("login"))


@app.route("/detail/<article_id>")
def detail(article_id):
    if session.get("user_id"):
        article = Article.query.filter_by(id=article_id).first()
        return render_template("detail.html", article=article)
    else:
        return redirect(url_for("login"))

@app.route('/search_author/')
def search_author():
    if session.get('user_id'):
        A = request.args.get('A')
        if User.query.filter(User.username.contains(A)).first():
            author = User.query.filter(User.username.contains(A))
            articles = Article.query.filter(Article.author_id == author[0].id).all()
            count = len(articles)
            if (count == 0):
                colors = '#BFBFBF'
            if (count > 0 and count < 20):
                colors = '#3498DB'
            if (count >= 20 and count < 50):
                colors = '#52C41A'
            if (count >= 50 and count < 100):
                colors = '#F39C11'
            if (count >= 100):
                colors = '#FE4C61'
            user = User.query.filter_by(id=author[0].id).first()
            if user.username == '韩天浩' or user.username == 'test1' or user.username == 'Ceptionday':
                colors = '#9D3DCF'
            return render_template('user_detail.html', user=author[0], articles=articles, count=count, colors=colors)
        else:
            return render_template('user_detail_wrong.html')
    else:
        return redirect(url_for('login'))
@app.route('/quick_search_form', methods=['GET', 'POST'])
def quick_search_form():
    form = Net()
    if request.method == 'POST':
        url = request.form.get("net")
        return render_template('quick_search.html', url=url)
    return render_template('quick_search_index.html', form=form)
@app.route("/comment", methods=["GET", "POST"])
def comment():
    if session.get("user_id"):
        content = request.form.get("comment_content").replace(" ", "__S__").split()
        text = ""
        for t in content:
            text += t + "__N__"
        comment = Comment(article_id=request.form.get("article_id"), content=text)
        comment.author_id = session.get("user_id")
        db.session.add(comment)
        db.session.commit()
        article_id = request.form.get("article_id")
        return redirect(url_for("detail", article_id=article_id))
    else:
        return redirect(url_for("index"))


@app.route("/delete/<article_id>")
def delete(article_id):
    if Article.query.filter_by(id=article_id).first().author_id == session.get("user_id"):
        article = Article.query.filter_by(id=article_id).first()
        comments = Comment.query.filter_by(article_id=article_id)
        for comment in comments:
            db.session.delete(comment)
        db.session.delete(article)
        db.session.commit()
    return redirect(url_for("blog"))


@app.route("/delete_comment/<comment_id>")
def delete_comment(comment_id):
    if Comment.query.filter_by(id=comment_id).first().author_id == session.get("user_id"):
        comment = Comment.query.filter_by(id=comment_id).first()
        article_id = comment.article_id
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for("detail", article_id=article_id))


@app.route("/search/<pitch_on>")
def search(pitch_on):
    q = request.args.get("q")
    counts = [
        len(Article.query.filter(Article.title.contains(q)).all()),
        len(Article.query.filter(Article.content.contains(q)).all())
    ]
    if pitch_on == "0":
        articles = Article.query.filter(Article.title.contains(q)).all()
    elif pitch_on == "1":
        articles = Article.query.filter(Article.content.contains(q)).all()
    else:
        articles = []

    return render_template("search.html", articles=articles, pitch_on=pitch_on, q=q, counts=counts)


@app.route("/user_detail/<user_id>", methods=["GET", "POST"])
def user_detail(user_id):
    i = 0
    form = UserForm()
    articles = Article.query.filter_by(author_id=user_id).all()
    if (len(articles) == 0):
        colors = '#BFBFBF'
    if (len(articles) > 0 and len(articles) < 20):
        colors = '#3498DB'
    if (len(articles) >= 20 and len(articles) < 50):
        colors = '#52C41A'
    if (len(articles) >= 50 and len(articles) < 100):
        colors = '#F39C11'
    if (len(articles) >= 100):
        colors = '#FE4C61'
    user = User.query.filter_by(id=user_id).first()
    if user.username == '韩天浩' or user.username == 'test1' or user.username == 'Ceptionday':
        colors = '#9D3DCF'
    return render_template("user_detail.html", user=user, articles=articles, colors=colors)

@app.route("/level")
def level():
    return render_template("level.html")
@app.route("/edit_info/<user_id>", methods=["GET", "POST"])
def edit_info(user_id):
    if str(session.get("user_id")) == user_id:
        user = User.query.filter_by(id=user_id).first()
        info = user.info
        if info:
            info = user.info.replace("__N__", "\n").replace("__S__", " ")
        form = InfoForm(address=user.address, info=info)
        tip = ""
        if request.method == "POST":
            user.address = request.form.get("address")
            text = "__N__"
            for t in request.form.get("info").replace(" ", "__S__").split():
                text += t + "__N__"
            user.info = text
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user_detail", user_id=user_id))
        return render_template("edit_info.html", user=user, form=form, tip=tip)
    else:
        return redirect(url_for("index"))


@app.context_processor
def my_context_processor():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        if user:
            return {"um": user}
    return {}
@app.errorhandler(404)
def not_found(a):
    return render_template("404.html")
if __name__ == '__main__':
    app.run()
