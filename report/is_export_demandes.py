# -*- coding: utf-8 -*-

from openerp import tools
from openerp.osv import fields,osv

class is_export_demandes(osv.osv):
    _name = "is.export.demandes"
    _description = "Exportation des demandes"
    _auto = False
    _columns = {
        'name': fields.char('N°demande'),
        'createur': fields.char('Créateur'),
        'demandeur': fields.char('Demandeur'),
        'date_demande': fields.date('Date demande', readonly=True),
        'application': fields.char('Application concernée'),
        'demande': fields.text('Demande'),
        'etude': fields.text('Étude'),
        'tps_prevu': fields.float('Temps prévu'),
        'date_validation': fields.date('Date validation'),
        'date_realisation': fields.date('Date réalisation'),
        'tps_passe': fields.float('Temps passé'),
        'facture': fields.char('Facture'),
        'state': fields.selection([('a_chiffrer' , u'A Chiffrer'),
                                   ('a_valider'  , u'A Valider'),
                                   ('a_realiser' , u'A Réaliser'),
                                   ('a_facturer' , u'A Facturer'),
                                   ('facture'    , u'Facturé')], 'Etat'),
    }
    _order = 'name desc'

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'is_export_demandes')
        cr.execute("""
                CREATE OR REPLACE view is_export_demandes AS (
                    SELECT
                        gd.id as id,
                        gd.name as name,
                        rp1.name as createur,
                        rp2.name as demandeur,
                        gd.date_demande as date_demande,
                        ia.name as application,
                        gd.demande as demande,
                        gd.etude as etude,
                        gd.tps_prevu as tps_prevu,
                        gd.date_validation as date_validation,
                        gd.date_realisation as date_realisation,
                        gd.tps_passe as tps_passe,
                        gd.facture as facture,
                        gd.state as state
                    FROM is_gestion_demandes gd LEFT OUTER JOIN res_users   ru1 ON gd.createur_id=ru1.id 
                                                LEFT OUTER JOIN res_partner rp1 ON ru1.partner_id=rp1.id

                                                LEFT OUTER JOIN res_users   ru2 ON gd.demandeur_id=ru2.id 
                                                LEFT OUTER JOIN res_partner rp2 ON ru2.partner_id=rp2.id

                                                LEFT OUTER JOIN is_application ia ON gd.application_id=ia.id 

                    WHERE gd.id>0 
                    ORDER BY gd.name DESC 
               )
        """)

#projets=# select ru.id,login,partner_id,rp.name from res_users ru left outer join res_partner rp  on ru.partner_id=rp.id  where ru.id=13;
#


#        'createur_id': fields.many2one('res.users', 'Créateur', readonly=True),

is_export_demandes()


