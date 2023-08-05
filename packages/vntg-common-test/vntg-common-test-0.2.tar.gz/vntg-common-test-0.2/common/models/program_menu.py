from django.db import models
from django.db.models import UniqueConstraint

from core.models import BaseTableModel, NullCharField


class CmProgram(BaseTableModel):
    """프로그램 목록
    """
    pgm_id = models.CharField(primary_key=True, max_length=20)
    pgm_name = models.CharField(max_length=100)
    system_code = models.CharField(max_length=10)
    pgm_type = models.CharField(max_length=10)
    pgm_url = NullCharField(max_length=200, blank=True, null=True)
    use_yn = NullCharField(max_length=1, blank=True, null=True, default='N')

    class Meta:
        managed = False
        db_table = 'cm_program'


class CmMenu(BaseTableModel):
    """메인 메뉴(구조 정보)
    """
    menu_sno = models.IntegerField(primary_key=True)
    menu_name = models.CharField(max_length=100)
    system_type = models.CharField(max_length=10)
    parent_menu_sno = models.IntegerField(blank=True, null=True)
    sort_seq = models.IntegerField(blank=True, null=True)
    use_yn = NullCharField(max_length=1, blank=True, null=True, default='N')

    class Meta:
        managed = False
        db_table = 'cm_menu'


class CmMenuPgm(BaseTableModel):
    """메인 메뉴 프로그램
    """
    run_sno = models.IntegerField(primary_key=True)
    run_name = models.CharField(max_length=100)
    menu_sno = models.IntegerField()
    pgm_id = models.CharField(max_length=20)
    sort_seq = models.IntegerField(blank=True, null=True)
    use_yn = NullCharField(max_length=1, blank=True, null=True, default='N')

    class Meta:
        managed = False
        db_table = 'cm_menu_pgm'


class CmMenuParam(BaseTableModel):
    """메뉴 실행 파라미터
    """
    run_sno = models.IntegerField(primary_key=True)
    param_name = models.CharField(max_length=100)
    param_value = NullCharField(max_length=100, blank=True, null=True)
    remark = NullCharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_menu_param'
        # PK 칼럼 그룹 설정
        constraints = [
            UniqueConstraint(fields=['run_sno', 'param_name'], name='pk_cm_menu_param')
        ]


class CmMenuTree(BaseTableModel):
    """메뉴+프로그램+파라미터 정보
    """
    menu_tree_sno = models.CharField(primary_key=True, max_length=100)
    menu_sno = models.IntegerField()
    run_sno = models.IntegerField()
    menu_name = models.CharField(max_length=100)
    system_type = models.CharField(max_length=10)
    parent_menu_tree_sno = NullCharField(blank=True, null=True, max_length=100)
    pgm_type = models.CharField(max_length=10)
    pgm_id = models.CharField(max_length=20)
    pgm_url = models.CharField(max_length=200)
    pgm_param = models.CharField(max_length=200)
    sort_seq = models.IntegerField(blank=True, null=True)
    use_yn = NullCharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False


class CmUserMenu(BaseTableModel):
    user_id = models.CharField(primary_key=True, max_length=20)
    menu_sno = models.IntegerField()
    menu_name = models.CharField(max_length=100)
    parent_menu_sno = models.IntegerField(blank=True, null=True)
    sort_seq = models.IntegerField(blank=True, null=True)
    first_rg_yms = models.DateTimeField(blank=True, null=True)
    first_rg_idf = NullCharField(max_length=20, blank=True, null=True)
    last_update_yms = models.DateTimeField(blank=True, null=True)
    last_update_idf = NullCharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_user_menu'
        # unique_together = (('user_id', 'menu_sno'),)
        # PK 칼럼 그룹 설정
        constraints = [
            UniqueConstraint(fields=['user_id', 'menu_sno'], name='pk_cm_user_menu')
        ]


class CmUserMenuPgm(BaseTableModel):
    user_id = models.CharField(primary_key=True, max_length=20)
    menu_sno = models.IntegerField()
    run_sno = models.IntegerField()
    run_name = models.CharField(max_length=100)
    sort_seq = models.IntegerField(blank=True, null=True)
    first_rg_yms = models.DateTimeField(blank=True, null=True)
    first_rg_idf = NullCharField(max_length=20, blank=True, null=True)
    last_update_yms = models.DateTimeField(blank=True, null=True)
    last_update_idf = NullCharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_user_menu_pgm'
        # unique_together = (('user_id', 'menu_sno', 'run_sno'),)
        # PK 칼럼 그룹 설정
        constraints = [
            UniqueConstraint(fields=['user_id', 'menu_sno', 'run_sno'], name='pk_cm_user_menu_pgm')
        ]