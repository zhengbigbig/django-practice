from django.db import models


# Create your models here.

class Bookinfo(models.Model):
    bid = models.AutoField(primary_key=True, db_column='id')
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
    bid = models.ForeignKey(Bookinfo, db_column='bid', blank=True, null=True, on_delete=models.CASCADE,
                            related_name='heros')

    def __str__(self):
        return self.hname

    class Meta:
        db_table = 'heroinfo'


class User(models.Model):
    username = models.CharField(max_length=30)
    password_hash = models.CharField(max_length=20, db_column='password')
    age = models.IntegerField(default=0)

    class Meta:
        db_table = 'user_drf'
