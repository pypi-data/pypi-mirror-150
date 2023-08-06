# -*- coding: utf-8 -*-
"""
@File        : department.py
@Author      : yu wen yang
@Time        : 2022/4/28 2:25 下午
@Description :
"""
import math

from django.http import JsonResponse, HttpRequest
from rest_framework.exceptions import APIException

from departments.models import Department
from departments.forms.forms import (
    DepartmentForms,
)


def get_department_list(params: dict) -> JsonResponse:
    """
    部门列表
    """
    page = params.get("page", "1")
    if not page.isdigit():
        raise APIException("参数错误")
    size = params.get("size", "20")
    if not size.isdigit():
        raise APIException("参数错误")
    organization_id = params.get("organization_id", "")
    if not organization_id or not organization_id.isdigit():
        raise APIException("参数错误")
    department_list = Department.objects.filter(
        organization_id=organization_id,
        is_deleted=False
    ).only('name').order_by("-id")
    total = department_list.count()
    max_page = math.ceil(total / size)
    items = [
        {
            'id': item.id,
            'name': item.name
        } for item in department_list
    ] if page <= max_page else []

    return JsonResponse(data={
        "total": total,
        "page": page,
        "max_page": max_page,
        "items": items
    })


def create_department(data: dict) -> JsonResponse:
    """
    新增部门
    """

    checked = DepartmentForms(data)
    if not checked.is_valid():
        raise APIException(str(checked.errors))
    organization_type = Department.objects.create(**data)
    return JsonResponse(data={'id': organization_type.pk})
