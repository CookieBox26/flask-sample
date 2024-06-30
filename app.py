from urllib.parse import quote
from flask import Flask, render_template, request
import os


class Variables:
    def __init__(self, host):
        self.host = host
        self.todofuken = '愛知県'
        self.shichoson = '名古屋市'
        self.message = ''

    def update(self, d):
        self.__dict__.update(d)

    def set_sharing_url(self):
        self.sharing_url = self.host \
            + '/?todofuken=' + quote(self.todofuken) \
            + '&shichoson=' + quote(self.shichoson)

    def exec(self):
        self.message = f'{self.todofuken}の{self.shichoson}に住みたいです。'
        self.set_sharing_url()

    sample_params = [
        {
            'label': 'あいちけんとうかいし',
            'values': {'todofuken': '愛知県', 'shichoson': '東海市'},
        },
        {
            'label': 'あいちけんちたし',
            'values': {'todofuken': '愛知県', 'shichoson': '知多市'},
        },
    ]
    def preset_sample_param(self):
        index_ = int(self.sample_index)
        if index_ > -1:
            self.__dict__.update(self.sample_params[index_]['values'])


app = Flask(__name__, template_folder=os.path.dirname(__file__))


@app.route(f'/', methods=['GET'])
@app.route(f'/post', methods=['POST'])
def index():
    vars = Variables('http://' + request.host)

    # GET ならパスパラメータからパラメータを取得するだけ
    if request.method == 'GET':
        vars.update(request.args)
        return render_template('index.html', vars=vars)

    # POST ならフォームからパラメータを取得する
    vars.update(request.form)

    # btn_exec がない場合はサンプルパラメータをプリセットするだけ
    if 'btn_exec' not in request.form:
        vars.preset_sample_param()
        return render_template('index.html', vars=vars)

    # 処理を実行する
    vars.exec()
    return render_template('index.html', vars=vars)
