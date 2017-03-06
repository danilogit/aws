#!/bin/bash
import boto3
from email.parser import Parser 
import os

# Need improvements
class SesForward:

    sesClient = None
    s3Client = None
    forwardTo = ["recipient@example.com"] #os.environ['']
    forwardFrom = "you@example.com"
    bucketName = ""
    bucketPrefix = ""

    def __init__(self):
        self.s3Client = boto3.client("s3")
        self.sesClient = boto3.client("ses")

        pass

    def sendEmail(self):
      
        f = open("/tmp/mail.txt")
        m = Parser().parse(f)      

        m.add_header("X-Original-From", m['from'])
        m.add_header("Reply-To", m['from'])
        m.replace_header("From", self.forwardFrom)
        m.replace_header("Return-Path", "");
        
        result = self.sesClient.send_raw_email(RawMessage= {'Data': bytearray(m.as_string())}, Destinations = self.forwardTo)

	os.remove("/tmp/mail.txt")
        


    def readRawEmail(self, messageId):
        
        key = self.bucketPrefix + "/" + messageId     
        self.s3Client.download_file(self.bucketName, key, "/tmp/mail.txt")
        pass


if __name__ == "__main__":
    f = SesForward()
    f.readRawEmail("<MessageIdForTestOnly>")
    f.sendEmail()

def lambda_handler(event, context):
    ses_notification = event['Records'][0]['ses']
    message_id = ses_notification['mail']['messageId']
    f = SesForward()
    f.readRawEmail(message_id)
    f.sendEmail()
