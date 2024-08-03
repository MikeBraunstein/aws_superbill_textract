import boto3

def create_file(bucket, file_name, byte_data, *, session=None):
    session = session
    if session != None:
        s3 = session.resource('s3')
    else:
        s3 = boto3.resource('s3')
    
    bucket = 'arn:aws:s3:us-east-1:722582923054:accesspoint/super-bill-access-point/object/text-bucket/'#+= '\'' + 'textbucket'
    print(bucket)
    s3_object = s3.Object(bucket, file_name)
    result = s3_object.put(Body=byte_data)
    print('createfile after result')
    
if __name__ == '__main__':
    create_file('super-bill-bucket', 'invoice_10.png', 'body')