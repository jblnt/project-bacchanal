from datetime import date, datetime, timezone, timedelta

#function views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

#classviews
from django.views.generic import DetailView, ListView
from django.db.models import Q

#custom models and forms
from .models import Articles
from .forms import SearchForm, DateForm

# Helper Functions
def day():
    delta = -5
    now = datetime.now(tz=timezone(timedelta(hours=delta)))
    #return date(now.year, now.month, now.day)
    return datetime(2022, 4, 25)

# Function Based Views
# Non Premium Functions
def newsListView(request):
    article_list=Articles.objects.filter(tag__icontains = "News", date = day())
    paginator=Paginator(article_list, 8)
    pageNum = request.GET.get('page') if request.GET.get('page') else 1
    page_obj = paginator.get_page(pageNum)

    source = request.path.split('/')[1] if request.path.split('/')[1] != "" else "all"

    context={
        'articles':page_obj.object_list,
        'title':'Today\'s Stories',
        'topic':'News',
        'form':SearchForm(),
        'form_date': DateForm(),
        'page_obj':page_obj,
        'source': source
    }

    return render(request, 'webapp_main/articles_list.html', context)

def source(request, source):
    article_list = Articles.objects.filter(source__icontains=source, date=day())
    paginator = Paginator(article_list, 8)
    p_num = request.GET.get('page') if request.GET.get('page') else 1
    page_obj = paginator.get_page(p_num)

    context = {
        'articles':page_obj.object_list,
        'title':source.upper(),
        'topic':source + ' news',
        'page_obj':page_obj,
        'source': source
    }

    return render(request, 'webapp_main/articles_list.html', context)

def tagView(request):
    source = request.GET.get("source")
    tag = request.GET.get("tag")

    excludedItems = Articles.objects.exclude(Q(tag__icontains = "News")|Q(tag__icontains = "Sports")|Q(tag__icontains = "Letters"))

    if source == "all":
        article_list = Articles.objects.filter(tag__icontains = tag, date = day()) if tag != "others" else excludedItems.filter(date = day()).order_by('tag')
    else:
        article_list = Articles.objects.filter(source__icontains = source, tag__icontains = tag, date = day()) if tag != "others" else excludedItems.filter(source__icontains = source, date = day()).order_by('tag')

    paginator = Paginator(article_list, 8)
    p_num = request.GET.get('page') if request.GET.get('page') else 1
    page_obj = paginator.get_page(p_num)

    #eg txt3 = "My name is {}, I'm {}".format("John",36) 
    context={
        "articles" : page_obj.object_list,
        "title" : source.upper(),
        "topic" : source + ' - ' + tag,
        "page_obj" : page_obj,
        "source" : source,
        "query": "source={}&tag={}".format(source, tag)
    }

    return render(request, 'webapp_main/articles_list.html', context)

@login_required
def SearchView(request):
    requestedQuery = request.GET.get("q")
    requestedTag = request.GET.get("tag")

    excludedItems = Articles.objects.exclude(Q(tag__icontains = "News")|Q(tag__icontains = "Sports")|Q(tag__icontains = "Letters"))

    if requestedTag:
        article_list =  Articles.objects.filter(title__icontains = requestedQuery, tag__icontains = requestedTag) if requestedTag != "others" else excludedItems.filter(title__icontains = requestedQuery).order_by('tag')
        queryString = "q={}&tag={}".format(requestedQuery, requestedTag)
    else:
        article_list=Articles.objects.filter(title__icontains = requestedQuery).order_by('source')
        queryString = "q={}".format(requestedQuery)

    paginator=Paginator(article_list, 8)
    p_num = request.GET.get('page') if request.GET.get('page') else 1
    page_obj=paginator.get_page(p_num)

    context={
        'articles':page_obj.object_list,
        'title': request.GET["q"]+' Results',
        'topic':'Results For "'+request.GET["q"]+'"',
        'page_obj': page_obj,
        'source': 'query',
        'q': requestedQuery,
        'query' : queryString
    }

    return render(request, 'webapp_main/articles_list.html', context)

@login_required
def archiveListView(request):
    requestedDate = request.GET.get("q")
    requestedTag = request.GET.get("tag")

    excludedItems = Articles.objects.exclude(Q(tag__icontains = "News")|Q(tag__icontains = "Sports")|Q(tag__icontains = "Letters"))

    if requestedTag:
        article_list =  Articles.objects.filter(date = requestedDate, tag__icontains = requestedTag).order_by('source') if requestedTag != "others" else excludedItems.filter(date = requestedDate).order_by('tag')
        queryString = "q={}&tag={}".format(requestedDate, requestedTag)
    else:
        article_list=Articles.objects.filter(date = requestedDate).order_by('source')
        queryString = "q={}".format(requestedDate)

    paginator = Paginator(article_list, 8)
    p_num = request.GET.get('page') if request.GET.get('page') else 1
    page_obj = paginator.get_page(p_num)

    context = {
        'articles':page_obj.object_list,
        'title': requestedDate +' Stories',
        'topic':'News From ' + requestedDate,
        'page_obj':page_obj,
        'source': 'archive',
        'q' : requestedDate,
        'query': queryString
    }

    return render(request, 'webapp_main/articles_list.html', context)

## Class Based Views
class ArticleDetailView(LoginRequiredMixin, DetailView):
    model=Articles
    context_object_name='article'

    query_pk_and_slug = True