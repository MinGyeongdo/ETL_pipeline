import boto3
from pathlib import Path
import gzip    
import environ
import os

BASE_DIR=Path(__file__).resolve().parent.parent


env = environ.Env(DEBUG=(bool, True))

environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)



def compressor():
    #압축할 로그파일 경로 생성
    logfile_path = BASE_DIR/'logs'/'encrypted_log.json'
    logfile_path = logfile_path.resolve() #절대경로 반환

    compressfile_path = BASE_DIR/'logs'/'compressed_log.gz'

    with open(logfile_path,'rb') as f_in:
        with gzip.open(compressfile_path,'wb') as f_out:
            f_out.writelines(f_in)  # ./logs/compressed_log.gz 압축 파일 생성


def s3_upload():
    compressor() #encrypted_logs파일을 통해 압축된 로그 파일 생성하고 시작

    #s3 client 생성
    s3 = boto3.client('s3',
            aws_access_key_id=env('AWS_KEY_ID'),
            aws_secret_access_key=env('AWS_ACCESS_KEY'))

    currentpath = str(BASE_DIR) #/Users/gyeongdo/projects/ETL_pipeline
    bucket_name = 'logdata.min'
    file_name = 'compressed_log.gz'
    file_path = currentpath+'/logs/'+file_name
    
    #변수: 순서대로 로컬 파일명, s3의 버킷명, s3에 저장되는 파일명
    s3.upload_file(file_path, bucket_name, file_name)


if __name__ == '__main__':
   s3_upload()