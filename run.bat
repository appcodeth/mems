python build/scripts-3.7/odoo -r openpg -w openpgpwd ^
    --db-filter=mems ^
    --addons-path="D:\Solutions\Mems\mems\custom_addons" ^
    --update=mems_theme,mems_master,mems_purchase,mems_equipment,mems_pulling,mems_repair,mems_inventory,mems_report,mems_dashboard,mems_i18n ^
    --i18n-overwrite
