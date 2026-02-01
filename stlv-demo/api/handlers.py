import json
import datetime
import uuid
import boto3


def hello_world(event, context):
    return {"statusCode": 200, "body": "Hello World!"}


def post_todo(event, context):
    from stlv_resources import Resources

    body = json.loads(event.get("body", "{}"))

    todo = {
        "user": body.get("name", "Stranger"),
        "text": body.get("text", ""),
        "finished": body.get("finished", False),
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "id": uuid.uuid4().hex,
    }

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(Resources.todos_table.table_name)

    table.put_item(Item=todo)

    return {"statusCode": 200, "body": json.dumps(todo)}


def list_todos(event, context):
    from stlv_resources import Resources

    user = event["pathParameters"]["user"]

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(Resources.todos_table.table_name)

    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("user").eq(user)
    )
    items = response.get("Items", [])

    if not items:
        items = {"message": "No Items"}

    return {"statusCode": 200, "body": json.dumps(items)}


def cleanup(event, context):
    from stlv_resources import Resources

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(Resources.todos_table.table_name)

    scan = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr("finished").eq(True)
    )
    for item in scan["Items"]:
        table.delete_item(Key={"id": item["id"]})
