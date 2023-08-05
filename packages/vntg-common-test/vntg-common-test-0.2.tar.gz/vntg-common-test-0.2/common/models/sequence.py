from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import BaseTableModel


class CmSequence(BaseTableModel):
    seq_name = models.CharField(verbose_name=_("seq_name"), max_length=100)
    prefix = models.CharField(primary_key=True, verbose_name=_("prefix"), max_length=50, default='default')
    padding = models.PositiveIntegerField(verbose_name=_("padding"), default=4)
    last_value = models.PositiveIntegerField(verbose_name=_("last_value"), editable=False)

    class Meta:
        managed = False
        db_table = 'cm_sequence'
        constraints = [
            models.UniqueConstraint(fields=['seq_name', 'prefix'], name='seq_prefix')
        ]
        verbose_name = _("sequence")
        verbose_name_plural = _("sequences")
