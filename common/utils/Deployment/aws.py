
#* Importing Libraries
import os
import boto3
import uuid

#* Global Variables
S3_BUCKET = os.environ.get('S3_BUCKET')

class ImageClass:
    
    def upload_image(self, file, bucket = S3_BUCKET, namespace = "Images"):
        '''
            Used to upload images to AWS S3 bucket. Retruns a link to the file.
            
            Args:
            ----
            file (`File`): File Object.
            bucket (`String`): Name of the s3 bucket.
            namespace (`String`): Name of the folder.
            
            Returns:
            -------
            image_path (`String | Boolean(False)`) : Url of the image.
        '''

        s3 = boto3.client("s3")
        
        name,extention = str(file.name).split('.')
        
        name = str(name) + '_' + str(uuid.uuid1().int)[-5:] + '.' + str(extention)
        s3_key = '{0}/{1}'.format(namespace, name)

        # Send the file
        result = s3.put_object(
            Bucket=bucket,
            Key=s3_key,
            Body=file,
            ACL='public-read',
            ContentType = 'image/jpeg'
        )
        
        if result['ResponseMetadata']['HTTPStatusCode'] == 200:
            response = "https://{0}.s3.us-east-2.amazonaws.com/{1}".format(bucket, s3_key)
        else:
            response = False

        return response