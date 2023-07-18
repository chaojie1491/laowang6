from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import get_user_model as user_model

# Create your models here.
User = user_model()


# Create your models here.
class Category(models.Model):
    """
    Django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    然后给name设置了一个'分类'的名称
    """
    name = models.CharField('分类', max_length=100, unique=True)
    seq = models.IntegerField('排序', default=1)


class Tags(models.Model):
    """
    标签 Tag 也比较简单，和 Category 一样。
    再次强调一定要继承 models.Model 类！
    """
    name = models.CharField('标签', max_length=100, unique=True)


class FileRecord(models.Model):
    origin_name = models.CharField('源文件名称', max_length=200)
    file_name = models.CharField('文件名称', max_length=200)
    file_path = models.FilePathField('文件路径', max_length=255)
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    suffix = models.CharField('文件类型', max_length=10)
    file_net_path = models.CharField('文件网络路径', max_length=200)


class NUser(models.Model):
    phone_number = models.CharField('手机号', max_length=20)
    identity_number = models.CharField('身份证号', max_length=50, blank=True)
    identity_photo = models.ForeignKey(FileRecord, related_name="identity_photo", on_delete=models.CASCADE,
                                       verbose_name='身份证照片',
                                       default='',
                                       blank=True, null=True)
    password = models.CharField('密码', max_length=20)
    invitation_code = models.CharField('邀请码', max_length=20, blank=True)
    real_name = models.CharField('手机号', max_length=10, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    status_choices = (
        (1, "PASS"),
        (0, "NO_APPROVAL"),
        (3, "WAIT"),
        (2, "REJECT"))
    approval_status = models.SmallIntegerField(verbose_name="审核状态", choices=status_choices, default=0)
    status_ = (
        (1, "正常"),
        (-1, "拉黑"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_, default=0)

    approval_time = models.DateTimeField('审核时间', auto_now_add=True, blank=True)
    reject_reason = models.TextField('拒绝原因', blank=True)
    max_invitation_number = models.IntegerField('最大邀请', default=10)


class NUserRelation(models.Model):
    invitation_user = models.ForeignKey(NUser, related_name='invitation_user', on_delete=models.CASCADE,
                                        verbose_name='用户', default='1')
    invited_user = models.ForeignKey(NUser, related_name='invited_user', on_delete=models.CASCADE, verbose_name='用户',
                                     default='1')


class Article(models.Model):
    # 文章正文，我们使用了 TextField，并且指定了标题的长度
    title = models.CharField('标题', max_length=70)
    # 使用 TextField 来存储大段文本，文章摘要，我们指定了最大长度和允许可以为空。
    intro = models.TextField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类', default='1')
    tags = models.ManyToManyField(Tags, blank=True)
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    html_text = models.TextField(blank=True)
    markdown_text = models.TextField(blank=True)
    net_cover = models.CharField('文件网络路径', max_length=200,blank=True,null=True)
    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    # created_time，我们使用了DateTimeField字段，添加了一个auto_now_add参数，自动获取添加时间！
    created_time = models.DateTimeField('发布时间', auto_now_add=True)
    type_choices = (
        (1, "ARTICLE"),
        (2, "NEWS"),
        (3, "MEDIA"))
    type = models.SmallIntegerField(verbose_name="类型", choices=type_choices, default=1)
    cover = models.ForeignKey(FileRecord, related_name="cover", on_delete=models.CASCADE, verbose_name='封面',
                              default='',
                              blank=True, null=True)
    music = models.ForeignKey(FileRecord, related_name="music", on_delete=models.CASCADE, verbose_name='音乐路径',
                              default='', blank=True, null=True)
    status_choices = (
        (1, "RELEASE"),
        (0, "PADDING"),
        (-1, "DELETE"))
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    is_top = models.BooleanField(verbose_name="是否在首页显示", default=True)
