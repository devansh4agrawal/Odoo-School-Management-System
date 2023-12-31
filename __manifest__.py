{
    'name': 'School Management',
    'version': '1.0',
    'category': 'Apps',
    'website': 'www.google.com',
    'author': 'Devansh Agrawal',
    'depends': ['base', 'mail', 'sale', 'account', 'point_of_sale'],
    'data': [
        "security/ir.model.access.csv",
        "views/relation.xml",
        "views/school_mang.xml",
        "views/teacher.xml",
        "views/fee.xml",
        "views/labs.xml",
        "views/standard.xml",
        "views/config_setting.xml",
        "views/school_config_setting.xml",
        # "views/templates.xml",
        "report/student_receipt_template.xml",
        "report/student_cron_job.xml",
        "report/student_confirm_email.xml",
        # "report/student_xls_template.xml",
        # 'wizard/excel_wizard.xml',
        'wizard/student_wizard.xml',
        'wizard/student_admission_status.xml',
        'wizard/student_result.xml',
        # "data/demo.xml",
        "views/menu.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'school/static/src/**/*',
        ],
    },
    "application": True,
    "auto_install": True,
    "sequence": 1
}
