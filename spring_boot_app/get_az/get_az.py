import boto3

ec2 = boto3.resource('ec2')

# instances = ec2.instances.filter(
#     Filters=[
#         {'Name': 'instance-state-name', 'Values': ['running']}
#     ]
# )

# for instance in instances:
#    print(instance.id, instance.instance_type, instance.private_ip_address)

  
output = {}

for instance in ec2.instances.all():
    for iface in instance.network_interfaces:
        output[instance.id] = {
            'Instance ID': instance.id,
            'Subnet ID': iface.subnet_id,
            'AZ': iface.subnet.availability_zone
        }

print(output)