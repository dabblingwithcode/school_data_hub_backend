from apiflask import APIFlask
from apiflask.ui_templates import redoc_template, elements_template, rapidoc_template
from flask import render_template_string
from dotenv import load_dotenv
import os

from models.schoolday import db
from api_endpoints.users_api import user_api
from api_endpoints.pupils_api import pupil_api
from api_endpoints.workbooks_api import workbook_api
from api_endpoints.pupil_workbooks_api import pupil_workbook_api
from api_endpoints.books_api import book_api
from api_endpoints.pupil_books_api import pupil_book_api
from api_endpoints.categories_api import goal_category_api
from api_endpoints.competences_api import competence_api
from api_endpoints.competence_goals_api import competence_goal_api
from api_endpoints.competence_checks_api import competence_check_api
from api_endpoints.competence_reports_api import competence_report_api
from api_endpoints.schooldays_api import schoolday_api
from api_endpoints.import_from_file_api import import_file_api
from api_endpoints.admonitions_api import admonition_api
from api_endpoints.category_statuses_api import category_status_api
from api_endpoints.school_lists_api import school_list_api
from api_endpoints.pupil_lists_api import pupil_list_api
from api_endpoints.missed_classes_api import missed_class_api
from api_endpoints.authorizations_api import authorization_api
from api_endpoints.pupil_authorizations_api import pupil_authorization_api
from api_endpoints.school_semester_api import school_semester_api
from api_endpoints.category_goals_api import category_goals_api

#- INIT APP

app = APIFlask(__name__)

#- BLUEPRINTS

app.register_blueprint(user_api, url_prefix='/api/users')
app.register_blueprint(pupil_api, url_prefix='/api/pupils')
app.register_blueprint(workbook_api, url_prefix='/api/workbooks')
app.register_blueprint(pupil_workbook_api, url_prefix='/api/pupil_workbooks')
app.register_blueprint(book_api, url_prefix='/api/books')
app.register_blueprint(pupil_book_api, url_prefix='/api/pupil_books')
app.register_blueprint(goal_category_api, url_prefix='/api/goal_categories')
app.register_blueprint(competence_api, url_prefix='/api/competences')
app.register_blueprint(competence_goal_api, url_prefix='/api/competence_goals')
app.register_blueprint(competence_check_api, url_prefix='/api/competence_checks')
app.register_blueprint(competence_report_api, url_prefix='/api/competence_reports')
app.register_blueprint(schoolday_api, url_prefix='/api/schooldays')
app.register_blueprint(import_file_api, url_prefix='/api/import')
app.register_blueprint(admonition_api, url_prefix='/api/admonitions')
app.register_blueprint(category_status_api, url_prefix='/api/category/statuses')
app.register_blueprint(school_list_api, url_prefix='/api/school_lists')
app.register_blueprint(pupil_list_api, url_prefix='/api/pupil_lists')
app.register_blueprint(missed_class_api, url_prefix='/api/missed_classes')
app.register_blueprint(authorization_api, url_prefix='/api/authorizations')
app.register_blueprint(pupil_authorization_api, url_prefix='/api/pupil_authorizations')
app.register_blueprint(school_semester_api, url_prefix='/api/school_semesters')
app.register_blueprint(category_goals_api, url_prefix='/api/category_goals')

#- APP CONFIG

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024 
app.config['UPLOAD_FOLDER'] = './media_upload'
ALLOWED_EXTENSIONS = ['jpg', 'jpeg']
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower in ALLOWED_EXTENSIONS

#- OPEN API APP CONFIG

app.title = 'School Data Hub'
app.config['DESCRIPTION'] = 'A backend tool for managing complex lists out of the pocket.'
app.config['DOCS_FAVICON'] = 'https://hermannschule.de/apps/favicon-32x32.png'
app.security_schemes = {
    'ApiKeyAuth' : {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-access-token'
    },
    'basicAuth': {
        'type': 'http',
        'scheme': 'basic'
    }
}
app.config['TAGS'] = [
    {'name': 'Auth', 'description': 'Basic Auth'},
    {'name': 'User', 'description': 'User endpoints - tested'},
    {'name': 'File Imports', 'description': 'File imports - tested'},
    {'name': 'Pupil', 'description': 'Pupil endpoints - tested'},
    {'name': 'Schooldays', 'description': 'Schoolday endpoints - tested'},
    {'name': 'Missed Classes', 'description': 'MissedClass endpoints -tested'},
    {'name': 'Admonitions', 'description': 'Admonition endpoints - tested'},
    {'name': 'Competence', 'description': 'Competence endpoints - tested'},
    {'name': 'Competence Checks', 'description': 'Competence check endpoints - tested'},
    {'name': 'Competence Goals', 'description': 'Competence goal endpoints - tested'},
    {'name': 'Competence Report', 'description': 'Competence report for a school semester'},
    {'name': 'Goal Categories', 'description': 'Goal category endpoints - tested'},
    {'name': 'Category Statuses', 'description': 'Category status endpoints - tested'},
    {'name': 'Goals', 'description': 'Goal endpoints - tested'},
    {'name': 'Goal Checks', 'description': 'Goal check endpoints - tested'},
    {'name': 'Authorizations', 'description': 'Authorization endpoints - tested'},
    {'name': 'Pupil Authorizations', 'description': 'Pupil authorization endpoints - tested'},
    {'name': 'School Lists', 'description': 'School list endpoints - tested'},
    {'name': 'Pupil Lists', 'description': 'Pupil list endpoints - tested'},
    {'name': 'School Semester', 'description': 'School semester endpoints'},
    {'name': 'Workbooks', 'description': 'Workbook catalogue endpoints'},
    {'name': 'Pupil Workbooks', 'description': 'Pupil workbooks endpoints'},
    {'name': 'Books', 'description': 'Book catalogue endpoints'},
    {'name': 'Pupil Books', 'description': 'Pupil books endpoints'},
]
app.config['CONTACT'] = {
    'name': 'API Support',
    'url': 'https://hermannschule.de/de',
    'email': 'admin@hermannschule.de'
}
app.config['SERVERS'] = [
       {
        'name': 'Production Server',
        'url': 'https://datahub.hermannschule.de'
    },
           {
        'name': 'Test Server',
        'url': 'https://testhub.hermannschule.de'
    },
    {
        'name': 'Development Server',
        'url': 'http://127.0.0.1:5000/'
    },
]

#- SWAGGER CONFIG

app.config['SWAGGER_UI_CONFIG'] = {
    'docExpansion': 'none',
    'persistAuthorization': True,
    'filter': True,
    'tryItOutEnabled': True,
    #'operationsSorter': 'alpha',	
}
# app.config['TERMS_OF_SERVICE'] = 'http://hermannschule.de'

#- RAPIDOC CONFIG

app.config['RAPIDOC_THEME'] = 'dark'
app.config['RAPIDOC_CONFIG'] = {
    #'update-route': False,
    'persist-auth': True,
    'layout': 'column',
    'render-style': 'read',
    'sort-endpoints-by': 'method',
    'heading-text': 'School Data Hub',
    'show-method-in-nav-bar': 'as-colored-block',
    'font-size': 'largest',
    'bg-color': '#111',
     'nav-bg-color': "#222",
    'primary-color':"#615ba7",
    'response-area-height': '600px'
}

#- OPEN API DOC ROUTES

@app.route('/redoc')
def my_redoc():
    return render_template_string(redoc_template, title='School Data Hub', version='1.0')
@app.route('/elements')
def my_elements():
    return render_template_string(elements_template, title='School Data Hub', version='1.0')
@app.route('/rapidoc')
def my_rapidoc():
    return render_template_string(rapidoc_template, title='School Data Hub', version='1.0')

#- RUN SERVER

# db.init_app(app) because of https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045
db.init_app(app)
with app.app_context():
    #db.drop_all()
    db.create_all()
if __name__ == '__main__':
    app.run(host='192.168.178.107')
    #app.run(host='0.0.0.0')
