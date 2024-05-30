import requests
lambda_endpoint = "https://cpf37oq7de.execute-api.us-east-1.amazonaws.com/dev/"

file={'files': open('shinchan_nohara.jpeg','rb')}
print(requests.post(lambda_endpoint, files=file))
#response = requests.post(lambda_endpoint, files=file, headers=headers)

# Print the response

#response = requests.post(lambda_endpoint, files=files)

# if response.status_code == 200:
#     result = response.json()
#     if result['authenticated']:
#         print('Image authenticated successfully')
#     else:
#         print('Image authentication failed')
# else:
#     print('Error while authenticating image')

