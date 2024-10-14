from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class AssignTask(models.TransientModel):
    _name = 'assign.task.wizard'
    _description = 'Assign Task Wizard'

    partner_id = fields.Many2one('res.partner', string='Assign To')
    todo_task_ids = fields.Many2many('todo.task')

    def confirm_user(self):
        for task in self.todo_task_ids:
            if task.state in ['completed', 'closed']:
                raise ValidationError(_(f'Tasks in state completed or closed can\'t be Re-assigned, task: {task.name}'))
            task.write({'partner_id': self.partner_id.id})
