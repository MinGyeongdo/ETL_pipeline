import requests
import time
import random
import json
from pathlib import Path
import environ
import os

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, True))

environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)


class bot:

    def __init__(self,num):
        self.num = num
        self.bot_list = [{"email": f"bot{random.randrange(1,41)}@bot.com", 
                          "password" : "iambot4084" } for _ in range(num)]
        print(f"{self.num}개 봇 랜덤 생성 완료!")
        #print(self.bot_list)
    
    def login(self):
        self.key_list = []
        cnt = 0
        for bot in self.bot_list:
            try:
                response = requests.post(f"http://{env('HOST')}/user/login/", json=bot)
                key = json.loads(response.text)['token']['access']
                self.key_list.append(key)
                cnt += 1
            except Exception as e:
                print(f"{bot}의 로그인이 실패하였습니다. 연결을 확인하세요 계정이 존재하지 않을 수도 있습니다.", e)
        #print(self.key_list)
        print(f"{cnt}개 봇 로그인 완료!")
    
    def post(self):
        
        self.post_ids = []
        cnt = 0
        for key in self.key_list:
            rand_num = random.randrange(1,1000)
            headers = {"Authorization": f"Bearer {key}"}
            data = {"title": f"글 작성 bot {rand_num}", "body": f"글 내용 생성 bot {rand_num}"}
            try:
                response = requests.post(f"http://{env('HOST')}/blog/create/",json=data, headers=headers)
                content_info = json.loads(response.text)
                self.post_ids.append(content_info['id'])
                cnt += 1
            except Exception as e:
                print("글생성에 실패했습니다.", e)
            
            time.sleep(1)
        print(f"{cnt}개 글 생성 완료!")
        #print(self.post_ids)
    
    def update(self):
        cnt = 0
        for key, post_id in zip(self.key_list, self.post_ids):
            rand_num = random.randrange(1,1000)
            headers = {"Authorization": f"Bearer {key}"}
            data = {"title": f"글 제목 수정 bot {rand_num}", "body": f"글 내용 수정 bot {rand_num}"}
            try :
                response = requests.put(f"http://{env('HOST')}/blog/{post_id}/",json=data, headers=headers)
                cnt += 1
            except Exception as e:
                print(f"post_id = {post_id} 번글 수정에 실패했습니다.")
            time.sleep(1)
        print(f"{cnt}개 글 업데이트 완료!")

    def delete(self):
        cnt = 0

        for key, post_id in zip(self.key_list, self.post_ids):
            headers = {"Authorization": f"Bearer {key}"}
            try :
                response = requests.delete(f"http://{env('HOST')}/blog/{post_id}/", headers=headers)
                cnt += 1
            except Exception as e:
                print(f"post_id = {post_id}글 삭제에 실패했습니다. 없는 게시글이나, 연결에 실패했을 수 있습니다.", e)
        
            time.sleep(1)
        print(f"{cnt}개 글 삭제 완료!")

if __name__ == '__main__':
    # 원하는 bot 개수 입력
    #bot_activate(30)
    bots = bot(5)
    bots.login()
    bots.post()
    bots.update()
    bots.delete()