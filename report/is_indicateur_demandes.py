# -*- coding: utf-8 -*-

from openerp import tools
from openerp.osv import fields,osv

class is_indicateur_demandes(osv.osv):
    _name = "is.indicateur.demandes"
    _description = "Indicateurs sur les demandes"
    _auto = False
    _columns = {
        'name'          : fields.char('Application concernée'),
        'application_id': fields.many2one('is.gestion.demandes.application', 'Application concernée'),
        'commentaire'   : fields.char('Commentaire'),
        'tps_maxi_jour' : fields.float('Temps prévu maxi (Jour)'),
        'tps_passe'     : fields.float('Temps passé (Jour)'),
        'tps_restant'   : fields.float('Temps restant'),
        'avancement'    : fields.float('Avancement'),
    }
    _order = 'name'






    def init(self, cr):
        tools.drop_view_if_exists(cr, 'is_indicateur_demandes')
        cr.execute("""
                CREATE OR REPLACE view is_indicateur_demandes AS (
                    SELECT
                        ia.id as id,
                        ia.name as name,
                        ia.id as application_id,
                        ia.commentaire as commentaire,
                        ia.tps_maxi_jour as tps_maxi_jour,
                        sum(gd.tps_passe)/8 as tps_passe,
                        (ia.tps_maxi_jour - sum(gd.tps_passe)/8) as tps_restant,
                        (100*sum(gd.tps_passe)/ia.tps_maxi) as avancement
                    FROM is_gestion_demandes gd LEFT OUTER JOIN is_gestion_demandes_application ia ON gd.application_id=ia.id 
                    WHERE ia.id>0 and ia.tps_maxi>0
                    GROUP BY ia.id, ia.name
                    ORDER BY ia.name 
               )
        """)

is_indicateur_demandes()


