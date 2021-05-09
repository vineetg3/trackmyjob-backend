from database import db
from .users import UserModel
from datetime import datetime
from dateTimeHelper import get_current_IST_dt
from sqlalchemy import or_

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
    
    @classmethod
    def run_query(cls,queryP,user_id):
        print(queryP)
        entitiesVisible=queryP['entitiesVisible']
        searchTerm=queryP['searchTerm']
        sortingEntity=queryP['sortingEntity']
        sortingOrder = queryP['sortingOrder']
        qr = db.session.query(cls).filter(cls.user_id==user_id,cls.status.in_(entitiesVisible))
        #search query is only compared with db.String
        if(len(searchTerm)!=0):
            qr = qr.filter(or_(
                cls.jobTitle.like(f'%{searchTerm}%'),
                cls.company.like(f'%{searchTerm}%'),
                cls.typeOfJob.like(f'%{searchTerm}%'),
                cls.location.like(f'%{searchTerm}%'),
                cls.description.like(f'%{searchTerm}%'),
                cls.applicationLocation.like(f'%{searchTerm}%'),
            ))
        switcher = {
            "Company":cls.company,
            "Salary":cls.salary,
            "Date of Last Application":cls.lastApplicationDate,
            "Start-Date":cls.startDate,
            "End-Date":cls.endDate,
            "Last Modified":cls.lastModified,
            "Created Date":cls.createdAt,
            "Job Title":cls.jobTitle
            }
        if(sortingOrder=="Asc"):
            qr = qr.order_by(switcher[sortingEntity].asc())
        else:
            qr = qr.order_by(switcher[sortingEntity].desc())
        return qr
        
        


    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def json(self):
        dateFormat="%a %b %d %Y" #Wed Dec 30 2020
        dateTimeFormat="%a %b %d %Y %I:%M %p"
        return { 
            "user_id":self.user_id,
            "userJob_id":self._id,
            "jobTitle":self.jobTitle,
            "company":self.company,
            "typeOfJob":self.typeOfJob,
            "location":self.location,
            "salary":self.salary,
            "createdAt":self.createdAt.strftime(dateTimeFormat),
            "lastModified":self.lastModified.strftime(dateTimeFormat), 
            "lastApplicationDate": self.lastApplicationDate.strftime(dateFormat) if self.lastApplicationDate!=None else None,
            "startDate": self.startDate.strftime(dateFormat) if self.startDate!= None else None,
            "endDate":self.endDate.strftime(dateFormat) if self.endDate != None else None,
            "description":self.description,
            "applicationLocation":self.applicationLocation,
            "status":self.status,
        }
