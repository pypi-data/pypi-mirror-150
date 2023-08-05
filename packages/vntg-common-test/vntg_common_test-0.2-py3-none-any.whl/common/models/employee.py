from django.db import models

from core.models import BaseTableModel, NullCharField


class CmDepartment(BaseTableModel):
    dept_code = models.CharField(primary_key=True, max_length=20)
    corp_code = models.CharField(max_length=10)
    busi_place = models.CharField(max_length=10)
    dept_name = models.CharField(max_length=50)
    parent_dept_code = NullCharField(max_length=9, blank=True, null=True)
    dept_type = NullCharField(max_length=10, blank=True, null=True)
    term_fr = models.DateTimeField(blank=True, null=True)
    term_to = models.DateTimeField(blank=True, null=True)
    print_seq = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_department'


class CmEmployee(BaseTableModel):
    emp_no = models.CharField(primary_key=True, max_length=10)
    corp_code = models.CharField(max_length=10)
    busi_place = models.CharField(max_length=10)
    emp_name = models.CharField(max_length=50)
    emp_name_en = NullCharField(max_length=100, blank=True, null=True)
    emp_name_cn = NullCharField(max_length=20, blank=True, null=True)
    dept_code = NullCharField(max_length=20, blank=True, null=True)
    unit_work_no = NullCharField(max_length=20, blank=True, null=True)
    plant_code = NullCharField(max_length=10, blank=True, null=True)
    equip_code = NullCharField(max_length=10, blank=True, null=True)
    unit_work_code = NullCharField(max_length=10, blank=True, null=True)
    emp_grd = NullCharField(max_length=10, blank=True, null=True)
    position = NullCharField(max_length=10, blank=True, null=True)
    responsi = NullCharField(max_length=10, blank=True, null=True)
    duty = NullCharField(max_length=10, blank=True, null=True)
    occup_kind = NullCharField(max_length=10, blank=True, null=True)
    ent_code = NullCharField(max_length=10, blank=True, null=True)
    ent_date = models.DateTimeField(blank=True, null=True)
    grp_ent_date = models.DateTimeField(blank=True, null=True)
    curr_stat = NullCharField(max_length=10, blank=True, null=True)
    curr_stat_date = models.DateTimeField(blank=True, null=True)
    retire_code = NullCharField(max_length=10, blank=True, null=True)
    retire_date = models.DateTimeField(blank=True, null=True)
    retire_calc_date = models.DateTimeField(blank=True, null=True)
    on_work_yn = NullCharField(max_length=1, blank=True, null=True)
    personal_sec_no = NullCharField(max_length=13, blank=True, null=True)
    gender = NullCharField(max_length=10, blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    birthday_type = models.CharField(max_length=10, blank=True, null=True)
    zipcode = NullCharField(max_length=6, blank=True, null=True)
    addr = NullCharField(max_length=100, blank=True, null=True)
    tel_no = NullCharField(max_length=20, blank=True, null=True)
    mobile_no = NullCharField(max_length=20, blank=True, null=True)
    email = NullCharField(max_length=100, blank=True, null=True)
    live_nation_code = NullCharField(max_length=10, blank=True, null=True)
    foreigner_type = NullCharField(max_length=10, blank=True, null=True)
    user_id = NullCharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_employee'
