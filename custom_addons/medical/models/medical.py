# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class HealthCenters(models.Model):
    _inherit = 'res.partner'

    building_count = fields.Integer(compute='_building_count', string='Buildings')

    @api.depends()
    def _building_count(self):
        mb_obj = self.env['medical.buildings']
        for centers in self:
            centers.building_count = len(mb_obj.search([['health_centers', '=', centers.id]]))
    
class Building(models.Model):
    _name = 'medical.buildings'

    name = fields.Char(string="Building Name", required=True)
    health_centers = fields.Many2one('res.partner', string="Health Center", required=True)
    code = fields.Integer(string="Code")

    ward_count = fields.Integer(compute="_ward_count")
    beds_count = fields.Integer(compute="_beds_count")
    theaters_count = fields.Integer(compute="_theaters_count")

    @api.depends()
    def _ward_count(self):
        mw_obj = self.env['medical.wards']
        for building in self:
            building.ward_count = len(mw_obj.search([['building', '=', building.id]]))

    @api.depends()
    def _beds_count(self):
        mb_obj = self.env['medical.beds']
        for building in self:
            building.beds_count = len(mb_obj.search([['building', '=', building.id]]))

    @api.depends()
    def _theaters_count(self):
        mt_obj = self.env['medical.theaters']
        for building in self:
            building.theaters_count = len(mt_obj.search([['building', '=', building.id]]))

class Wards(models.Model):
    _name = 'medical.wards'

    name = fields.Char(string="Ward Name")
    # image = fields.Boolean()
    health_center = fields.Many2one('res.partner', string="Health Center")
    floor_number = fields.Char(string="Floor Number")
    private_room = fields.Boolean(string="Private Room")
    building = fields.Many2one('medical.buildings', string="Building")
    gender = fields.Selection([('unisex_ward', "Unisex Ward"),
        ('men_ward', "Men Ward"),
        ('female_ward', "Female Ward"),])
    bio_hazard = fields.Boolean(string="Bio Hazard")
    telephone_access = fields.Boolean(string=" Telephone access")
    private_bathroom = fields.Boolean(string="Private Bathroom")
    television = fields.Boolean(string="Television")
    refrigerator = fields.Boolean(string="Refrigerator")
    air_conditioning = fields.Boolean(string="Air Conditioning")
    guest_sofa_bed = fields.Boolean(string="Guest sofa-bed")
    internet_access = fields.Boolean(string="Internet Access")
    microwave = fields.Boolean(string="Microwave")

    beds_count = fields.Integer(compute="_beds_count")
    bed_count = fields.Integer(string="Bed counts")

    @api.depends()
    def _beds_count(self):
        mb_obj = self.env['medical.beds']
        for ward in self:
            ward.beds_count = len(mb_obj.search([['ward', '=', ward.id]]))


    @api.onchange('building')
    def change(self):
            self.bed_count = self.beds_count


class Beds(models.Model):
    _name = 'medical.beds'

    name = fields.Char(string="Bed Name")
    health_center = fields.Many2one('res.partner', string="Health Center")
    telephone_number = fields.Char(string="Telephone Number")
    reservation_charge = fields.Char(string="Reservation Charge", default=100)
    building = fields.Many2one('medical.buildings', string="Building")
    ward = fields.Many2one('medical.wards', string="Ward")
    bed_type = fields.Selection([
        ('gatch_bed', "Gatch Bed"),
        ('electric', "Electric"),
        ('other', "Other"),])
    change_bed_status = fields.Selection([
        ('1', "Mark as Reserved"),
        ('0', "Mark as Not Reserved"),])

    state = fields.Selection([
        ('free', "Free"),
        ('reserved', "Reserved"),
        ('occupied', "Occupied"),
        ('not_available', "Not Available"),
    ], default='free')

    @api.one
    def bed_free(self):
        self.write({
            'state': 'free',
            })

    @api.one
    def bed_reserved(self):
        self.write({
            'state': 'reserved',
            })

    @api.one
    def bed_occupied(self):
        self.write({
            'state': 'occupied',
            })

    @api.one
    def bed_not_available(self):
        self.write({
            'state': 'not_available',
            })

class Theaters(models.Model):
    _name = 'medical.theaters'

    name  = fields.Char(string="Operating Theaters Name")
    building = fields.Many2one('medical.buildings', string="Building")
    
    state = fields.Selection([
        ('free', "Free"),
        ('not_available', "Not Available"),
    ], default='free')

    @api.one
    def theater_free(self):
        self.write({
            'state': 'free',
            })

    @api.one
    def theater_not_available(self):
        self.write({
            'state': 'not_available',
            })

class Pharmacies(models.Model):
    _inherit = 'res.partner'

    pharmacy_name = fields.Char(string="Pharmacy Name")
    health_centers = fields.Many2one('res.partner', string="Health Center")
    prescription = fields.One2many('medical.prescription', 'partner_id', string="Pharmacy Lines")

    
class Test(models.Model):
    _name = 'medical.prescription'

    partner_id = fields.Many2one('res.partner', string="Partner")
    prescription = fields.Char(string="Prescription")
    physician = fields.Char(string="Physician")
    patient = fields.Char(string="Patient")
    total = fields.Integer(string="Total")
    state = fields.Selection([
        ('draft', "Draft"),
        ('invoiced', "Invoiced"),
    ], default='draft')

    @api.one
    def state_change(self):
        self.write({
            'state': 'invoiced',
            })


class Patients(models.Model):
    _inherit = 'res.partner'

    file = fields.One2many('ir.attachment', 'id', string='Files')



    # fields.Many2one('medical.upload', string="Files")
    patient_age = fields.Char(string="Patient Age", readonly=True)
    blood_type = fields.Selection([
        ('ap', "A +ve"),
        ('bp', "B +ve"),
        ('op', "O +ve"),
        ('abp', "AB +ve"),
        ('an', "A -ve"),
        ('bn', "B -ve"),
        ('on', "O -ve"),
        ('abn', "AB -ve"),
    ], default='ap')


    fields.Char(string=" Blood Type")


    gender = fields.Selection([
        ('male', "Male"),
        ('female', "Female"),
    ], default='male')

    responsible = fields.Char(string="Responsible") 
    date_of_birth = fields.Datetime(string="Date Of Birth", default=datetime.datetime.now()) 
    marital_status = fields.Selection([
        ('single', "Single"),
        ('married', "Married"),
    ], default='single')

    rh = fields.Selection([
        ('n', "-"),
        ('p', "+"),
    ], default='n')

    family_physician = fields.Selection([
        ('p1', "Family Physician1"),
        ('p2', "Family Physician2"),
    ], default='p1')

    @api.onchange('date_of_birth')
    def change(self):
            dob = self.date_of_birth
            dob1 = datetime.datetime.strptime(dob, '%Y-%m-%d %H:%M:%S')
            crt = datetime.datetime.now()
            if int(dob1.strftime('%Y')) > int(crt.strftime('%Y')):
                self.patient_age = int(dob1.strftime('%Y'))-int(crt.strftime('%Y'))

            else:
                self.patient_age = 0
            # int(dob.strftime('%Y'))
            # d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Admissions(models.Model):
    _name = 'medical.admissions'

    patient = fields.Many2one('res.partner', string="Patient")
    reason_for_dmission = fields.Char(string="Reason for Admission")
    ward = fields.Many2one('medical.wards', string="Ward")
    bed = fields.Many2one('medical.beds', string="Bed")
    theaters = fields.Many2one('medical.theaters', string="Operating Theater")
    admission_type = fields.Char(string="Admission Type")
    attending_physician = fields.Char(string="Attending Physician")
    operating_physician = fields.Many2one('medical.physicians', string="Operating Physician")
    queue = fields.Char(string="Queue")
    hospitalization_date = fields.Datetime(string="Hospitalization Date")
    discharge_date = fields.Datetime(string="Discharge Date")
    condition_before_admission = fields.Text(string="Condition before Admission")
    nursing_plan = fields.Text(string="Nursing Plan")
    discharge_plan = fields.Text(string="Discharge Plan")
    state = fields.Selection([('draft', "Draft"),
        ('hospitalized', "Hospitalized"),
        ('invoiced', "Invoiced"),
        ('discharge', "Discharged"),
        ], default='draft')

    @api.one
    def state_hospitalized(self):
        self.write({
            'state': 'hospitalized',
            })

    @api.one
    def state_invoiced(self):
        self.write({
            'state': 'invoiced'
            })

    @api.one
    def state_discharge(self):
        self.write({
            'state': 'discharge'
            })

    @api.multi
    def get_upd(self):
        base_url = self.env['medical.invoice']
        base_url.create({'reservation_charge': self.bed.reservation_charge, 
            'patient': self.patient.name, 
            'hospitalization_date': self.hospitalization_date, 
            'discharge_date': self.discharge_date})
        

class Physicians(models.Model):
    _name = 'medical.physicians'

    name = fields.Char(string="Physician Name")
    image = fields.Binary("Image", attachment=True)
    speciality = fields.Char()
    degree = fields.Char(string="Degrees")
    graduation_institute = fields.Char(string="Graduation Institute")
    consultancy_type = fields.Char(string="Consultancy Type")
    consultancy_charge = fields.Char(string="Consultancy Charge", default=100)
    licence_id = fields.Char(string="Licence ID")
    working_institution = fields.Char(string="Working Institution")
    work_mobile = fields.Char(string="Work Mobile")
    work_email = fields.Char(string="Work Email")
    responsible = fields.Char(string="Responsible")
    work_phone = fields.Char(string="Work Phone")
    work_location = fields.Char(string="Work Location")

class PatientInvoice(models.Model):
    _name = 'medical.invoice'
    
    patient = fields.Char(string="Patient Name")
    hospitalization_date = fields.Char(string="Hospitalization Date")
    discharge_date = fields.Char(string="Discharge Date")
    reservation_charge = fields.Float(string="Reservation Charge")
    days = fields.Integer(compute='_change')
    untaxed_amount = fields.Integer(compute='_untax', string="Untaxed Amount")
    tax = fields.Integer(compute='_untax', default=2)
    total =fields.Integer(compute='_untax', default=1, string="Toatal")
    doh = datetime.datetime.now()
    dod = datetime.datetime.now()

    @api.depends()
    def _untax(self):
        for x in self:
            x.untaxed_amount = x.reservation_charge * x.days
            x.tax = x.reservation_charge*2/100
            x.total = x.untaxed_amount + x.tax

    @api.depends()
    def _change(self):
        for l in self:
            doh1 = datetime.datetime.strptime(l.hospitalization_date, '%Y-%m-%d %H:%M:%S')
            dod1 = datetime.datetime.strptime(l.discharge_date, '%Y-%m-%d %H:%M:%S')

            if int(doh1.strftime('%d')) == int(dod1.strftime('%d')):
                l.days = 1 
            else:
                l.days = int(dod1.strftime('%d')) - int(doh1.strftime('%d'))