from flask import Flask, render_template, request
from SPARQLWrapper import SPARQLWrapper, JSON

# app = Flask(__name__)

ns = """
        PREFIX : <http://www.nottingham.ac.uk/ontologies/2016/10/BrCa_family#>
        PREFIX BrCa: <http://www.nottingham.ac.uk/ontologies/2016/10/BrCa_family#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
"""


class FamilyData:
    sparql_select = SPARQLWrapper("http://localhost:7200/repositories/Openclinical")

    def __init__(self, query):
        pID = "376"
        patientID = ":" + request.form['patientID']
        query1 = query.replace(":1004", patientID)
        self.query = query1

    def view_patient_demographics(self):
        self.sparql_select.setQuery(ns + self.query)
        self.sparql_select.setReturnFormat(JSON)
        results = self.sparql_select.query().convert()

        for result in results["results"]["bindings"]:
            PatientURI = result["Patient"]["value"]
            Psplit = PatientURI.split("#")
            PatientID = Psplit[1]

            DateOfBirth = result["DateOfBirth"]["value"]
            return (PatientID, DateOfBirth)


q1 = """SELECT ?Patient ?DateOfBirth
        WHERE
        {
        ?Patient :Date_Of_Birth ?DateOfBirth
        FILTER (?Patient = :1004)
    }"""

viewPD = FamilyData(q1)
v = viewPD.view_patient_demographics()
print(v)
