import hashlib
import os
from cryptography.fernet import Fernet
from pathlib import Path
from dateutil import parser #epoch time 생성
import json
from uuid import uuid4 #recordId 생성

def get_hash(integer):
    """
    입력한 정수값을 binary 문자열로 인코딩 후, salt값을 append하여 SHA256 알고리즘을 이용하여 해시값을 생성하는 함수
    """

    salt = os.urandom(32) #binary 값 생성
    #ex)\xa9\x84\x01\x96\xa4\t\xadP\x1e\xf3:\x94[\xb7\x9c=\xfebI\x03\xa2\x05\xd5\x9a\x19\x9b\xabhO\x13\xb8\x83
    # 

    plainstring = str(integer)
    plaintext = plainstring.encode() #encode하고 싶은 문자열을 binary 문자열로 인코딩
    digest = hashlib.pbkdf2_hmac('sha256', plaintext, salt, 10000) #digest 객체는 생성된 해시값을 가짐
    hex_hash = digest.hex()
    return hex_hash #바이트 문자열을 16진수로 변환한 문자열(hex)을 반환

def decrypt(plaintext):
    """
    양방향 암호화를 사용하여 key를 생성 및 별도 파일에 저장하며, 복호화된 데이터를 반환하는 함수
    plaintext: 복호화하려는 데이터(json 형태)
    """
    #logkey.key 파일에서 key값 불러오기
    mod_path = Path(__file__).parent
    #print(mod_path)
    absolute_keyfile_path = (mod_path/"./logkey.key").resolve()#resolve: 절대 경로 반환
    
    #print(absolute_keyfile_path)
    my_file = Path(absolute_keyfile_path)
    if my_file.is_file():
        # 'logkey.key' 파일이 존재
        with open(absolute_keyfile_path,'rb') as file:
            key = file.read()    
    
    fernet = Fernet(key)
    json_log = plaintext
    decrypt_str = fernet.decrypt(f"{json_log}".encode('ascii'))
    return decrypt_str.decode('utf-8')

def encrypt(plaintext):
    """
    양방향 암호화를 사용하여 key를 생성 및 별도 파일에 저장하며, 암호화된 데이터를 반환하는 함수
    plaintext: 암호화하려는 데이터(json 형태)
    """
    #logkey.key 파일에서 key값 불러오기
    mod_path = Path(__file__).parent
    absolute_keyfile_path = (mod_path /"./logkey.key").resolve() #resolve: 절대 경로 반환
    print(absolute_keyfile_path)
    my_file = Path(absolute_keyfile_path)
    if my_file.is_file():
        # 'logkey.key' 파일이 존재
        with open(absolute_keyfile_path,'rb') as file:
            key = file.read()
    else:
        #키 생성, 'logkey.key' 파일 생성 및 키값 저장
        key = Fernet.generate_key()
        with open('logkey.key','wb') as file:
            file.write(key)
    
    fernet = Fernet(key)
    json_log = plaintext
    encrypt_str = fernet.encrypt(f"{json_log}".encode('ascii'))
    # decrypt_str = fernet.decrypt(encrypt_str)
    return encrypt_str
def executedata_from_encrypted_log():
    """
    암호화된 로그로부터 복호화 하여 메타데이터 추출
    """
    mod_path = Path(__file__).parent
    decrypt_log_path = (mod_path/"../logs/decrypt_log.json").resolve()
    absolute_logfile_path = (mod_path /"../logs/encrypted_log.json").resolve()
    print(absolute_logfile_path)
    
    with open(absolute_logfile_path,'r') as file:
            meta =  [json.loads(decrypt(line["data"])) for line in json.loads(file.read())]
                  
            #print(type(file_data))
            # Join encrypted with file_data inside encrypted_logs
            
            # Sets file's current position at offset.
            #file.seek(0)
            # convert back to json.
    with open(decrypt_log_path, 'w') as file:
          file.write(json.dumps(meta, indent=2))            

    

def update_file():
    """
    로그 파일에 로그가 추가될 때마다 해당 내용을 가져와서 암호화된 내용을 별도 JSON 파일에 저장하는 함수
    recordId, ArrivalTimestamp 생성 후 암호화된 데이터 (data)와 함께 저장
    """
    #로그 파일 읽어오기
    mod_path = Path(__file__).parent
    
    absolute_logfile_path = (mod_path /"../logs/board_logging.log").resolve()

    #로그 파일의 마지막 줄 읽어오기
    with open(absolute_logfile_path, 'rb') as f:
        try:  # catch OSError in case of a one line file 
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()

    #데이터 생성하기
    data = encrypt(last_line).decode('utf8')
    data_dict = json.loads(last_line) #json 형태의 log를 dictionary 형태로 변환
    strtime = data_dict["time"]
    epoch_time = parser.parse(strtime).timestamp() #string 형태의 로그 생성 시간을 timestamp 형태로 변환

    encrypted = {}
    encrypted["recordId"] = uuid4().int  #랜덤한 고유값
    encrypted["ArrivalTimestamp"] = epoch_time  #로그 생성 시간 (epoch time으로 표시)
    encrypted["data"] = data  #암호화된 개별 로그 데이터값

    newLogfile_path = Path(absolute_logfile_path).parent
    newLogfile_path = (newLogfile_path /"encrypted_log.json").resolve() #logs 폴더에 저장

    # json_root = {"encrypted_logs": []} #json 파일 생성 시 필요한 root 추가
    # json_root = json.dumps(json_root, indent=4)

    
    my_file = Path(newLogfile_path)
    if not my_file.is_file():
        with open(newLogfile_path,'w') as file:
                file.write('[')
                file.write(json.dumps(encrypted, indent=2))                             
                file.write(']')
    else:
        with open(newLogfile_path,'r+') as file:
            file_data = json.loads(file.read())
            #print(type(file_data))
            # Join encrypted with file_data inside encrypted_logs
            file_data.append(encrypted)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            file.write(json.dumps(file_data, indent=2))
