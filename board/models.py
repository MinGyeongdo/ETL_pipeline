from django.db import models
from django.conf import settings
from accounts.models import User
from django.utils import timezone

class Blog(models.Model):

    # 1. 게시글의 id 값
    id = models.AutoField(primary_key=True, null=False, blank=False) 

    # 2. 제목
    title = models.CharField(max_length=100)

    # 3. 작성일
    created_at = models.DateTimeField(auto_now_add=True)

    # 4. 작성자 CASCADE( 사용자 정보삭제 시 게시글도 같이 삭제하는 Option )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    # 5. 본문
    body = models.TextField()


    class Meta:
        db_table = 'text' # 테이블명을 text 로 설정