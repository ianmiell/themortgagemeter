from mortgagecomparisonapp.models import Turl, Tmortgage, Tinstitution, Tmortgagejrnl
from django.contrib import admin

class TurlAdmin(admin.ModelAdmin):
	fields = ['url_id','url']
admin.site.register(Turl,TurlAdmin)
admin.site.register(Tmortgage)
admin.site.register(Tinstitution)
admin.site.register(Tmortgagejrnl)
