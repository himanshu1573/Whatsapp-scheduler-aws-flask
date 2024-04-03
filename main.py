from flask import Flask, request, jsonify
import boto3
import uuid
import json
from datetime import datetime

app = Flask(__name__)

client = boto3.client('scheduler')

@app.route('/schedule_lambda', methods=['POST'])
def schedule_lambda():
    body = request.get_json()

    if body.get('type') == 'One_Time':
        response = client.create_schedule(
            ActionAfterCompletion='NONE',
            Description='This Schedule is created for  Lambda functions',
            FlexibleTimeWindow={'Mode': 'OFF'},
            ScheduleExpression='at({})'.format(body.get('one_time_schedule')),
            ScheduleExpressionTimezone='Asia/Kolkata',
            Target={
                 'Arn': 'arn:aws:lambda:ap-south-1:837299133726:function:him_scheduler',
                'Input': json.dumps(body),  # Send the entire request body as input to the Lambda function
                'RoleArn':'arn:aws:iam::837299133726:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_375614c3be'
            },
            Name='Himanshu_' + str(uuid.uuid4()),
        )
    else:
        time = body.get('schedule').get('time')
        print(body)
        
        response = client.create_schedule(
            ActionAfterCompletion='NONE',
            Description='This Schedule is created using Lambda functions',
            EndDate=datetime.fromtimestamp(body.get('schedule').get('end')) ,
            FlexibleTimeWindow={'Mode': 'OFF'},
            ScheduleExpression='cron({} {} * * ? *)'.format(time.get('minute'), time.get('hour')),
            ScheduleExpressionTimezone='Asia/Kolkata',
            StartDate=datetime.fromtimestamp(body.get('schedule').get('start')),
            Target={
                'Arn': 'arn:aws:lambda:ap-south-1:837299133726:function:him_scheduler',
                'Input': json.dumps(body),
                'RoleArn':'arn:aws:iam::837299133726:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_375614c3be'
            },
            Name='Himanshu_' + str(uuid.uuid4()),
        )

    return jsonify({"message": "Scheduled successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)
