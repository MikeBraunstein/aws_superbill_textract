import boto3
import requests
from botocore.config import Config
import json

class TextractWrapper:
    """Encapsulates Textract functions."""

    def __init__(self, textract_client, s3_resource, sqs_resource):
        """
        :param textract_client: A Boto3 Textract client.
        :param s3_resource: A Boto3 Amazon S3 resource.
        :param sqs_resource: A Boto3 Amazon SQS resource.
        """
        self.textract_client = textract_client
        self.s3_resource = s3_resource
        self.sqs_resource = sqs_resource


    def analyze_file(
        self, feature_types, *, document_file_name=None, document_bytes=None
    ):
        """
        Detects text and additional elements, such as forms or tables, in a local image
        file or from in-memory byte data.
        The image must be in PNG or JPG format.

        :param feature_types: The types of additional document features to detect.
        :param document_file_name: The name of a document image file.
        :param document_bytes: In-memory byte data of a document image.
        :return: The response from Amazon Textract, including a list of blocks
                 that describe elements detected in the image.
        """
        if document_file_name is not None:
            with open(document_file_name, "rb") as document_file:
                document_bytes = document_file.read()
        try:
            response = self.textract_client.analyze_document(
                Document={"Bytes": document_bytes}, FeatureTypes=feature_types
            )
            logger.info("Detected %s blocks.", len(response["Blocks"]))
        except ClientError:
            logger.exception("Couldn't detect text.")
            raise
        else:
            return response

class Context:
    def __init__(self):
        self.function_name = "test_function"
        self.memory_limit_in_mb = 128
        self.invoked_function_arn = "arn:aws:lambda:us-west-2:123456789012:function:test_function"
        self.aws_request_id = "test_request_id"

def smarttext_handler(event, context):
    event = json.loads(event);
    textract_client = boto3.client('textract')
    s3_resource = boto3.resource('s3')
    sqs_resource = boto3.resource('sqs')
    #textract = TextractWrapper(textract_client, s3_resource, sqs_resource)
    print(s3_resource)
    print(sqs_resource.get_queue_by_name(QueueName = 'SuperBillQueue'))
    textract = TextractWrapper
    #textract.__init__(textract_client, s3_resource, sqs_resource)
'''
    document = {
        'Bytes': b'bytes',
        'S3Object': {
            'Bucket': 'string',
            'Name': 'string',
            'Version': 'string'
        }
    }'''
    s3_client = boto3.client('s3')
    try:
    # Get the file inside the S3 Bucket
    s3_response = s3_client.get_object(
        Bucket='super-bill-bucket',
        Key='invoice_22.pdf'
    )

    # Get the Body object in the S3 get_object() response
    s3_object_body = s3_response.get('Body')

    # Read the data in bytes format and convert it to string
    content_str = s3_object_body.read().decode()

    # Print the file contents as a string
    print(content_str)

except s3_client.exceptions.NoSuchBucket as e:
    # S3 Bucket does not exist
    print('The S3 bucket does not exist.')
    print(e)

except s3_client.exceptions.NoSuchKey as e:
    # Object does not exist in the S3 Bucket
    print('The S3 objects does not exist in the S3 bucket.')
    print(e)
    feature_types = 'TABLES'
    textract.analyze_file(feature_types, document_file_name='invoice_22.pdf', document_byte_data=)
    
if (__name__=='__main__'):
    s3_client = boto3.client('s3')
    bucket_name = 'super-bill-bucket'
    object_name = 'invoice_22.pdf'
    presigned_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_name}, ExpiresIn=3600)
    output_route = 's3://super-bill-bucket/text-bucket/'
    request_example = '{'+'"getObjectContext": {'+'"inputS3Url": "'+presigned_url+'",'+'"outputRoute": "'+output_route+'",'+'"outputToken": "output-token"'+'}'+'}'
    context = Context
    #smarttext_handler(request_example, context)