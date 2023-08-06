from django.db import models
from django.contrib.postgres.fields import ArrayField


class BaseModel(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="最后更新时间"
    )

    class Meta:
        abstract = True


class Department(BaseModel):
    """
    部门表
    """
    name = models.CharField(max_length=32, verbose_name="部门名称")
    path = ArrayField(
        models.IntegerField(verbose_name="上级部门ID"),
        null=True,
        verbose_name="所属部门路径"
    )
    organization_id = models.IntegerField(verbose_name="组织id")
    is_deleted = models.BooleanField(default=False, verbose_name="部门是否删除, 默认False")

    class Meta:
        db_table = 'department'
        index_together = [
            ["organization_id", "is_deleted"]
        ]
        unique_together = [
            "name", "organization_id"
        ]


class DepartmentUserMap(BaseModel):
    """
    部门和用户的关系映射表
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="部门id")
    user_id = models.IntegerField(verbose_name="用户id")

    class Meta:
        db_table = 'department_user_map'
        unique_together = ["department", "user_id"]


class UserInformation(BaseModel):
    """
    用户信息表
    """
    user_id = models.IntegerField(verbose_name="用户id", unique=True)
    position = models.CharField(max_length=64, verbose_name="职位")
    leader_user_id = models.IntegerField(verbose_name="直属领导id")
    is_deleted = models.BooleanField(default=False, verbose_name="部门是否删除, 默认False")

    class Meta:
        db_table = 'user_information'
