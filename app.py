import requests
import base64
from flask import Flask, render_template, request
import boto3

app = Flask(__name__)
rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')


# Landing page route
@app.route('/')
def index():
   
    return render_template('index.html')


# Route to handle image upload
@app.route('/upload', methods=['POST'])
def upload():
   if 'file' not in request.files:
        return 'No file part'

   file = request.files['file']

   if file.filename == '':
        return 'No selected file'

    # Get the filename of the uploaded file
   filename = file.filename
   file.save('visitors/'+filename)
   with open('visitors/'+filename,'rb') as f:
        image_bytes = f.read()
   collection_id="employee"
   # Match the image with the Rekognition collection
   matched_image_info = match_image_with_collection(image_bytes, collection_id)
   table_name = 'van-employee-table'  # Replace with your DynamoDB table name
   
   if matched_image_info:
       facid = matched_image_info[0]["Face"]["FaceId"]  # Replace with the facid you want to check
       first_name, last_name = get_name_from_dynamodb(table_name, facid)
  
   else:
        first_name = "unkown"
        last_name = "unknown"
  
   return render_template("index.html",matched_image_info=matched_image_info,first_name=first_name,last_name=last_name)




def match_image_with_collection(image_bytes, collection_id, threshold=80):
    try:
        response = rekognition.search_faces_by_image(
            CollectionId=collection_id,
            Image={'Bytes': image_bytes},
            FaceMatchThreshold=threshold,
            MaxFaces=1
        )
        face_matches = response['FaceMatches']
        return face_matches
    except Exception as e:
        print(f"Error matching image with collection: {e}")
        return []

def get_name_from_dynamodb(table_name, facid):
    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={'rekID': {'S': facid}}
        )
    # Check if the item exists in the response
        if 'Item' in response:
            # Extract first name and last name from the item
            item = response['Item']
            first_name = item.get('firstname', {}).get('S', 'Unknown')
            last_name = item.get('lastname', {}).get('S', 'Unknown')
            return first_name, last_name
        else:
            return None, None  # Item does not exist
    except Exception as e:
        print(f"Error retrieving name from DynamoDB: {e}")
        return None, None  # Assume item does not exist in case of error

    

if __name__ == '__main__':
    app.run(debug=True)
