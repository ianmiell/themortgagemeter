# Clear the cache
mkdir -p /tmp/tmpcacheclear
cd /tmp/tmpcacheclear
wget --quiet -o /dev/null http://localhost/rest/clear_cache
cd -
# restart the site
./restart_site.exp
cd -
# Restore the cache
wget --quiet -o /dev/null http://localhost/rest/latest_n_changes/0
wget --quiet -o /dev/null http://localhost/rest/graphs
wget --quiet -o /dev/null http://localhost/rest/best_mortgages/0/X/X/X/6000/0
rm -rf *
cd -

