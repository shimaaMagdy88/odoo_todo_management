from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Todo Task'

    name = fields.Char(string='Task Name', required=1, translate=True)
    partner_id = fields.Many2one('res.partner', string='Assign To', required=0)
    description = fields.Text(translate=True)
    due_date = fields.Date(string='Due Date')
    state = fields.Selection([('new', 'New'),
                              ('in_progress', 'In Progress'),
                              ('completed', 'Completed'),
                              ('closed', 'Closed')], default='new', translate=True)
    estimated_time = fields.Float()
    timesheet_line_ids = fields.One2many('timesheet.line', 'task_id')
    count_hours = fields.Float(compute='_compute_count_hours')
    active = fields.Boolean(default=True)
    is_late = fields.Boolean()
    sequence = fields.Char(string='Sequence', readonly=True)

    def test(self):
        print('hh')
        # my_user_id = self.env['res.users'].browse(2)
        # print('user', my_user_id)
        # print('partner of this user', my_user_id.partner_id)
        if self.partner_id:
            print('current partner', self.partner_id)
            print('user of current partner', self.env['res.users'].search([('partner_id', '=', self.partner_id.id)]))
            print('--------------------')
            print('user of current partner', self.partner_id.user_id)
            print('user of current partner', self.partner_id.user_ids)

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('todo_task')
        return super(TodoTask, self).create(vals)

    @api.depends('timesheet_line_ids', 'estimated_time', 'timesheet_line_ids.hours')
    def _compute_count_hours(self):
        for rec in self:
            if rec.timesheet_line_ids:
                for line in rec.timesheet_line_ids:
                    rec.count_hours += line.hours
                    if rec.count_hours > rec.estimated_time:
                        raise ValidationError(_('Timesheet Hours Can\'t Exceed The Estimated Time'))
            else:
                rec.count_hours = rec.count_hours

    def action_new(self):
        for rec in self:
            rec.state = 'new'

    def action_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_completed(self):
        for rec in self:
            rec.state = 'completed'

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'

    def check_due_date(self):
        todo_task_ids = self.search([])
        for rec in todo_task_ids:
            if rec.due_date and fields.Date.today() > rec.due_date and rec.state in ['new', 'in_progress']:
                rec.is_late = True


class TimesheetLine(models.Model):
    _name = 'timesheet.line'

    date = fields.Date()
    description = fields.Text()
    hours = fields.Integer()
    task_id = fields.Many2one('todo.task')
