from django.db import models

from core.models import BaseTableModel


class CmCorporation(BaseTableModel):
    corp_code = models.CharField(primary_key=True, max_length=2)
    corp_no = models.CharField(max_length=13, blank=True, null=True)
    corp_name = models.CharField(max_length=50, blank=True, null=True)
    corp_name_en = models.CharField(max_length=100, blank=True, null=True)
    corp_sht_name = models.CharField(max_length=50, blank=True, null=True)
    rep_corp_yn = models.CharField(max_length=1, blank=True, null=True)
    president = models.CharField(max_length=50, blank=True, null=True)
    president_en = models.CharField(max_length=100, blank=True, null=True)
    prsd_sec_no = models.CharField(max_length=13, blank=True, null=True)
    biz_type = models.CharField(max_length=50, blank=True, null=True)
    biz_item = models.CharField(max_length=50, blank=True, null=True)
    tel_no = models.CharField(max_length=25, blank=True, null=True)
    fax_no = models.CharField(max_length=25, blank=True, null=True)
    zip_code = models.CharField(max_length=6, blank=True, null=True)
    addr = models.CharField(max_length=200, blank=True, null=True)
    addr_en = models.CharField(max_length=300, blank=True, null=True)
    foundation_date = models.DateTimeField(blank=True, null=True)
    remark = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_corporation'


class CmBusiplace(BaseTableModel):
    corp_code = models.CharField(max_length=2)
    busi_place = models.CharField(primary_key=True, max_length=1)
    business_no = models.CharField(max_length=13, blank=True, null=True)
    busi_place_name = models.CharField(max_length=50, blank=True, null=True)
    busi_place_name_en = models.CharField(max_length=100, blank=True, null=True)
    busi_place_sht_name = models.CharField(max_length=50, blank=True, null=True)
    rep_busi_place_yn = models.CharField(max_length=1, blank=True, null=True)
    president = models.CharField(max_length=50, blank=True, null=True)
    president_en = models.CharField(max_length=100, blank=True, null=True)
    biz_type = models.CharField(max_length=100, blank=True, null=True)
    biz_item = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=6, blank=True, null=True)
    addr = models.CharField(max_length=200, blank=True, null=True)
    addr_en = models.CharField(max_length=300, blank=True, null=True)
    tel_no = models.CharField(max_length=25, blank=True, null=True)
    fax_no = models.CharField(max_length=25, blank=True, null=True)
    tax_office_code = models.CharField(max_length=4, blank=True, null=True)
    hometax_id = models.CharField(max_length=20, blank=True, null=True)
    slave_busi_no = models.CharField(max_length=4, blank=True, null=True)
    sum_recog_no = models.CharField(max_length=7, blank=True, null=True)
    prsd_sec_no = models.CharField(max_length=13, blank=True, null=True)
    homepage = models.CharField(max_length=100, blank=True, null=True)
    cust_code = models.CharField(max_length=10, blank=True, null=True)
    item_code = models.CharField(max_length=6, blank=True, null=True)
    biz_date = models.DateTimeField(blank=True, null=True)
    remark = models.CharField(max_length=100, blank=True, null=True)
    busi_part = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_busiplace'
        # unique_together = (('corp_code', 'busi_place'),)
        constraints = [
            models.UniqueConstraint(fields=['corp_code', 'busi_place'], name='uk_cmbusiplace_corp_busi')
        ]