import json
import os
import urllib3

headers = {
	"Authorization": os.environ["APIKEY"],
	"Content-Type": 'application/json'
}

def lambda_handler(event, context):
    numbers = event.get('recipients')
    http = urllib3.PoolManager()
    
    
    for number in numbers:
    	data = {
    		"message": [
    				{
    					"recipient_whatsapp": number.get('Mobile'),
    					"recipient_type": "individual",
    					"message_type": "Template",
    					"source": os.environ["SOURCE"],
    					"type_template": [
    						{
    							"name": event.get('template'),
    							"attributes": [
    									event.get('title')
    								],
    								"language": {
    									"locale": "en",
    									"policy": "deterministic"
    								}
    						}
    					]
    				}
    			]
    	}
    	if event.get('is_media_template'):
    	    data["message"][0]["message_type"] = "media_template"
    	    data["message"][0].update({
    	        "type_media_template": {
    	            "type": "image",
    	            "url": "https://vivek-whatsapp-s3.s3.ap-south-1.amazonaws.com/{}".format(event.get("media"))
    	        }
    	    })

    	try:
    	    response = http.request(method='POST', url=os.environ["MESSAGE_URL"], body=json.dumps(data), headers=headers, timeout=5)
    	except Exception as e:
    	    print(e)
    	    return {'statusCode': 500, 'body': "Soemthing went wrong!"}
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    