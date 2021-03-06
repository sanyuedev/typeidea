#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/11/20 04:01
# @Author  : 三哥
# @Site    : 
# @File    : apis.py
# @Software: PyCharm
from rest_framework.permissions import IsAdminUser

from .models import Post, Category, Tag
from .serializers import PostSerializer, PostDetailSerializer, CategorySerializer, CategoryDetailSerializer
from rest_framework import viewsets


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """提供文章接口"""
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)

    # permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        # 获取参数 self.request.query_params.get('category') 即 category?category=id
        # 不是 /category/id 之前一直搞错
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        print(category_id)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Post.STATUS_NORMAL)

    # TODO:学习这个函数
    def retrieve(self, request, *args, **kwargs):
        """重写retrieve 更改获取单个数据为多个数据"""
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)
