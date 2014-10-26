from django.conf.urls.defaults import *

urlpatterns = patterns('themortgagemeterapp.views',
    url(r'^$', 'home', name='home'),
    url(r'^api$', 'api'),
    url(r'conversions/$', 'get_conversions'),
    url(r'best_mortgages/(?P<num_results>[0-9]+)/(?P<mortgage_type>[FDVTOBX]+)/(?P<eligibility>[A-Z]+)/(?P<institution_code>[A-Z]+)/(?P<ltv>[0-9]+)/(?P<initial_period>[0-9]+)$', 'best_mortgages'),
	url(r'latest_n_changes/(?P<num_changes>[0-9]+)/$', 'latest_n_changes'),
	url(r'latest_n_changes_savings/(?P<num_changes>[0-9]+)/$', 'latest_n_changes_savings'),
	url(r'subscribe_email/(?P<email>.+)/$', 'subscribe_email'),
	url(r'unsubscribe_email/(?P<email>.+)/$', 'unsubscribe_email'),
	url(r'graphs/$', 'graphs'),
	url(r'clear_cache/$', 'clear_cache'),
)
