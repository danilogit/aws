#!/bin/python

import boto3
import os
import sys

# Environment variables to set
# INSTANCE_ID=
# INSTANCE_PUBLIC_IP=
# EIP_ALLOCATION_ID=
# EIP_SCOPE=vpc|standard


class ec2:

    instanceId = None
    instance = None
    ec2Client = None

    def __init__(self):
        self.instanceId = os.environ['INSTANCE_ID']
        self.ec2Client = boto3.resource("ec2")
        self.instance = self.ec2Client.Instance(self.instanceId)
        self.getStatus()

    def getStatus(self):
        state = self.instance.state
        return state['Name']

    def start(self):
        print "Starting instance ", self.instanceId
        self.instance.start()
        self.instance.wait_until_running()
        self.updateIpAddress()
        print "Instance Running"

    def stop(self):
        print "Instance stopped", self.instanceId
        self.instance.stop()

    def updateIpAddress(self):

        scope = os.environ['EIP_SCOPE']
        client = boto3.client('ec2')
        public_ip = os.environ['INSTANCE_PUBLIC_IP']
        allocation_id = os.environ['EIP_ALLOCATION_ID']

        try:
            # FIXME: Allocate IP only for standard public ip, or create a force option
            if(scope == 'vpc'):
                response = client.associate_address(
                    InstanceId=self.instanceId,
                    AllocationId=allocation_id
                )
            elif scope == 'standard':
                response = client.associate_address(
                    InstanceId=self.instanceId,
                    PublicIp=public_ip
                )

            print "EC2 Public IP is ", public_ip
        except:
            print "Error allocating public ip address ", public_ip


    def toggleStatus(self):
        status = str(self.getStatus())

        print "Instance status", status
        if status == "running":
            self.stop()
        elif status == 'stopped':
            self.start()


if __name__ == '__main__':
    ec2 = ec2()

    if len(sys.argv) == 2:
        command = sys.argv[1]
    else:
        command = 'toggle'

    if command == 'toggle':
        ec2.toggleStatus()
    elif command == 'status':
        print ec2.getStatus()
    elif command == 'start':
        ec2.start()
    elif command == 'stop':
        ec2.stop()
