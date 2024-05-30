import boto3

s3= boto3.client("s3")
rekognition = boto3.client("rekognition",region_name="eu-north-1")
dynamodb_table ="employee"
employee_table= boto3.Table(dynamodb_table)


def lambda_handler(event,context):
    print(event)
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key= event["Records"][0]["s3"]["object"]["key"]


    try:
        response = index_employee_image(bucket,key)
        print(response)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            faceid= response["FaceRecords"][0]["Face"]["FaceId"]
            name= key.split(".")[0].split("_")
            firstname=name[0]
            lastname= name[1]
            register_employee(faceid,firstname,lastname)

        return  response
       
    except Exception as e:
        print(e)    
        print("error processing image {} from bucket {}".format(key,bucket))


def index_employee_image(bucket,key):
    response = rekognition.index_faces(
        Image={
            "S3Object":
            {
                "Bucket":bucket,
                "Name": key,
            }
        },
        CollectionId= "employees"
    )
    return response


def register_employee(faceid,firstname,lastname):
    employee_table.put_item(
        Item={
            "rekognitionId":faceid,
            "firstname":firstname,
            "lastname":lastname,

        }
    )