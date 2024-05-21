from flask import Flask, jsonify, render_template
from flask_restful import Api, Resource
import pandas as pd
import random

# Initialize Flask app and API
app = Flask(__name__)
api = Api(app)

# Load CSV data
df = pd.read_csv("./resources/all_resources.csv")


# Define Resource class
class ResourceList(Resource):
    def get(self):
        resources = df.to_dict(orient="records")
        return jsonify(resources)


class ResourceDetail(Resource):
    def get(self, resource_id):
        resource = df[df["id"] == resource_id].to_dict(orient="records")
        if resource:
            return jsonify(resource[0])
        return {"message": "Resource not found"}, 404


class RandomResource(Resource):
    def get(self):
        random_resource = df.sample(n=1).to_dict(orient="records")[0]
        return jsonify(random_resource)


# Route for the index page
@app.route("/")
def index():
    return render_template("index.html")


# Add resource routes
api.add_resource(ResourceList, "/resources")
api.add_resource(ResourceDetail, "/resources/<int:resource_id>")
api.add_resource(RandomResource, "/resources/random")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
