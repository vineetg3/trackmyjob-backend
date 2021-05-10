from flask import request
from flask_restful import Resource, reqparse
from models.userJobs import UserJobsModel
from models.tokenBlacklist import TokenBlocklist
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,get_jwt
from datetime import datetime
from pytz import timezone
from .utilities import printResponse,convertToDate

class UserJobPost(Resource):
    parser = reqparse.RequestParser() 
    parser.add_argument('user_id',required=False)
    parser.add_argument('jobTitle',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('company',required=False)
    parser.add_argument('typeOfJob',required=False)
    parser.add_argument('location',required=False)
    parser.add_argument('salary',required=False)
    parser.add_argument('lastApplicationDate',required=False)
    parser.add_argument('startDate',required=False)
    parser.add_argument('endDate',required=False)
    parser.add_argument('description',required=False)
    parser.add_argument('applicationLocation',required=False)
    parser.add_argument('status',required=True)


    @jwt_required()
    def post(self):
        data=UserJobPost.parser.parse_args()
        user_id=get_jwt_identity() 
        data['user_id']=user_id
        data['startDate']=convertToDate(date=data['startDate'])
        data['endDate']=convertToDate(date=data['endDate'])
        data['lastApplicationDate']=convertToDate(date=data['lastApplicationDate'])
        data['createdAt']=datetime.now()
        data['lastModified']=datetime.now()
        userjob=UserJobsModel(**data)
        userjob.save_to_db()
        return printResponse({"message":"user job created","userJob":userjob.json()},201)

class UserJobById(Resource):
    parser = reqparse.RequestParser() 
    parser.add_argument('user_id',required=False)
    parser.add_argument('jobTitle',required=False)
    parser.add_argument('company',required=False)
    parser.add_argument('typeOfJob',required=False)
    parser.add_argument('location',required=False)
    parser.add_argument('salary',required=False)
    parser.add_argument('lastApplicationDate',required=False)
    parser.add_argument('startDate',required=False)
    parser.add_argument('endDate',required=False)
    parser.add_argument('description',required=False)
    parser.add_argument('applicationLocation',required=False)
    parser.add_argument('status',required=True)

    @jwt_required()
    def get(self,pk):
        user_id=get_jwt_identity() 
        userjob = UserJobsModel.query.filter_by(user_id=user_id).filter_by(_id=pk).first()
        return printResponse(userjob.json())
    #UPDATE FUNCTIONALITY
    @jwt_required()
    def put(self,pk):
        updatedData=UserJobById.parser.parse_args()
        user_id=get_jwt_identity()
        updatedData['user_id']=user_id
        userjob= UserJobsModel.query.filter_by(user_id=user_id).filter_by(_id=pk).first()
        userjob.lastModified=datetime.now()
        for key, value in updatedData.items():
            setattr(userjob, key, value)
        userjob.save_to_db()
        return printResponse({"message":"user job modified","userJob":userjob.json()},200)

    @jwt_required()
    def delete(self,pk):
        user_id=get_jwt_identity()
        userjob= UserJobsModel.query.filter_by(user_id=user_id).filter_by(_id=pk).first()
        userjob.delete_from_db()
        return printResponse({"msg":"userjob deleted","userJob_id":pk},200)

class UserJobList(Resource):
    parser = reqparse.RequestParser() 
    parser.add_argument('searchTerm',
                        type=str,
                        required=False,
                       )
    parser.add_argument('sortingEntity',
                        type=str,
                        required=False,
                       )
    parser.add_argument('sortingOrder',
                        type=str,
                        required=False,
                       )
    parser.add_argument('entitiesVisible',
                        type=str,
                        action='append', 
                        required=False,
                       )
                       
    @jwt_required()
    def post(self):
        print(request.form.get('searchTerm')) 
        queryP=UserJobList.parser.parse_args()
        user_id=get_jwt_identity() 
        userJobs = UserJobsModel.run_query(queryP,user_id)
        return printResponse({"userJobs":[job.json() for job in userJobs]},200)