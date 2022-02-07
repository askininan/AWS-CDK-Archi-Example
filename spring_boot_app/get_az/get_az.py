#!./.venv/bin/python3

import boto3
    
def main():
    ec2 = boto3.resource('ec2')
    
    output = {}

    for instance in ec2.instances.all():
        for interface in instance.network_interfaces:
            output[instance.id] = {
                'Instance ID': instance.id,
                'Subnet ID': interface.subnet_id,
                'AZ': interface.subnet.availability_zone
            }

    print(output)


if __name__ == '__main__':
    main()