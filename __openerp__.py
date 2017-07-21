# -*- coding: utf-8 -*-

{
    'name'     : 'Gestion des demandes pour Plastigray',
    'version'  : '1.0',
    'author'   : "InfoSaône",
    'category' : "InfoSaône\Plastigray",
    'description': """
Gestion des demandes pour Plastigray
""",
    'maintainer': 'InfoSaône',
    'website': 'http://www.infosaone.com',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'is_gestion_demandes_view.xml',
        'data/sequence.xml',
        'report/is_export_demandes.xml',
        'report/is_indicateur_demandes.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

