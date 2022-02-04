import boto3

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