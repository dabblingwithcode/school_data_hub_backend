from datetime import datetime
from apiflask import APIBlueprint, abort
from flask import jsonify
from app import db
from auth_middleware import token_required
from models.schoolday import Schoolday, MissedClass
from schemas.missed_class_schemas import *
from schemas.pupil_schemas import *
from models.pupil import Pupil

missed_class_api = APIBlueprint('missed_class_api', __name__, url_prefix='/api/missed_classes')

#- POST MISSED CLASS 
#####################
@missed_class_api.route('/new', methods=['POST'])
@missed_class_api.input(missed_class_in_schema, example={
  "contacted": None,
  "excused": False,
  "minutes_late": None,
  "missed_day": "2023-11-20",
  "missed_pupil_id": 1234,
  "missed_type": "missed",
  "returned": None,
  "returned_at": None,
  "written_excuse": None
})
@missed_class_api.output(pupil_schema)
@missed_class_api.doc(security='ApiKeyAuth', tags=['Missed Classes'], summary='Post a missed class')
@token_required
def add_missed_class(current_user, json_data):
    data = json_data
    this_missed_pupil_id = data['missed_pupil_id']
    missed_pupil = db.session.query(Pupil).filter(Pupil.internal_id == this_missed_pupil_id ).first()
    if missed_pupil == None:
       abort(404, message="Schüler/Schülerin nicht im System!")       
    missed_day = data['missed_day']
    # stringtodatetime = datetime.strptime(missed_day, '%Y-%m-%d').date()
    #this_schoolday = db.session.query(Schoolday).filter(Schoolday.schoolday == stringtodatetime ).first()
    this_schoolday = db.session.query(Schoolday).filter(Schoolday.schoolday == missed_day ).first()
    if this_schoolday == None:
        abort(404, message="Dieser Schultag existiert nicht!")
    this_missed_day_id = this_schoolday.schoolday
    missed_class_exists = db.session.query(MissedClass).filter(MissedClass.missed_day_id == this_missed_day_id, MissedClass.missed_pupil_id == this_missed_pupil_id ).first()
    if missed_class_exists != None :
        abort(403, message="This missed class exists already - please update instead!")
    else:    
        missed_type = data['missed_type']
        excused = data['excused']
        contacted = data['contacted']
        returned = data['returned']
        returned_at = data['returned_at']
        minutes_late = data['minutes_late']
        written_excuse = data['written_excuse']
        created_by = current_user.name
        modified_by = None
        new_missed_class = MissedClass(this_missed_pupil_id, this_missed_day_id, missed_type, excused,
                                      contacted, returned, written_excuse, minutes_late, returned_at,
                                      created_by, modified_by)
        db.session.add(new_missed_class)
        db.session.commit()       
        return missed_pupil 

#- POST LIST OF MISSED CLASSES
##############################
@missed_class_api.route('/list', methods=['POST'])
@missed_class_api.input(missed_classes_in_schema, example=[{
  "contacted": None,
  "excused": False,
  "minutes_late": None,
  "missed_day": "2023-11-20",
  "missed_pupil_id": 1234,
  "missed_type": "missed",
  "returned": None,
  "returned_at": None,
  "written_excuse": None
},
{
  "contacted": None,
  "excused": False,
  "minutes_late": None,
  "missed_day": "2023-11-21",
  "missed_pupil_id": 1234,
  "missed_type": "missed",
  "returned": None,
  "returned_at": None,
  "written_excuse": None
}])
@missed_class_api.output(pupil_schema, 200)
@missed_class_api.doc(security='ApiKeyAuth', tags=['Missed Classes'], summary='Post a list of missed classes')
@token_required
def add_missed_class_list(current_user, json_data):
    missed_class_list = json_data
    commited_missed_classes = []
    for entry in missed_class_list:
        this_missed_pupil_id = entry['missed_pupil_id']
        missed_pupil = db.session.query(Pupil).filter(Pupil.internal_id == this_missed_pupil_id ).first()
        if missed_pupil == None:
            abort(404, message='Schüler/Schülerin nicht im System!')     
        this_missed_day = entry['missed_day']
        # stringtodatetime = datetime.strptime(this_missed_day, '%Y-%m-%d').date()
        # this_schoolday = db.session.query(Schoolday).filter(Schoolday.schoolday == stringtodatetime ).first()
        this_schoolday = db.session.query(Schoolday).filter(Schoolday.schoolday == this_missed_day ).first()
        
        if this_schoolday == None:
            abort(404, message='Dieser Schultag existiert nicht!')
        
        missed_class = db.session.query(MissedClass).filter(MissedClass.missed_day_id == this_schoolday.schoolday, MissedClass.missed_pupil_id == missed_pupil.internal_id ).first()
        if missed_class != None:
                for key in entry:
                    match key:
                        case 'missed_type':
                            missed_class.missed_type = entry[key]
                        case 'excused':
                            missed_class.excused = entry[key]
                        case 'contacted':
                            missed_class.contacted = entry[key]
                        case 'returned':
                            missed_class.returned = entry[key]
                        case 'written_excuse':
                            missed_class.written_excuse = entry[key]
                        case 'minutes_late':
                            missed_class.minutes_late = entry[key]
                        case 'returned_at':
                            missed_class.returned_at = entry[key]
                        case 'modified_by':
                            missed_class.modified_by = entry[key]
                commited_missed_classes.append(missed_class)  
        else:    
            missed_type = entry['missed_type']
            excused = entry['excused']
            contacted = entry['contacted']
            returned = False
            returned_at = None
            minutes_late = None
            written_excuse = None
            created_by = current_user.name
            modified_by = None
            new_missed_class = MissedClass(this_missed_pupil_id, this_missed_day, missed_type, excused,
                                        contacted, returned, written_excuse, minutes_late, returned_at,
                                        created_by, modified_by)
            db.session.add(new_missed_class)
            commited_missed_classes.append(new_missed_class) 
    db.session.commit()
    # result = missed_classes_schema.dump(commited_missed_classes)
    
    return missed_pupil

#- GET ALL MISSED CLASSES
#########################
@missed_class_api.route('/all', methods=['GET'])
@missed_class_api.output(missed_classes_schema, 200)
@missed_class_api.doc(security='ApiKeyAuth', tags=['Missed Classes'], summary='Get all missed classes')
@token_required
def get_missed_classes(current_user):
    all_missed_classes = MissedClass.query.all()
    if all_missed_classes == []:
        abort(404, message="There are no missed classes!")   
    #result = missed_classes_schema.dump(all_missed_classes)
    return all_missed_classes

#- GET MISSED CLASSES ON A SCHOOL DAY
#####################################
@missed_class_api.route('/schoolday/<date>', methods=['GET'])
@missed_class_api.output(missed_classes_schema, 200)
@missed_class_api.doc(security='ApiKeyAuth', tags=['Missed Classes'], summary='Get missed classes on a school day')
@token_required
def get_missed_classes_on_schoolday(current_user, date):
    this_schoolday = db.session.query(Schoolday).filter(Schoolday.schoolday == date ).first()
    if this_schoolday == None:
        abort(404, message="This school day does not exist!")
    all_missed_classes = db.session.query(MissedClass).filter(MissedClass.missed_day_id == this_schoolday.schoolday).all()
    if all_missed_classes == []:
        abort(404, message="There are no missed classes on this school day!")
    return all_missed_classes

#- GET ONE MISSED CLASS
#######################
@missed_class_api.route('/<missed_class_id>', methods=['GET'])
@missed_class_api.doc(security='ApiKeyAuth', tags=['Missed Classes'], summary='Get ONE missed class by id', deprecated=True)
@token_required
def get_missed_class(current_user, missed_class_id):
    this_missed_class = db.session.query(MissedClass).get(missed_class_id)
    if this_missed_class == None:
        return jsonify({'error': 'This missed class does not exist!'})
    return missed_class_schema.jsonify(this_missed_class)

#- PATCH MISSED CLASS
#####################
@missed_class_api.route('/<pupil_id>/<date>', methods=['PATCH'])
@missed_class_api.input(missed_class_in_schema)
@missed_class_api.output(pupil_schema, 200)
@missed_class_api.doc(security='ApiKeyAuth', tags=['Missed Classes'], summary='Patch a missed class by pupil_id and date')
@token_required
def update_missed_class(current_user, pupil_id, date, json_data):
    missed_pupil = db.session.query(Pupil).filter(Pupil.internal_id == pupil_id ).first()
    date_as_datetime = datetime.strptime(date, '%Y-%m-%d').date()
    missed_schoolday = db.session.query(Schoolday).filter(Schoolday.schoolday == date_as_datetime ).first()
    if missed_schoolday == None:
        abort(401, message="This schoolday does not exist!")
        #return jsonify({'error': 'This schoolday does not exist!'}), 401
    missed_class = db.session.query(MissedClass).filter(MissedClass.missed_day_id == missed_schoolday.schoolday, MissedClass.missed_pupil_id == pupil_id ).first()  
    if missed_class == None:
        abort(401, message="This missed class does not exist!")
        #return jsonify({'error': 'This missed class does not exist!'}), 401
    data = json_data # request.get_json()
    for key in data:
        match key:
            case 'missed_type':
                missed_class.missed_type = data[key]
                print('sent value: ' + data[key])
            case 'excused':
                missed_class.excused = data[key]
                print('sent value: ' + str(data[key]))
            case 'contacted':
                missed_class.contacted = data[key]
            case 'returned':
                missed_class.returned = data[key]
                print('sent return value: ' + str(data[key]))
            case 'written_excuse':
                missed_class.written_excuse = data[key]
            case 'minutes_late':
                missed_class.minutes_late = data[key]
            case 'returned_at':
                returned_time = data[key]
                missed_class.returned_at = returned_time
            case 'modified_by':
                missed_class.modified_by = data[key]
    db.session.commit()
    return missed_pupil

#- DELETE MISSED CLASS WITH DATE
################################
@missed_class_api.route('/<pupil_id>/<schoolday>', methods=['DELETE'])
@missed_class_api.output(pupil_schema, 200)
@missed_class_api.doc(security='ApiKeyAuth', tags=['Missed Classes'], summary='Delete a missed class by pupil_id and date')
@token_required
def delete_missed_class_with_date(current_user, pupil_id, schoolday):
    missed_pupil = db.session.query(Pupil).filter(Pupil.internal_id == pupil_id ).first()
    if missed_pupil == None:
       return jsonify({'message': 'Schüler/Schülerin nicht im System!'}), 404 
    missed_pupil_id = pupil_id
    stringtodatetime = datetime.strptime(schoolday, '%Y-%m-%d').date()
    schoolday = db.session.query(Schoolday).filter(Schoolday.schoolday == stringtodatetime ).first()
    thismissed_day_id = schoolday.schoolday
    missed_schoolday = db.session.query(MissedClass).filter(MissedClass.missed_day_id == thismissed_day_id ).first()
    if missed_schoolday == None:
        abort(401, message="Keine Fehlzeiten an diesem Tag!")
    missed_class = db.session.query(MissedClass).filter(MissedClass.missed_day_id == thismissed_day_id, MissedClass.missed_pupil_id == missed_pupil_id ).first() 
    if missed_class == None:
        abort(401, message="Diese Fehlzeit existiert nicht!")
    db.session.delete(missed_class)
    db.session.commit()
    return missed_pupil