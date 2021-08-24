python3 build/scripts-3.7/odoo -r openpg -w openpgpwd \
  --db_host=localhost \
  --db-filter=mems \
  --addons-path="/Users/ekkasit/Project/Mems/mems/odoo/addons,/Users/ekkasit/Project/Mems/mems/custom_addons" \
  --update=mems_theme,mems_master,mems_purchase,mems_equipment,mems_pulling,mems_repair,mems_inventory,mems_report,mems_dashboard,mems_i18n \
  --i18n-overwrite
