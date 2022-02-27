'''
Date: 2022-02-27 13:29:25
LastEditors: GC
LastEditTime: 2022-02-27 22:14:39
FilePath: \REST API\Tutorial-2\main.py
'''
from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Wrap our app in an API and this just initializes the fact that we are using a RESTful API
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
db.create_all()

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes}"
        

# Make a new request parser object, it will automatically parse through the request that's being sent and make sure that it
#   fits the kind of guildlines that we are about to define here.
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video", required = True)
video_put_args.add_argument("views", type=int, help="Views of the video", required = True)


video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video")
video_update_args.add_argument("likes", type=int, help="Likes of the video")
video_update_args.add_argument("views", type=int, help="Views of the video")




# Define the fields from this video model that i wanna return 
resource_field = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}


class Video(Resource):

    # When we take this return value and serialize it using these fields
    @marshal_with(resource_field)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()

        if not result:
            abort(404, message="Could not find the video with that id...")
        return result

    @marshal_with(resource_field)
    def put(self, video_id):
        args = video_put_args.parse_args()

        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id is taken...")
            
        video = VideoModel(id=video_id, name=args["name"], views=args["views"], likes=args["likes"])
        db.session.add(video)
        db.session.commit()

        return video, 201

    @marshal_with(resource_field)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        
        if not result:
            abort(404, message="Video doesnot exist, can not update it.")

        if args["name"]:
            result.name = args["name"]
        
        if args["views"]:
            result.views = args["views"]
        
        if args["likes"]:
            result.likes = args["likes"]
 
        db.session.commit()

        return result



    # def delete(self, video_id):
    #     abort_if_video_exists(video_id)
    #     del videos[video_id]

    #     return "", 204


# Register the class as a resource
api.add_resource(Video, "/video/<int:video_id>")




        


if __name__ == "__main__":
    app.run(debug=True)

