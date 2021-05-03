from database import db
from .users import UserModel
from datetime import datetime
from dateTimeHelper import get_current_IST_dt
from enums.statusEnum import StatusTypes
#https://medium.com/the-andela-way/how-to-create-django-like-choices-field-in-flask-sqlalchemy-1ca0e3a3af9d

class UserJobsModel(db.Model):
    __tablename__ = "userJobs"

    _id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey(UserModel._id),nullable=False)
    createdAt=db.Column(db.DateTime, nullable=False, default=get_current_IST_dt())
    lastModified=db.Column(db.DateTime, nullable=False, default=get_current_IST_dt())
    jobTitle = db.Column(db.String(100))
    company = db.Column(db.String(100))
    typeOfJob = db.Column(db.String(100))
    location = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    lastApplicationDate = db.Column(db.Date) #yyyy/mm/dd
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
    description = db.Column(db.String(300))
    applicationLocation = db.Column(db.String(200))
    status=db.Column(db.String(50),nullable=False,default="Saved",server_default="Saved")

    def __init__(
            self,
            company=None,
            typeOfJob=None,
            location=None,
            salary=None,
            lastApplicationDate=None,
            startDate=None,
            endDate=None,
            description=None,
            applicationLocation=None,
            user_id=None,
            jobTitle=None,
            status="Saved"
        ):
        self.user_id=user_id
        self.jobTitle=jobTitle
        self.company=company
        self.typeOfJob=typeOfJob
        self.location=location
        self.salary=salary
        self.lastApplicationDate=lastApplicationDate
        self.startDate=startDate
        self.endDate=endDate
        self.description=description
        self.applicationLocation=applicationLocation
        self.status=status

    @classmethod
    def find_by_id(cls, username):
        return cls.query.get(id)
    
    @classmethod
    def find_by_user_id(cls,user_id):
        return cls.query.filter_by(user_id=user_id)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def json(self):
        return {
            "user_id":self.user_id,
            "userJob_id":self._id,
            "jobTitle":self.jobTitle,
            "company":self.company,
            "typeOfJob":self.typeOfJob,
            "location":self.location,
            "salary":self.salary,
            "createdAt":self.createdAt.isoformat(),
            "lastModified":self.lastModified.isoformat(), 
            "lastApplicationDate": self.lastApplicationDate.strftime('%Y-%m-%d') if self.lastApplicationDate!=None else None,
            "startDate": self.startDate.strftime('%Y/%m/%d') if self.startDate!= None else None,
            "endDate":self.endDate.strftime('%Y/%m/%d') if self.endDate != None else None,
            "description":self.description,
            "applicationLocation":self.applicationLocation,
            "status":self.status,
        }
