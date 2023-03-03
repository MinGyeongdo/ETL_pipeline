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


def bot_choice(num):
    """
    봇계정 중 랜덤하게 선택해서 정보를 저장
    """
    bot_list = []
    for i in range(num):
        bot_info = {
                "email": f"bot{random.randrange(4,21)}@bot.com",
                "password" : "iambot4084",            
                }
        bot_list.append(bot_info)
    
    return bot_list
        
def get_access(bot_list):
    """
    bot_choice 에서 얻은 bot의 리스트를 가지고 로그인하여 Access key를 얻습니다.
    """
    access_list = []

    for bot in bot_list:
        response = requests.post(f"https://{env('HOST')}/user/login/", json=bot)
        access_key = json.loads(response.text)['token']['access']
        access_list.append(access_key)
    return access_list

def create_content(access_list):
    """
    access key를 헤더에 넣어주어서 인증된 페이지에 접근하여 글을 생성합니다.
    """
    content_id_list = []
    for access_key in access_list:
        rand_num = random.randrange(1,1000)
        headers = {"Authorization": f"Bearer {access_key}"}
        data = {"title": f"글 작성 bot {rand_num}", "body": f"글 내용 생성 bot {rand_num}"}
        response = requests.post(f"{env('HOST')}/blog/create/",json=data, headers=headers)
        content_info = json.loads(response.text)
        
        content_id_list.append(content_info['id'])
        time.sleep(1)
    

    return content_id_list

def revise_content(access_list, content_id_list):
    """
    access key를 헤더에 넣어주어서 인증된 페이지에 접근하여 글을 수정합니다.
    """
    for access_key, content_id in zip(access_list, content_id_list):
        rand_num = random.randrange(1,1000)
        headers = {"Authorization": f"Bearer {access_key}"}
        data = {"title": f"글 제목 수정 bot {rand_num}", "body": f"글 내용 수정 bot {rand_num}"}
        response = requests.put(f"{env('HOST')}/blog/{content_id}/",json=data, headers=headers)
        time.sleep(1)
    return f"{len(access_list)}개 봇 글 수정 완료!"

def delete_content(access_list, content_id_list):
    """
    access key를 헤더에 넣어주어서 인증된 페이지에 접근하여 글을 삭제합니다.
    """
    for access_key, content_id in zip(access_list, content_id_list):
        
        headers = {"Authorization": f"Bearer {access_key}"}
        response = requests.delete(f"{env('HOST')}/blog/{content_id}/", headers=headers)
        time.sleep(1)
    
    return f"{len(access_list)}개 봇 생성한 글 삭제 완료!"


def bot_activate(num):
    """
    1. 입력한 num 수만큼 bot 계정을 랜덤으로 선정한다.
    2. 선택한 bot 계정들을 로그인하여, access key list를 만든다.
    3. access key 를 활용하여, 글 생성 페이지에 접근하여 글을 랜덤으로 생성한다.
    4. 여기서 생성한 content의 id를 list로 저장한다.
    5. content id list를 활용하여 글을 수정하고 마지막으로 삭제한다.
    """
    bots = bot_choice(num)
    access_key_list = get_access(bots)
    content_id_list = create_content(access_key_list)
    revise_content(access_key_list, content_id_list)
    delete_content(access_key_list, content_id_list)

if __name__ == '__main__':
    # 원하는 bot 개수 입력
    bot_activate(30)