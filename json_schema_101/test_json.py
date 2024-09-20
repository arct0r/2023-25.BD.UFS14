from jsonschema import validate
schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}

def func(x):
    return x + 1


def test_answer():
    assert func(4) == 5


def validate_wrapper(instance, schema):
    try:
        validate(
            instance=instance,
            schema=schema
        )
        return True
    except:
        return False


def test_success():
    assert validate_wrapper(
        instance={"name" : "Eggs", "price" : 333}, schema=schema,
    ) 

def test_fail():
    assert validate_wrapper(
        instance={"name" : "Eggs", "price" : '333'}, schema=schema,
    ) == False