from flask import Flask, g, make_response, request, Response # pip install flask
from flask import session, render_template, Markup
import atexit
from apscheduler.schedulers.blocking import BlockingScheduler # pip install apscheduler
import os
import subprocess

def exec_cron():
    print("=====start crwaling=====")
    os.system("python crawling.py") # 크롤링 코드 실행
    os.system("curl localhost:5000")

app = Flask(__name__)

@app.route('/')
def index():
    sched = BlockingScheduler()
    # 예약방식 interval로 설정, 59초마다 한번 실행
    sched.add_job(exec_cron, 'interval', seconds=5)
    sched.start()
    return render_template('app.html')

if __name__=="__main__":
    app.run()
