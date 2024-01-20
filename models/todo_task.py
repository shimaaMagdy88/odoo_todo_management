from odoo import api, fields, models

class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Todo Task'

    name = fields.Char(string='Task Name')
    partner_id = fields.Many2one('res.partner', string='Assign To')
    description = fields.Text()
    due_date = fields.Date(string='Due Date')
    state = fields.Selection([('new', 'New'),
                              ('in_progress', 'In Progress'),
                              ('completed', 'Completed')], default='new')

    def action_new(self):
        self.state = 'new'

    def action_in_progress(self):
        self.state = 'in_progress'

    def action_completed(self):
        self.state = 'completed'
