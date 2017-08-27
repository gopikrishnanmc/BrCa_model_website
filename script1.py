from flask import Flask, render_template, request
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)
sparql = SPARQLWrapper("http://localhost:7200/repositories/Openclinical")

ns = """
PREFIX : <http://www.nottingham.ac.uk/ontologies/2016/10/BrCa_family#>
PREFIX BrCa: <http://www.nottingham.ac.uk/ontologies/2016/10/BrCa_family#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX BrCa_family: <http://www.nottingham.ac.uk/ontologies/2016/10/BrCa_family/Family#>
"""

queryString1 = ns + """
SELECT ?Relative ?Sex ?FamilyID1 ?Mother ?Father ?AgeAtDeath ?RelativeBreastCancer
WHERE{

?Patient rdf:type :Patient.
?Patient :hasFamilyID ?FamilyID1.
?Relative :hasFamilyID ?FamilyID2.
?Relative :hasSex ?Sex.
?Relative :hasMother ?Mother.
?Relative :hasFather ?Father.
?Relative :Age_At_Death ?AgeAtDeath.
?Relative :hasBreastCancerStatus ?RelativeBreastCancer.

FILTER (?Patient = :1004 )
FILTER (?FamilyID1 = ?FamilyID2)
}
ORDER BY ?Relative
        """

queryString2 = ns+"""SELECT ?Patient ?DateOfBirth
WHERE
{?Patient :Date_Of_Birth ?DateOfBirth
 FILTER (?Patient = :1004)
}"""

@app.route('/')
def patient_data():
    return render_template('patient_enquiry.html')


@app.route('/data', methods=['POST'])
def process(queryString=queryString1):
    patientID = ":" + request.form['patientID']
    queryString = queryString.replace(":1004", patientID)
    sparql.setQuery(queryString)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        requestGood = True
    except Exception as e:
        results = str(e)
        requestGood = False

    if requestGood == False:
        return render_template('error.html')
    elif (len(results['results']['bindings']) == 0):
        return render_template('no_results.html')
    elif requestGood == True:
        return render_template('login.html', results=results["results"]["bindings"], patientID=patientID)




#if __name__ == "__main__":
    #app.run(debug=True)
