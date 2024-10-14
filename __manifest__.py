{
    'name': 'To-Do App',
    'author': 'Shimaa Magdy',
    'version': '15.0.0.1.0',
    'summary': """To Do List""",
    'description': """todo list app""",
    'sequence': 3,
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/todo_task_view.xml',
        'views/base_menu.xml',
        'wizard/assign_tasks_wizard.xml',
        'reports/todo_task_report.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
