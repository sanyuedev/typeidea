from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html

from blog.adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site
from .models import Post, Category, Tag


# Register your models here.

class PostInline(admin.TabularInline):  # 可选择继承自 admin.StackInline 获取不同的展示样式
    """
    内链
    """
    fields = ('title', 'desc')

    extra = 1  # 控制额外多几个
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav',)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'post_count',)
    fields = ('name', 'status',)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    """定制的文章发表界面"""
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator',
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter, ]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    form = PostAdminForm

    # 编辑页面

    save_on_top = True

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tags',
    # )

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            )
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tags',),
        })
    )

    def operator(self, obj):
        """
        自定义
        :param obj:
        :return:
        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,)),
        )

    operator.short_description = '操作'

    class Media:
        css = {
            'all': ()
        }
        js = ()


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    """
    查询所有变更记录
    """
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
