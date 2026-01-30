import json
import uuid
import boto3
import datetime

from stlv_resources import Resources


def hello_world(event, context):
    return {
        "statusCode": 200,
        "body": "Hello, World!",
    }


def post_todo(event, context):
    body = json.loads(event.get("body", "{}"))

    todo = {
        "user": body.get("name", "Stranger"),
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "text": body.get("text", ""),
        "finished": body.get("finished", False),
        "id": uuid.uuid4().hex,
    }

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(Resources.todos_table.table_name)
    table.put_item(Item=todo)
    return {
        "statusCode": 200,
        "body": json.dumps(todo, indent=4),
    }


def get_todos(event, context):
    user = event["pathParameters"]["user"]

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(Resources.todos_table.table_name)
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("user").eq(user)
    )
    items = response.get("Items", [])

    return {
        "statusCode": 200,
        "body": json.dumps(items, indent=4),
    }


def cleanup(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(Resources.todos_table.table_name)
    # Example cleanup logic: delete all finished items
    scan = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr("finished").eq(True)
    )
    for item in scan["Items"]:
        table.delete_item(
            Key={
                "id": item["id"],
            }
        )

    return {
        "statusCode": 200,
        "body": "Cleanup completed.",
    }
