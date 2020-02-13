from django.core import serializers
from django.shortcuts import render, redirect
from bookInfo.models import Book, Hero, Area
from datetime import date
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q, F, Count, Sum, Avg, Max, Min
import json


# Create your views here.

# 显示图书信息
def index(request):
    print("bookSystemMysql")
    """显示图书信息"""
    # 1.所有图书
    book_list = Book.objects.all()
    # 2.使用模板
    return render(request, "bookInfo/index.html", {"book_list": book_list})


def create(request):
    # 1.创建book对象
    b = Book()
    b.title = "流星蝴蝶剑"
    b.publish_date = date(1990, 1, 1)
    # 2.保存进数据库
    b.save()
    # 3.重定向到index
    # return HttpResponseRedirect("/index")
    return redirect("/index")


def delete(request, book_id):
    # 1.通过book_id获取对象
    book = Book.objects.get(id=book_id)
    # 2.删除
    book.delete()
    # 3.重定向/index
    # return HttpResponseRedirect("/index")
    return redirect("/index")  # 等价于上面这句话，但更简单


def select_get(request):
    # get:
    # 返回满足条件的一条且只能有一条数据
    # 返回一个模型对象
    # 如果查到多条记录，抛MultipleObjectsReturned
    # 如果没有查到数据，抛DoesNotExist

    # 精确查询
    # id=1 是id__exact=1的简写
    book = Book.objects.get(id=1)
    book = Book.objects.get(id__exact=1)

    return redirect("index")


def select_all(request):
    # all:
    # 返回查询到的所有对象
    # 返回值是QuerySet类型，可遍历
    book_list = Book.objects.all()
    # 模糊查询
    return redirect("index")


def select_filter(request):
    # filter:
    # get只能有一条，filter可以有多条
    book_list = Book.objects.filter(title__contains="射")
    book_list = Book.objects.filter(titile__endswith="部")
    book_list = Book.objects.filter(titile__startswith="天")
    bool_list = Book.objects.filter(title__isnull=False)  # False: is not null
    bool_list = Book.objects.filter(id__in=[1, 3])
    # gt: great than
    # lt: less than
    # gte: great than equal
    # lte: less than equal
    book_list = Book.objects.filter(id__gt=1)
    book_list = Book.objects.filter(id__gte=1)
    book_list = Book.objects.filter(id__lt=3)
    book_list = Book.objects.filter(id__lte=3)

    # 日期查询
    book_list = Book.objects.filter(publish_date__year=1980)  # 日期年份等于1980
    book_list = Book.objects.filter(publish_date__gt=date(1980, 1, 1))  # 1980.1.1 之后的

    # exclude 返回不满足条件的
    book_list = Book.objects.exclude(id=3)  # id不等于3

    # order_by
    book_list = Book.objects.order_by('id')  # 默认升序
    book_list = Book.objects.order_by('-id')  # 降序

    # 组合
    book_list = Book.objects.filter(id__gt=3).order_by("-read_count")
    book_list = Book.objects.filter(id__gt=3, read_count__gt=30)  # 默认多个条件之间是且的关系
    return redirect("index")


def select_q(request):
    # 使用Q对象, 进行条件查询之间的  与、或、非
    # or :  id>3 or read_count>30
    book_list = Book.objects.filter(Q(id__gt=3) | Q(read_count__gt=30))
    # and :  id>3 and read_count>30
    book_list = Book.objects.filter(Q(id__gt=3) & Q(read_count__gt=30))
    # not(非): id!=3
    book_list = Book.objects.filter(~Q(id == 3))
    return redirect("index")


def select_f(request):
    # 使用F对象，进行不同属性之间的比较
    # 阅读量 > 评论量
    book_list = Book.objects.filter(read_count__gt=F("comment_count"))
    # 阅读量 > 2倍数评论量
    book_list = Book.objects.filter(read_count_gt=F("comment_count") * 2)
    print(book_list.exists())
    return redirect("index")


def select_juhe(request):
    # count 总条数
    key_count = Book.objects.all().aggregate(Count("id"))  # 返回字典{"id_count":20}
    key_count = Book.objects.all().count()  # 返回数字 5
    key_count = Book.objects.filter(id__gt=3).count()
    # sum
    key_sum = Book.objects.all().aggregate(Sum("id"))
    # avg
    key_avg = Book.objects.all().aggregate(Avg("id"))
    # max
    key_max = Book.objects.all().aggregate(Max("id"))
    # min
    key_min = Book.objects.all().aggregate(Min("id"))
    return redirect("index")


def select_linked(request):
    # 图书关联的英雄的描述包含'六'
    book_list = Book.objects.filter(hero__comment__contains='六')
    book_list = Book.objects.filter(hero__id__gt=3)
    # 查询书名为'天龙八部' 的所有英雄
    hero_list = Hero.objects.filter(book__title='天龙八部')
    return redirect("index")


def get_areas(request):
    """获取广州市的上级地区和下级地区"""
    # 1.获取广州市的信息
    guang_zhou_shi = Area.objects.get(title="广州市")
    # 2.查询广州市的上级地区
    parent = guang_zhou_shi.parent
    # 3.查询广州市的下级地区
    children_area = guang_zhou_shi.area_set.all()
    return render(request, "bookInfo/area.html",
                  {"area": guang_zhou_shi, "parent": parent, "children_area": children_area})


def book_json(request):
    book_list = Book.objects.all()
    temp = serializers.serialize('json', book_list, ensure_ascii=False)
    print(type(temp))
    print(serializers.serialize('json', book_list, ensure_ascii=False))
    temp2 = json.loads(serializers.serialize('json', book_list, ensure_ascii=False))
    print(type(temp2))
    print(json.loads(serializers.serialize('json', book_list, ensure_ascii=False)))
    return JsonResponse({
        'code': '200',
        'data': json.loads(serializers.serialize('json', book_list, ensure_ascii=False)),
        'msg': '获取book列表成功'
    })


def login(request):
    """显示登录页面"""
    return render(request, "bookInfo/login.html")


def login_check(request):
    """校验登录"""
    # request.POST 保存的是post提交的参数
    # request.GET 保存的是get提交的参数
    request_path = request.path
    print(request_path)
    method_type = request.method
    print(method_type)

    # 1.获取用户名和密码
    username = request.GET.get("username")
    password = request.GET.get("password")
    print("username: %s " % username)
    print("password: %s " % password)
    username = request.POST.get("username")
    password = request.POST.get("password")
    gender = request.POST.get('gender')
    is_tuanyuan = request.POST.get('is_tuanyuan')
    joy = request.POST.getlist('joy')
    city = request.POST.get('city')
    more_text = request.POST.get('more_text')
    print("username: %s " % username)
    print("password: %s " % password)
    print(gender)
    print(is_tuanyuan)
    print(joy)
    print(city)
    print(more_text)
    # 2.进行登录的校验

    # 3.返回应答
    return render(request, "bookInfo/success.html", {"username": username, "password": password})


def test_ajax(request):
    """返回test_ajax页面"""
    return render(request, "bookInfo/test_ajax.html")


def ajax_handler(request):
    """处理ajax请求"""
    book_list = Book.objects.all()
    return JsonResponse({
        'code': '200',
        'data': json.loads(serializers.serialize('json', book_list, ensure_ascii=False)),
        'msg': '获取book列表成功'
    })
