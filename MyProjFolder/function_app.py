import azure.functions as func
import datetime
import json
import logging
import duckdb

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    cognome = req.params.get('cognome')
    
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        if cognome:
            return func.HttpResponse(f"Hello, {name} {cognome}. This HTTP triggered function executed successfully.")
        else:
            return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "Quack quack motherquackeeeeeeeeeeeeers.",
             status_code=200
        )


@app.route(route="PubChem", auth_level=func.AuthLevel.ANONYMOUS)
def PubChem(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    substance = req.params.get('substance')

    if substance:
        #return func.HttpResponse(f"Results for {substance}: ")

        conn = duckdb.connect(':memory:')
        conn.execute("CREATE TABLE local_substances AS SELECT * FROM read_csv('HSDB.csv', header=1)")         
        query = "SELECT Measure, Toxicity FROM local_substances WHERE Name = ?"
        query_res = conn.execute(query, [substance]).df()
        return func.HttpResponse(f"Searching for {substance} \nResults: {query_res.to_string()}")

    else:
        return func.HttpResponse(
             "pubchem.",
             status_code=200
        )

@app.route(route="SubstanceList", auth_level=func.AuthLevel.ANONYMOUS)
def SubstanceList(req: func.HttpRequest) -> func.HttpResponse:

        #return func.HttpResponse(f"Results for {substance}: ")

        conn = duckdb.connect(':memory:')
        conn.execute("CREATE TABLE local_substances AS SELECT * FROM read_csv('HSDB.csv', header=1)")         
        query = "SELECT Name FROM local_substances"
        query_res = conn.execute(query).df()
        return func.HttpResponse(f"{query_res.to_string()}")
