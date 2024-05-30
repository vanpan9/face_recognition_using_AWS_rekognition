import boto3
import json



s3= boto3.client("s3")
rekognition = boto3.client("rekognition",region_name="us-east-1")
dynamodb_table ="employees"
dynamodb = boto3.resource("dynamodb",region_name="us-east-1")

employee_table= dynamodb.Table(dynamodb_table)
bucket_name="van-emp-visitor-img"

def lambda_handler(event,context):
    print(event)

    object_key= event["queryStringParameters"]["objectKey"]
    image_bytes=s3.get_object(Bucket=bucket_name, Key=object_key)["Body"].read()
    response=rekognition.search_faces_by_image(
        CollectionId = "employee",
        Image={"Bytes":image_bytes}

    )


    for match in response["FaceMatches"]:
        print(match["Face"]["FaceId"],match["Face"]["Confidence"]) 

        face=  employee_table.get_item(
        Item={
            "rekognitionId": match["Face"]["FaceId"]
        }
    ) 
        
    if 'Item' in face:
        print("Person Found ",face["Item"])
        return buildResponse(200,{
            "Message":"Success",
            "firstName": face["Item"]["firstName"],
            "lastName": face["Item"]["lastName"]
        })  
    print("Person can't be recognised")
    return buildResponse(403,{
        "Message":"Person Not Found"
    })



def buildResponse(StatusCode,body=None):
      response={
           "StatusCode":StatusCode,
           "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",


           }
      }

      if body is not None:
           response["body"]=json.dumps(body)
      return response     



