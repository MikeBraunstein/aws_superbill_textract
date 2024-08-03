import boto3
from savecash import savecash

def detectTextS3(s3_bucket, document_name):
    # Document
    s3BucketName = s3_bucket
    documentName = document_name
    print("You've made it this far!")
    
    # Amazon Textract client
    textract = boto3.client('textract')
    '''
    # Call Amazon Textract
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': documentName
            }
        })'''
    
    response = savecash()
    #print(response)
    #print(response["Blocks"])
    # Print detected text
    for item in response["Blocks"]:
        #print(item)
        print(item["BlockType"])
        if item["BlockType"] == "LINE":
            print(item["Text"])
            if item["Text"] == 'Reproductive Psychiatry and Counseling':
                return(True);
                #break;
            #print ('\033[94m' +  item["Text"] + '\033[0m')
    return(False);
#print(__name__) 
if(__name__ == '__main__'):
    detectTextS3('super-bill-bucket', 'invoice_10.png')