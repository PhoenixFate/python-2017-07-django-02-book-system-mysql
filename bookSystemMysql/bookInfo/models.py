from django.db import models


# Create your models here.
class BookManager(models.Manager):
    """图书管理类"""

    # 1.改变查询的结果集
    # 重写父类的方法
    def all(self):
        # 调用父类的all方法
        book_list = super().all()  # QuerySet
        book_list = book_list.filter(is_delete=False)
        return book_list

    # 2.封装其他函数
    def create_book(self, title, publish_date):
        # 这样写的好处是在Book类名发生变化的时候，不需要改变代码
        model_class = self.model  # self.model 就是Book
        book = model_class()
        book.title = title
        book.publish_date = publish_date
        book.save()
        return book


class Book(models.Model):
    """图书模型"""
    # 常用属性：
    # default
    # primary_key
    # unique
    # db_index, 若为True，则在表中会为该字段创建索引
    # db_column 如果未指定，则默认使用属性名称
    # null 是否允许为空

    # 图书名
    title = models.CharField(max_length=100)
    # 价格,max_digits: 最大位数量； decimal_places：小数点位数
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # 出版日期
    # auto_now: 表示每次保存时，自动设置该值为当前时间
    # auto_now_add: 第一次被创建的时候，设置当前时间
    # auto_now, auto_now_add 同时只能用一个
    # DateField：年月日
    # TimeField：时分秒
    # DateTimeField：年月日时分秒
    publish_date = models.DateField(auto_now=False)
    # 阅读量
    read_count = models.IntegerField(default=0)
    # 评论量
    comment_count = models.IntegerField(default=0)
    # 是否删除
    is_delete = models.BooleanField(default=False)

    # 如果定义了Manager对象，则Book.objects不再默认提供
    # object_book = models.Manager()  # 自定义一个Manager类对象
    objects = BookManager()

    # 指定表名！！！！！！！！
    # class Meta:
    #     db_table = 'book'  # 指定模型类对应的表名


class Hero(models.Model):
    """英雄"""
    # 姓名
    name = models.CharField(max_length=100)
    # 性别
    gender = models.BooleanField(default=False)
    # 备注
    # blank=True 表示admin可以不输入
    comment = models.CharField(max_length=1024, null=True, blank=True)
    # 关联属性
    book = models.ForeignKey('Book', on_delete=models.CASCADE, )


# 两个类之间是多对多的关系
class NewsType(models.Model):
    """新闻类型类"""
    # 类型名
    type_name = models.CharField(max_length=20)


class News(models.Model):
    """新闻类"""
    # 标题
    title = models.CharField(max_length=128)
    # 发布时间
    publish_date = models.DateTimeField(auto_now_add=True)
    # 新闻内容
    content = models.TextField()
    # 关联属性
    news_type = models.ManyToManyField("NewsType")


# 1对1 关系
class EmployeeBasicInfo(models.Model):
    """员工基本属性"""
    # 姓名
    name = models.CharField(max_length=64)
    # 性别
    gender = models.BooleanField(default=False)
    # 年龄
    age = models.IntegerField()


class EmployeeDetailInfo(models.Model):
    """员工详细信息"""
    phone = models.CharField(max_length=20)
    # 联系地址
    address = models.CharField(max_length=1024)
    # 关联属性
    employee_basic = models.OneToOneField('EmployeeBasicInfo', on_delete=models.CASCADE, )


# 自关联
# 地区模型类
# 省 1:n  市 1: n 区/县
class Area(models.Model):
    """地区模型类"""
    title = models.CharField(max_length=100)
    # 关系属性，代表当前地区的父级属性
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, )



