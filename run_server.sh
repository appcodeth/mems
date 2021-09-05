/opt/odoo11/odoo11env/bin/python3 /opt/odoo11/odoo11env/mems/build/scripts-3.7/odoo -r odoo13 -w odoo13 \
  --db_host=localhost \
  --db-filter=mems \
  --addons-path="/opt/odoo11/odoo11env/mems/odoo/addons,/opt/odoo11/odoo11env/mems/custom_addons" \
  --update=mems_theme,mems_master,mems_purchase,mems_equipment,mems_pulling,mems_repair,mems_inventory,mems_report,mems_dashboard,mems_i18n,login_controller \
  --i18n-overwrite --no-database-list

