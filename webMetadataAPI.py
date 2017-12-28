from flask import Flask
from flask import request
import json
import sys
import localMetadataAPI
app = Flask(__name__)

metadata = localMetadataAPI.Metadata()

@app.route("/")
def landing():
	spec = "Metadata API Specs<br/>"
	select = "Select Metadata (fieldName optional):<br/> /select?varName=x&fieldName=y<br/><br/>"
	filte = "Filter Metadata (provide any fields as filters):<br/> /filter?field1=x&field2=y&field3=z<br/><br/>"
	search = "SearchMetadata (provide both a query string and a search field):<br/> /search?query=x&fieldName=y<br/><br/>"
	return spec + select + filte + search

@app.route("/select")
def selectMetadata():
	global metadata

	varName = request.args.get('varName')
	if varName is None:
		return('Error: please enter a varName')
	fieldName = request.args.get('fieldName', default=None)
	return app.response_class(metadata.selectMetadata(varName, fieldName), content_type='application/json')

@app.route("/filter")
def filterMetadata():
	global metadata
	filters = {}
	for query in request.args:
		filters[query] = request.args.get(query)
	if filters == {}:
		return app.response_class(metadata.filterMetadata(), content_type='application/json')
	else:
		return app.response_class(metadata.filterMetadata(filters), content_type='application/json')