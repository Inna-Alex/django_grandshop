from collections import namedtuple
import logging
import sqlite3

from django.db import connection
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CategoryRawModelForm
from .models import Category
from catalog.loggers.query_logger import QueryLogger
from catalog.loggers.query_logger_config import init_log
from catalog.utils import consts

active_tab = '\'categories\''
log_name = consts.logs['category']
init_log(log_name)
logger = logging.getLogger(log_name)


class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 10

    def get_context_data(self, **kwargs):
        ql = QueryLogger()
        with connection.execute_wrapper(ql):
            context = super(CategoryListView, self).get_context_data(**kwargs)
            context['active_tab'] = active_tab
        logger.info(str(ql))

        return context


# CRUD
class CategoryDetailView(generic.DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def get_object(self, queryset=None):
        ql = QueryLogger()
        with connection.execute_wrapper(ql):
            obj = super(CategoryDetailView, self).get_object()
        logger.info(str(ql))

        return obj


class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def form_valid(self, form):
        ql = QueryLogger()
        with connection.execute_wrapper(ql):
            response = super(CategoryCreateView, self).form_valid(form)
        logger.info(str(ql))

        return response


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'summary', 'availability']

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def form_valid(self, form):
        ql = QueryLogger()
        with connection.execute_wrapper(ql):
            response = super(CategoryUpdateView, self).form_valid(form)
        logger.info(str(ql))

        return response


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('categories')

    def get_context_data(self, **kwargs):
        context = super(CategoryDeleteView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def delete(self, request, *args, **kwargs):
        ql = QueryLogger()
        with connection.execute_wrapper(ql):
            response = super(CategoryDeleteView, self).delete(request, *args, **kwargs)
        logger.info(str(ql))

        return response


def category_raw_sql_get_one(category_id):
    ql = QueryLogger()
    with connection.execute_wrapper(ql):
        with connection.cursor() as cursor:
            sql_select = '''select category_id, name, summary,
                            availability, created_date
                            from catalog_category
                            where category_id = %s'''
            cursor.execute(sql_select, [category_id])
            result = namedtuple_fetch_one(cursor)
    logger.info(str(ql))

    return result


def category_raw_sql_get_all():
    sql_select = '''select category_id, name, summary,
                    availability, created_date
                    from catalog_category'''
    ql = QueryLogger()
    with connection.execute_wrapper(ql):
        with connection.cursor() as cursor:
            cursor.execute(sql_select)
            result = namedtuple_fetch_all(cursor)
    logger.info(str(ql))

    return result


def namedtuple_fetch_one(cursor):
    nt_result = []
    category_fields = ['category_id', 'name',
                       'summary', 'availability',
                       'created_date']
    category = namedtuple('category', category_fields)
    row = cursor.fetchone()
    nt_result.append(category._make(row))
    return nt_result


def namedtuple_fetch_all(cursor):
    desc = cursor.description
    nt_result = namedtuple('category', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def category_raw(request):
    name = 'Дирижабли%'
    sql_select = '''select category_id, name, summary, availability, created_date
                    from catalog_category
                    where name like %s'''
    category_objs_raw = Category.objects.raw(sql_select, [name])
    form = CategoryRawModelForm()

    return render(request, 'catalog/category_raw.html', {
            'form': form,
            'category_objs': category_objs_raw,
            'active_tab': active_tab})


def category_raw_one(request):
    category_objs_raw = category_raw_sql_get_one(1)
    form = CategoryRawModelForm()

    return render(request, 'catalog/category_raw.html', {
            'form': form,
            'category_objs': category_objs_raw,
            'active_tab': active_tab})


def category_raw_all(request):
    category_objs_raw = category_raw_sql_get_all()
    form = CategoryRawModelForm()

    return render(request, 'catalog/category_raw.html', {
            'form': form,
            'category_objs': category_objs_raw,
            'active_tab': active_tab})


def python_func_get_category_id():
    """
    Function get category_id with maximum numbers of items
    """
    sql_select = '''select category_id, max(num) as max_num
                    from (select category_id, count(*) as num
                    from catalog_item
                    group by category_id)'''
    with connection.cursor() as cursor:
        cursor.execute(sql_select)
        result = cursor.fetchone()

    return result[0]


def category_raw_by_func(request):
    con = sqlite3.connect(":memory:")
    con.create_function('db_func_get_category_id', 0,
                        python_func_get_category_id)
    cur = con.cursor()
    ql = QueryLogger()
    with connection.execute_wrapper(ql):
        cur.execute('select db_func_get_category_id()')
        category_id = cur.fetchone()[0]
        category_objs_raw = category_raw_sql_get_one(category_id)
    logger.info(str(ql))
    form = CategoryRawModelForm()

    return render(request, 'catalog/category_raw_by_func.html', {
            'form': form,
            'category_objs': category_objs_raw,
            'active_tab': active_tab})

