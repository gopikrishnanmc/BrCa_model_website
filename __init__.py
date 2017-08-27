from flask import Flask, render_template, request
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

sparql = SPARQLWrapper("http://localhost:7200/repositories/Openclinical")
ns = """
        PREFIX : <http://www.nottingham.ac.uk/ontologies/2016/10/BrCa_family#>
        PREFIX BrCa: <http://www.nottingham.ac.uk/ontologies/2016/10/BrCa_family#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
"""


@app.route('/')
def homepage():
    try:
        name = "Python"
        example_list = ["2.5", "2.6", "2.7", "3.1", "3.2", "3.1"]
        return render_template('index.html', name=name, example_list=example_list)
    except Exception as e:
        return (str(e))


@app.route('/patient-demo/', methods=['POST'])
def patientdemo():
    queryString1 = ns + """
    SELECT ?Patient ?Sex ?DateOfBirth
    WHERE
    {?Patient :Date_Of_Birth ?DateOfBirth.
     ?Patient :hasSex ?Sex
     FILTER (?Patient = :1004)
    }
    """
    patientID = ":" + request.form['patientID1']
    queryString = queryString1.replace(":1004", patientID)
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
        return render_template('patientdemo.html', results=results["results"]["bindings"], patientID=patientID)


@app.route('/patient-history/', methods=['POST'])
def patienthistory():
    queryString2 = ns + """
SELECT ?Patient ?FamilyHistoryOfCancer ?Personal_history_of_breast_cancer
WHERE
{
?Patient :hasFamilyHistoryOfCancer ?FamilyHistoryOfCancer.
?Patient :hasBreastCancerStatus ?Personal_history_of_breast_cancer.
FILTER (?Patient = :1004)
}
    """
    patientID = ":" + str(request.form['patientID2'])
    print(patientID)
    queryString = queryString2.replace(":1004", patientID)
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
        return render_template('patienthistory.html', results=results["results"]["bindings"], patientID=patientID)


@app.route('/relative-cancer/', methods=['POST'])
def relativecancer():
    queryString4 = ns + """
    SELECT ?Patient ?Jewish_ancestry
    WHERE
    {
    ?Patient :hasBreastCaRiskFactorsJewishInheritance ?Jewish_ancestry.
    FILTER (?Patient = :1004)
    }
            """
    patientID = ":" + str(request.form['patientID4'])
    print(patientID)
    queryString = queryString4.replace(":1004", patientID)
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
        return render_template('otherfamily.html', results=results["results"]["bindings"], patientID=patientID)


@app.route('/other-family/', methods=['POST'])
def otherfamily():
    queryString3 = ns + """
SELECT ?Patient ?Jewish_ancestry
WHERE
{
?Patient :hasBreastCaRiskFactorsJewishInheritance ?Jewish_ancestry.
FILTER (?Patient = :1004)
}
        """
    patientID = ":" + str(request.form['patientID3'])
    print(patientID)
    queryString = queryString3.replace(":1004", patientID)
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
        return render_template('otherfamily.html', results=results["results"]["bindings"], patientID=patientID)


@app.errorhandler(404)
def four_of_four(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run()
