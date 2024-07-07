import boto3

def create_file(session=None, *, bucket, file_name, byte_data):
    session = session
    if session != None:
        s3 = session.resource('s3')
    else:
        s3 = boto3.resource('s3')
    
    s3_object = s3.Object(bucket, file_name)
    result = s3_object.put(byte_data)
    