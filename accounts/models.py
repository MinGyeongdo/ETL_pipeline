from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, email, gender, name, password=None):
        if not email:
            raise ValueError('must have user email')
        if not gender:
            raise ValueError('must have user nickname')
        if not name:
            raise ValueError('must have user name')
        user = self.model(
            email = self.normalize_email(email),
            gender = gender,
            name = name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            password = password,
            name = name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    
    # ( db에저장될이름, 선택사항 )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    id = models.AutoField(primary_key=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    gender = models.CharField(default='', max_length=6, choices=GENDER_CHOICES, null=False, blank=False, unique=True)
    name = models.CharField(default='', max_length=100, null=False, blank=False)
    
    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    
    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 email 으로 설정
    USERNAME_FIELD = 'email'

    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ['name','gender']

    
    def has_perm(self, perm, obj=None): # True를 반환하여 권한이 있음을 알림
        return True

    def has_module_perms(self, app_label): # True를 반환하여 주어진 APP의 모델에 접근 가능하도록 함
        return True

    @property
    def is_staff(self): # True를 받아오면 장고의 관리자 화면에 로그인이 가능해짐.
        return self.is_admin
    
    class Meta:
        db_table = 'userinfo' # 테이블명을 user로 설정