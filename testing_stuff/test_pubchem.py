import duckdb
import jsonschema
import json

# Metodo che prova a collegarsi ad un file csv non vuoto e controlla che la struttura sia corretta
def test_PubChem_Index_table():
    conn = duckdb.connect(':memory:')
    assert(conn.execute("CREATE TABLE pubchem_live AS SELECT * FROM read_csv('pubchem.csv', header=1)"))
    # Verifico che esista un file pubchem.csv dal quale caricare l'indice delle sostanze 

    result = conn.execute("SELECT * FROM pubchem_live ORDER BY substances ASC").df()
    
    assert list(result.columns) == ['cid', 'substances']
    assert len(result) != 0
    # Verifico che il csv appena caricato in memoria abbia queste due colonne: CID e Substances e che non sia vuoto
    
    conn.close()

    return True


def test_substance_snapshot(snapshot):
    # Metodo per lo snapshot testing. Carico il csv attraverso duckdb e cerco una sostanza specifica
    substance_name = 'NITROGLYCERIN'
    conn = duckdb.connect(':memory:')
    conn.execute("CREATE TABLE pubchem_live AS SELECT * FROM read_csv('pubchem.csv', header=1)")
    conn.execute("CREATE TABLE local_substances AS SELECT * FROM read_csv('HSDB.csv', header=1)")         
                    
    query = "SELECT Measure, Toxicity, Reference FROM local_substances WHERE Name = ?"
    query_res = conn.execute(query, [substance_name]).df()
    #print(query_res.to_csv())

    #query_res.to_csv('testing_stuff/snap_csv_substance_pubchem.csv')
    # Query che ho usato per creare il csv da confrontare
    #snapshot.snapshot_dir = 'testing_stuff'  # This line is optional.
    snapshot.assert_match(query_res.to_csv().replace('\r', ''), 'snap_csv_substance_pubchem.csv')

    conn.close()

def test_ingredient_json():
    # Testo il JSON Schema
    schema_file = 'schema.json'
    data_file = 'pubchem.json'
    with open(schema_file, 'r') as f:
        schema = json.load(f)

    with open(data_file, 'r') as f:
        data = json.load(f)

    assert bool_validate(instance=data,schema=schema) == True

def bool_validate(instance,schema):
    try:
        jsonschema.validate(instance=instance,schema=schema)
        return True
    except:
        return False
#substance_snapshot()

