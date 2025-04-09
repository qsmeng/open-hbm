import os
import flask 
import server

app = flask.Flask(
    __name__, 
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/'))
)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

def handle_error(e, msg, status=500):
    print(f"Error occurred: {e} - {type(e).__name__}")  # 输出错误的类型和信息
    return flask.Response(msg, status=status)

@app.route('/index')
def index():
    try:
        return flask.render_template('index.html')  # 
    except Exception as e:
        return handle_error(e, "出现错误，请稍后再试。")
@app.route('/login')
def login():
    try:
        return flask.render_template('login.html')  # 
    except Exception as e:
        return handle_error(e, "出现错误，请稍后再试。")

@app.route('/')
def root():
    return flask.redirect(flask.url_for('index'))

@app.route('/static/<path:filename>')
def static_file(filename):
    static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/static/'))
    file_path = os.path.join(static_folder, filename)

    if not os.path.exists(file_path):
        return flask.Response("文件未找到", status=404)

    try:
        return flask.send_file(file_path)
    except Exception as e:
        return handle_error(e, "出现错误，请稍后再试。")



@app.route('/get_character_templates', methods=['GET'])
def get_character_templates():
    # 准备实现的逻辑
    pass

@app.route('/get_story_templates', methods=['GET'])
def get_story_templates():
    # 准备实现的逻辑
    pass

if __name__ == '__main__':
    app.run(debug=True)

server.main()
