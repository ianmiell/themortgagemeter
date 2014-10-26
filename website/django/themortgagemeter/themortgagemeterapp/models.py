# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Turl(models.Model):
    url_id = models.IntegerField(primary_key=True)
    url = models.CharField(unique=True, max_length=200)
    def __unicode__(self):
        return self.url
    class Meta:
        db_table = u'turl'

class Talert(models.Model):
    alert_id = models.IntegerField()
    cr_date = models.DateTimeField()
    alert = models.TextField()
    status = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'talert'

class Tmailsubscriber(models.Model):
    email_address = models.TextField(primary_key=True)
    #cr_date = models.DateTimeField()
    class Meta:
        db_table = u'tmailsubscriber'

class Tretrievaldates(models.Model):
    day = models.DateField(primary_key=True)
    class Meta:
        db_table = u'tretrievaldates'

class Tmortgage(models.Model):
    mortgage_id = models.IntegerField(primary_key=True)
    institution_code = models.CharField(max_length=6)
    mortgage_type = models.TextField() # This field type is a guess.
    rate = models.IntegerField()
    apr = models.IntegerField()
    ltv = models.IntegerField()
    initial_period = models.IntegerField()
    booking_fee = models.IntegerField()
    term = models.IntegerField()
    eligibility = models.CharField(max_length=16)
    svr = models.IntegerField()
    def __unicode__(self):
        return self.mortgage_type + "|" + str(self.rate) + "|" + str(self.apr) + "|" + str(self.ltv) + "|" + str(self.initial_period) + "|" + str(self.booking_fee) + "|" + str(self.term)
    class Meta:
        db_table = u'tmortgage'

# cr_date deliberately left out of model as it doesn't like not nullity when saving.
class Tmailsubscriber(models.Model):
    email_address = models.TextField()
    def __unicode__(self):
        return self.email_address
    class Meta:
        db_table = u'tmailsubscriber'

class Tsavings(models.Model):
    savings_id = models.IntegerField(primary_key=True)
    institution_code = models.CharField(max_length=6)
    variability = models.TextField() # This field type is a guess.
    isa = models.TextField() # This field type is a guess.
    child = models.TextField() # This field type is a guess.
    online = models.TextField() # This field type is a guess.
    branch = models.TextField() # This field type is a guess.
    regular_saver = models.TextField() # This field type is a guess.
    regular_saver_frequency_period = models.IntegerField()
    regular_saver_frequency_type = models.TextField() # This field type is a guess.
    regular_saver_min_amt = models.IntegerField()
    regular_saver_max_amt = models.IntegerField()
    bonus = models.TextField() # This field type is a guess.
    bonus_frequency_period = models.IntegerField()
    bonus_frequency_type = models.TextField() # This field type is a guess.
    savings_period = models.IntegerField()
    min_amt = models.IntegerField()
    max_amt = models.IntegerField()
    gross_percent = models.IntegerField()
    aer_percent = models.IntegerField()
    interest_paid = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'tsavings'

class Tsavingsjrnl(models.Model):
    savings_jrnl_id = models.IntegerField(primary_key=True)
    cr_date = models.DateField()
    savings = models.ForeignKey(Tsavings)
    last_retrieved = models.DateField()
    delete_date = models.DateField()
    url_id = models.IntegerField()
    class Meta:
        db_table = u'tsavingsjrnl'

class Tmortgagejrnl(models.Model):
    mortgage_jrnl_id = models.IntegerField(primary_key=True)
    cr_date = models.DateField()
    mortgage = models.ForeignKey(Tmortgage)
    last_retrieved = models.DateField()
    delete_date = models.DateField()
    url_id = models.IntegerField()
    class Meta:
        db_table = u'tmortgagejrnl'

class Tinstitution(models.Model):
    institution_code = models.CharField(max_length=6, primary_key=True)
    institution_type = models.CharField(max_length=4)
    institution_name = models.CharField(max_length=100)
    mortgage_status = models.TextField() # This field type is a guess.
    def __unicode__(self):
        return self.institution_name
    class Meta:
        db_table = u'tinstitution'



class ReplacementMortgagesView(models.Model):
    change_date = models.DateField()
    institution_code = models.CharField(max_length=6)
    mortgage_type = models.TextField() # This field type is a guess.
    eligibility = models.CharField(max_length=16)
    ltv = models.IntegerField()
    initial_period = models.IntegerField()
    booking_fee = models.IntegerField()
    cr_date = models.DateField()
    delete_date = models.DateField()
    rate = models.IntegerField()
    svr = models.IntegerField()
    apr = models.IntegerField()
    last_retrieved = models.DateField()
    mortgage_id = models.IntegerField()
    institution_name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    action_type = models.TextField()
    class Meta:
        db_table = u'replacement_mortgages_view'

class ReplacementSavingsMaterializedView(models.Model):
    change_date = models.DateField()
    institution_code = models.CharField(max_length=6)
    variability = models.TextField() # This field type is a guess.
    isa = models.TextField() # This field type is a guess.
    child = models.TextField() # This field type is a guess.
    online = models.TextField() # This field type is a guess.
    branch = models.TextField() # This field type is a guess.
    interest_paid = models.TextField() # This field type is a guess.
    regular_saver = models.TextField() # This field type is a guess.
    regular_saver_frequency_period = models.IntegerField()
    regular_saver_frequency_type = models.TextField() # This field type is a guess.
    regular_saver_min_amt = models.IntegerField()
    regular_saver_max_amt = models.IntegerField()
    bonus = models.TextField() # This field type is a guess.
    bonus_frequency_period = models.IntegerField()
    bonus_frequency_type = models.TextField() # This field type is a guess.
    savings_period = models.IntegerField()
    min_amt = models.IntegerField()
    max_amt = models.IntegerField()
    gross_percent = models.IntegerField()
    aer_percent = models.IntegerField()
    last_retrieved = models.DateField()
    institution_name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    action_type = models.TextField()
    class Meta:
        db_table = u'replacement_savings_materialized_view'
