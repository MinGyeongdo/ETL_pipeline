import requests
from datetime import datetime
import random
from pathlib  import Path
import environ
import os
# 원하는 만큼의 봇계정 생성

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, True))

environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

def create_bot(num):

    # 봇 생성 숫자 조절

    for i in range(1,num+1):
        bot_form = {
            "email": f"bot{i}@bot.com",
            "nickname" : f"bot{i}",
            "gender" : random.choice(['M','F']),
            "password" : "iambot4084",
            "password2" : "iambot4084",
            "name" : f"bot{i}",
            "birth_date" : datetime.today().strftime("%Y-%m-%d"),
        }
        try:
            response = requests.post(f"http://{env('HOST')}/user/signup/", json=bot_form)
        except Exception as e:
            print("bot 생성에 오류가 발생했습니다. ", e)


    return  f"{num}개의 bot accounts 생성 complete"









if __name__ == '__main__':
    # 원하는 bot 개수 입력
    create_bot(30)
