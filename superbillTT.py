import boto3
import requests
from botocore.config import Config
import json
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import io
from tabless3super import extractTablesS3

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
        self, feature_types, *, document_file_name=None, document_bucket=None, document_bytes=None, local_document=False
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
            if local_document == True:
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
            elif local_document == False:
                try:
                    extractTablesS3(document_bucket, document_file_name)
                except ClientError:
                    logger.exception("Couldn't detect tables.")
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
    s3_client = boto3.client('s3')
    
    
    event = json.loads(event);
    textract_client = boto3.client('textract')
    s3_resource = boto3.resource('s3')
    sqs_resource = boto3.resource('sqs')
    bucket = s3_resource.Bucket('super-bill-bucket')
    file = bucket.Object('invoice_10.png')
    
    feature_types = 'TABLES'
    
    textract_obj = TextractWrapper(textract_client, s3_resource, sqs_resource)
    
    mem_file = io.BytesIO()
    file.download_fileobj(mem_file)
    mem_file.seek(0)
    #print(mem_file.getvalue())
    mem_file.close()
    FeatureTypes=["TABLES"]
    
    textract_obj.analyze_file(feature_types=FeatureTypes, document_bucket=bucket, document_file_name='invoice_10.png')
    
    
if (__name__=='__main__'):
    s3_client = boto3.client('s3')
    bucket_name = 'super-bill-bucket'
    object_name = 'invoice_22.pdf'
    presigned_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_name}, ExpiresIn=3600)
    output_route = 's3://super-bill-bucket/text-bucket/'
    request_example = '{'+'"getObjectContext": {'+'"inputS3Url": "'+presigned_url+'",'+'"outputRoute": "'+output_route+'",'+'"outputToken": "output-token"'+'}'+'}'
    context = Context
    smarttext_handler(request_example, context)