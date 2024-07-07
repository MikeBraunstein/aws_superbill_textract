import boto3
from trp import Document

def extractTablesS3(bucket_name, document_name):
    # Document
    documentName = document_name
    # Bucket
    s3BucketName = bucket_name
    
    # Amazon Textract client
    textract = boto3.client('textract')
    
    # Call Amazon Textract
    response = textract.analyze_document(
        Document={
            'S3Object': {
            'Bucket': s3BucketName,
            'Name': documentName
            }
        },
        FeatureTypes=["TABLES"])
    '''
    It seems that you only have to pass byte data to Textract if/when you are attempting to process localy.
    If you are processing from an s3 bucket, simply send the S3Object as seen above.'''
    #print(response)
    
    doc = Document(response)
    print(doc)
    #'''Commented out for in loop to test doc object
    for page in doc.pages:
         # Print tables
        for table in page.tables:
            for r, row in enumerate(table.rows):
                for c, cell in enumerate(row.cells):
                    print("Table[{}][{}] = {}".format(r, c, cell.text))
                    
if(__name__=='__main__'):
    extractTablesS3('super-bill-bucket', 'invoice_10.png')