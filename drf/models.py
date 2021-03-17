from django.db import models


# Create your models here.

class Bookinfo(models.Model):
    btitle = models.CharField(max_length=200)
    bpub_date = models.DateField(blank=True, null=True)
    bread = models.IntegerField()
    bcomment = models.IntegerField()
    bimage = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'bookinfo'

    def to_dict(self):
        return {
            'btitle': self.btitle,
            'bpub_date': self.bpub_date,
            'bread': self.bread,
            'bcomment': self.bcomment,
            'bimage': self.bimage,
        }


class Heroinfo(models.Model):
    hid = models.AutoField(primary_key=True)
    hname = models.CharField(max_length=50)
    bid = models.ForeignKey(Bookinfo, models.DO_NOTHING, db_column='bid', blank=True, null=True)

    class Meta:
        db_table = 'heroinfo'
