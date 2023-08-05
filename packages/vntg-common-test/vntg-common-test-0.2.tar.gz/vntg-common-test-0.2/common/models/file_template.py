from django.db import models

from core.models import BaseTableModel, NullTextField, NullCharField


class CmTemplate(BaseTableModel):
    mgt_sno = models.AutoField(primary_key=True)
    rg_date = models.DateTimeField(blank=True, null=True)
    ctnt = NullCharField(max_length=500, blank=True, null=True)
    rg_emp_no = NullCharField(max_length=20, blank=True, null=True)
    email_attach_no = NullCharField(max_length=20, blank=True, null=True)
    attach_id = NullCharField(max_length=36, blank=True, null=True)
    remark = NullCharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_template'
