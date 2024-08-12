from flask_smorest import Blueprint, abort
from flask.views import MethodView
from firebase_admin import auth
from firebase_set import get_db
from schemas.schemas import UserSchema, EmailSchema

blp = Blueprint("api", __name__, url_prefix="/api", description="API operations")

# Firebase DB 참조 설정
ref = get_db()

@blp.route('/main')
class Main(MethodView):
    @blp.response(200, description="Welcome message")
    def get(self):
        return {"message": "Welcome to the Home Page"}, 200


@blp.route('/documents')
class Documents(MethodView):
    @blp.response(200, description="Get all documents")
    def get(self):
        documents = ref.get()
        return documents if documents else {'message': 'No documents found'}, 200


@blp.route('/items/<item_id>')
class ItemResource(MethodView):
    @blp.response(200, description="Get item details by ID")
    def get(self, item_id):
        """Get item details by ID"""
        item = ref.child(item_id).get()
        if not item:
            abort(404, message="Item not found")
        return item, 200
    
    @blp.arguments(UserSchema)  # UserSchema를 통해 PUT 요청 본문 데이터 유효성 검사
    @blp.response(200, description="Update an existing item")
    def put(self, data, item_id):
        """Update an existing item"""
        ref.child(item_id).update(data)
        return {"message": "Item updated"}, 200

    @blp.response(204, description="Delete an item by ID")
    def delete(self, item_id):
        """Delete an item by ID"""
        ref.child(item_id).delete()
        return {"message": "Item deleted"}, 204


@blp.route('/signup/register')
class RegisterUser(MethodView):
    @blp.arguments(UserSchema)  # UserSchema를 통해 POST 요청 본문 데이터 유효성 검사
    @blp.response(201, description="User registered")
    def post(self, data):
        """Handle user registration"""
        try:
            user = auth.create_user(
                email=data['email'],
                password=data['password'],
                display_name=data.get('display_name')
            )
            return {"uid": user.uid}, 201
        except Exception as e:
            abort(400, message=str(e))


@blp.route('/resetpw')
class ResetPassword(MethodView):
    @blp.arguments(EmailSchema)  # EmailSchema를 통해 POST 요청 본문 데이터 유효성 검사
    @blp.response(200, description="Password reset link sent")
    def post(self, data):
        """Send password reset link"""
        email = data['email']
        try:
            link = auth.generate_password_reset_link(email)
            return {"reset_link": link}, 200
        except Exception as e:
            abort(400, message=str(e))
