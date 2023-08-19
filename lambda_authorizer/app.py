import os


def lambda_handler(event, context):
    method_arn = event['methodArn']
    token = event['headers']['Authorization']
    principal_id = 'user'

    bearer_token = f"Bearer {os.getenv('AUTH_TOKEN')}"
    # print(token)
    # print(bearer_token)
    
    if token == bearer_token:  
        policy_document = {
            'principalId': principal_id,
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Effect': 'Allow',
                        'Resource': method_arn
                    }
                ]
            }
        }
    else:
        policy_document = {
            'principalId': principal_id,
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Effect': 'Deny',
                        'Resource': method_arn
                    }
                ]
            }
        }

    return policy_document
