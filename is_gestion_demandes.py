# -*- coding: utf-8 -*-

from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning
import datetime

class is_gestion_demandes_application(models.Model):
    _name = 'is.gestion.demandes.application'
    _description = u"Application"
    

    name          = fields.Char('Application', required=True)
    tps_mini      = fields.Float('Temps mini prévu (H)')
    tps_maxi      = fields.Float('Temps maxi prévue (H)')
    tps_mini_jour = fields.Float('Temps mini (Jour)' , compute="_compute", store=True)
    tps_maxi_jour = fields.Float('Temps maxi (Jour)' , compute="_compute", store=True)
    cout_horaire = fields.Float('Coût horaire')
    cout_mini    = fields.Float('Coût mini prévu'    , compute="_compute", store=True)
    cout_maxi    = fields.Float('Coût maxi prévue'   , compute="_compute", store=True)
    commentaire  = fields.Text('Commentaire')

    _defaults = {
        'cout_horaire': 37.5,
    }


    @api.depends('tps_mini','tps_maxi','cout_horaire')
    def _compute(self):
        for obj in self:
            obj.cout_mini = obj.tps_mini * obj.cout_horaire
            obj.cout_maxi = obj.tps_maxi * obj.cout_horaire
            obj.tps_mini_jour = obj.tps_mini/8
            obj.tps_maxi_jour = obj.tps_maxi/8


    

class is_gestion_demandes(models.Model):
    _name = 'is.gestion.demandes'
    _description = u"Gestion des demandes pour Plastigray"
    _order='name desc'    #Ordre de tri par defaut des listes


    name             = fields.Char('N°demande', readonly=True)
    createur_id      = fields.Many2one('res.users', 'Créateur', readonly=True)
    demandeur_id     = fields.Many2one('res.users', 'Demandeur', required=True)
    date_demande     = fields.Date('Date demande')
    application_id   = fields.Many2one('is.gestion.demandes.application', 'Application concernée')
    demande          = fields.Text('Demande', required=True)
    etude            = fields.Text('Étude')
    tps_prevu        = fields.Float('Temps prévu (H)')
    date_validation  = fields.Date('Date validation')
    date_prevue      = fields.Date('Date prévue')
    date_realisation = fields.Date('Date réalisation')
    tps_passe        = fields.Float('Temps passé (H)')
    tps_passe_jour   = fields.Float('Temps passé (Jour)', compute="_compute", store=True)
    montant_facture  = fields.Float('Montant à facturer', compute="_compute", store=True)
    facture          = fields.Char('Facture')
    state            = fields.Selection([
        ('a_chiffrer' , u'A Chiffrer'),
        ('a_valider'  , u'A Valider'),
        ('a_realiser' , u'A Réaliser'),
        ('a_facturer' , u'A Facturer'),
        ('facture'    , u'Facturé')
    ], 'Etat', select=True)


    _defaults = {
        'createur_id': lambda obj, cr, uid, context: uid,
        'demandeur_id': lambda obj, cr, uid, context: uid,
        'date_demande': datetime.date.today(),
        'state': 'a_chiffrer',
    }


    @api.depends('application_id','tps_passe')
    def _compute(self):
        for obj in self:
            cout_horaire=37.5
            if obj.application_id:
                cout_horaire=obj.application_id.cout_horaire
            obj.montant_facture = obj.tps_passe*cout_horaire
            obj.tps_passe_jour=obj.tps_passe/8





    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get('gestion.demandes.number') or ''
        return super(is_gestion_demandes, self).create(vals)


#    def write(self, cr, uid, ids, vals, context=None):
#        res = super(is_gestion_demandes, self).write(cr, uid, ids, vals, context=context)
#        obj = self.browse(cr, uid, ids[0], context=context)
#        vals["state"]=""
#        if obj.tps_prevu==0.0:
#            vals["state"]="a_chiffrer"
#        if obj.date_validation==False and obj.tps_prevu>0:
#            vals["state"]="a_valider"
#        if obj.date_validation<>False:
#            vals["state"]="a_realiser"
#        if obj.date_realisation<>False:
#            vals["state"]="a_facturer"
#        if obj.facture<>False:
#            vals["state"]="facture"
#        res = super(is_gestion_demandes, self).write(cr, uid, ids, vals, context=context)
#        return res




