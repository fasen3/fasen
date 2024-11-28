from captcha.fields import CaptchaField
from django.db import models
from django import forms


class User(models.Model):
    """用户表"""

    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    # name必填，最长不超过128个字符，并且唯一，也就是不能有相同姓名
    name = models.CharField(max_length=128, unique=True)
    # password必填，最长不超过256个字符（实际可能不需要这么长）
    password = models.CharField(max_length=256)
    # email使用Django内置的邮箱类型，并且唯一
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    # 元数据里定义用户按创建时间的反序排列，也就是最近的最先显示
    c_time = models.DateTimeField(auto_now_add=True)

    # 使用__str__帮助人性化显示对象信息；
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField()


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # password1和password2，用于输入两遍密码，并进行比较，防止误输密码
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')

#属性名称必须是英文，否则渲染不到
class Bilibili(models.Model):
    rank_tab = models.TextField(db_column='分区名称',blank=True, null=True)
    rank_num = models.IntegerField(db_column='排名',blank=True, null=True)
    bvid = models.IntegerField(db_column='视频ID', blank=True, null=True)  # Field name made lowercase.
    title = models.TextField(db_column='视频标题',blank=True, null=True)
    author = models.TextField(db_column='作者',blank=True, null=True)
    au_href = models.CharField(max_length=255, blank=True, null=True)
    href = models.CharField(max_length=255, blank=True, null=True)
    like = models.IntegerField(db_column='点赞',blank=True, null=True)
    coin = models.IntegerField(db_column='投币',blank=True, null=True)
    reply = models.IntegerField(db_column='评论',blank=True, null=True)
    favorite = models.IntegerField(db_column='收藏',blank=True, null=True)
    danmaku = models.IntegerField(db_column='弹幕',blank=True, null=True)
    share = models.IntegerField(db_column='分享',blank=True, null=True)
    reply = models.IntegerField(db_column='播放',blank=True, null=True)
    tag_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bilibili'
