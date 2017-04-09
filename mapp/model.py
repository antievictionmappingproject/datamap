from cantools import db
from ctmap.model import *

class Parcel(db.ModelBase):
    building = db.ForeignKey(kind="building")
    parcel_id = db.String()
    dwelling_units = db.Integer()
    from_addr = db.String()
    to_addr = db.String()
    label = "parcel_id"

class Eviction(db.ModelBase):
    building = db.ForeignKey(kind="building")
    petition = db.String()
    date = db.DateTime()
    reason = db.String() # omi|ellis
    label = "petition"

class PropertyValue(db.ModelBase):
    building = db.ForeignKey(kind="building")
    year = db.Integer()
    value = db.Integer()
    label = "year"

class Owner(db.ModelBase):
    name = db.String()
    address = db.String()
    zipcode = db.ForeignKey(kind="zipcode")
    owner = db.ForeignKey(kind="owner") # to map front trees...
    # collections: buildings, owners

class Fire(db.ModelBase):
    date = db.DateTime()
    building = db.ForeignKey(kind="building")
    battalion = db.String()
    alarms = db.Integer()
    units = db.Integer()
    persons = db.Integer()
    injuries = db.Integer()
    fatalities = db.Integer()
    losses = db.Integer()
    label = "date"

class PoliceMurder(db.ModelBase):
    date = db.DateTime()
    name = db.String()
    age = db.Integer()
    race = db.String()
    photo = db.String()
    link = db.String()
    latitude = db.Float()
    longitude = db.Float()
    description = db.Text()
