from optparse import OptionParser
import hashlib
import string
import boto3
import os

s3Cli = boto3.client("s3")

def toUrlShort(option, opt_str, value, parser):
    longUrl = str(value)
    # CloudFront will handle all url ending with 5u and send to urls folder
    key = hashlib.sha1(longUrl).hexdigest()[:4] + "5u";
    uploadFile(key, longUrl)
    print "http://danilo.cc/" + key

def uploadFile(key, longUrl):
    response = s3Cli.put_object(
        ACL='public-read',
        Body='',
        Bucket='danilo.cc',
        Key='urls/' + key,
        WebsiteRedirectLocation=longUrl,
        StorageClass='REDUCED_REDUNDANCY'
        )

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", "--url", action="callback", callback=toUrlShort, help="Long Url", dest="longUrl", type='str')
    (options, args) = parser.parse_args()
