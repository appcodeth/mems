from odoo import models, fields, api, exceptions


class ServiceRequest(models.Model):
    _name = 'mems.sr'
    _order = 'name desc'
    _rec_name = 'name'
    name = fields.Char('Name')
    date_order = fields.Date('Order Date', default=fields.Date.today())
    department_id = fields.Many2one('mems.department', string='Department', required=True)
    equip_id = fields.Many2one('mems.equipment', string='Equipment', required=True, domain=[('state', '=', 'active')])
    equip_code = fields.Char('Code', related='equip_id.code', readonly=True, store=True)
    equip_brand = fields.Char('Brand', readonly=True, store=True)
    equip_model = fields.Char('Model', related='equip_id.model_name', readonly=True, store=True)
    equip_price = fields.Float('Unit Price', related='equip_id.unit_price', readonly=True, store=True)
    equip_sn = fields.Char('S/N', related='equip_id.serial_no', readonly=True, store=False)
    equip_warty_type = fields.Selection('Warranty Type', related='equip_id.warranty_type', readonly=True, store=False)
    equip_warty_expire = fields.Date('Warranty Expire', related='equip_id.warranty_end_date', readonly=True, store=False)
    equip_image = fields.Binary('Image', related='equip_id.image', readonly=True, store=False)
    problem_text = fields.Text('Problem Description')
    image_attachments = fields.Many2many('ir.attachment', string='Image Attachment')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user.id)
    responsible_id = fields.Many2one('res.users', string='Responsible')
    remark = fields.Text('Remark')
    date_plan = fields.Date('Plan Date')
    date_finish = fields.Date('Finish Date')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approve'),
        ('cancel', 'Cancel'),
        ('close', 'Close'),
    ], string='Status', default='draft')

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('sr.sr_no') or '-'
        vals['name'] = seq
        return super(ServiceRequest, self).create(vals)

    def do_sr_approve(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.sr.approve.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_sr_id': self.id,
                'default_sr_name': self.name,
            }
        }

    def do_sr_cancel(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.sr.cancel.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_sr_id': self.id,
                'default_sr_name': self.name,
            }
        }

    def do_sr_email(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('mems_repair', 'mail_template_sr_form')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'mems.sr',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': ctx,
            'res_model': 'mail.compose.message',
            'view_id': compose_form_id,
            'views': [(compose_form_id, 'form')],
        }

    def do_sr_print(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.report',
            'report_name': 'mems_repair.sr_form',
            'model': 'mems.sr',
            'report_type': 'qweb-pdf',
        }
