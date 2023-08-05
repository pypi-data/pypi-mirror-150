"""코드 참고 용
"""
from django.db import models

from core.models import NullCharField

exclude_fields = ['row_stat']


class BaseModel(models.Model):
    first_rg_yms = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    first_rg_idf = NullCharField(max_length=20, blank=True, null=True)
    last_update_yms = models.DateTimeField(blank=True, null=True, auto_now=True)
    last_update_idf = NullCharField(max_length=20, blank=True, null=True)

    # row 상태 칼럼 추가 - 테이블에 없는 칼럼(저장 안함)
    # row_stat = models.CharField(max_length=20, null=True, blank=True, default='unchanged')

    class Meta:
        abstract = True

    # def get_update_fields(self):
    #     # return list(x.attrname for x in self._meta.fields if x.attrname not in exclude_fields)
    #     return {'pgm_id', 'pgm_name', 'system_code', 'pgm_type', 'pgm_url', 'use_yn', 'first_rg_yms', 'first_rg_idf', 'last_update_yms', 'last_update_idf'}

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # force_insert = True
        # force_update = True
        # update_fields = self.get_update_fields()
        super().save(force_insert, force_update, using, update_fields)


class ProgramModel(BaseModel):
    pgm_id = models.CharField(primary_key=True, max_length=20)
    pgm_name = models.CharField(max_length=100)
    system_code = models.CharField(max_length=10)
    pgm_type = models.CharField(max_length=10)
    pgm_url = NullCharField(max_length=200, blank=True, null=True)
    use_yn = NullCharField(max_length=1, blank=True, null=True, default='N')

    class Meta:
        managed = False
        db_table = 'cm_program'
