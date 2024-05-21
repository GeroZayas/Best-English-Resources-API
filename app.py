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


class CategoryResource(Resource):
    def get(self, category):
        filtered_resources = df[df["category"].str.lower() == category.lower()].to_dict(
            orient="records"
        )
        if filtered_resources:
            return jsonify(filtered_resources)
        return {"message": "No resources found for this category"}, 404


# Route for the index page
@app.route("/")
def index():
    categories = [
        "top",
        "CAE",
        "collocations",
        "dictionary",
        "FCE",
        "grammar",
        "listening",
        "phrasal verbs",
        "pronunciation",
        "reading",
        "speaking",
        "general",
        "vocabulary",
        "writing",
        "young learners and kids",
    ]
    return render_template("index.html", categories=categories)


# Add resource routes
api.add_resource(ResourceList, "/resources")
api.add_resource(ResourceDetail, "/resources/<int:resource_id>")
api.add_resource(RandomResource, "/resources/random")
api.add_resource(CategoryResource, "/resources/<string:category>")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
