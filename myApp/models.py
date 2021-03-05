from django.db import models


# Create your models here.

class BaseModel(models.Model):
    createTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True  # 不生成表


class UserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(password__isnull=False)


class User(BaseModel):
    objects = models.Manager()
    userManager = UserManager()
    # 字段名：不能是Python的关键字，不能使用连续的下划线
    # db_column: 数据表中的字段名称
    id = models.AutoField(primary_key=True, db_column='id')
    # CharField类型必须指明长度max_length
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    createTime = models.DateTimeField(auto_now_add=True)

    class Meta:  # 元数据
        db_table = 'users'
        ordering = ['username']

    # def __str__(self):
    #     return self.username

    @classmethod
    def after(cls, date):
        return cls.objects.filter(createTime__gt=date)


class Publisher(models.Model):
    pname = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'publisher'


class Book(models.Model):
    bname = models.CharField(max_length=200, blank=True, null=True)
    # ForeignKey 参数：参照的模型名
    # 多对一模型通过ForeignKey表示多对一
    # 如果Publisher定义在book之后，第一个参数应该用字符串'Publisher'
    publisher = models.ForeignKey('Publisher', on_delete=models.DO_NOTHING,
                                  db_column='pid',  # 表中字段名
                                  related_name='books'  # 通过出版社查图书时使用的关系名
                                  , null=True)

    class Meta:
        db_table = 'book'


class Buyer(models.Model):
    bname = models.CharField(max_length=30)
    level = models.IntegerField(default=1)

    class Meta:
        db_table = 'buyer'


class Goods(models.Model):
    gname = models.CharField(max_length=100)
    price = models.FloatField()
    # buyer = models.ManyToManyField(Buyer)  # 这种写法会自动生成第三张表，但我们无法直接控制
    buyer = models.ManyToManyField(Buyer, through='Orders')

    def __str__(self):
        return self.gname + "  " + str(self.price)

    class Meta:
        db_table = 'goods'
        ordering=['id']

# 手动创建中间表
class Orders(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, db_column='bid')
    # 若使用了related_name，则可以通过order.goods，若没有，可通过order.goods_set
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, db_column='gid',related_name='goods')
    num = models.IntegerField(default=1)

    class Meta:
        db_table = 'orders'