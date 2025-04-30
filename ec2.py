import boto3

ec2 = boto3.resource('ec2')
instance_name: str = 'Test instance 123 Wojtek 123'

instance_id: None = None

# Check if instance already exists

instances_list: list = ec2.instances.all()
instance_exists: bool = False

for instance in instances_list:
    for tag in instance.tags:
        if tag['Key'] == 'Name' and tag['Value'] == instance_name:
            instance_exists: bool = True
            instance_id = instance.id
            print(f'An instance named {instance_name} with id {instance_id} already exists.')
            break
    if instance_exists:
        break

if not instance_exists:
    # Creating new EC2 instance
    new_instance = ec2.create_instances(
        ImageId='ami-0d8d11821a1c1678b',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='TEST-KEY',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'None',
                        'Value': instance_name
                    },
                ]
            },
        ]
    )
    instance_id = new_instance[0].id
    print(f'Instance named {instance_name} with id {instance_id} created.')

# Stop instance
ec2.Instance(instance_id).stop()
print(f'Instance named {instance_name}-{instance_id} has been stopped.')

# Start an instance
ec2.Instance(instance_id).start()
print(f'Instance named {instance_name}-{instance_id} has been started.')

# Terminate an instance
ec2.Instance(instance_id).terminate()
print(f'Instance named {instance_name}-{instance_id} has been terminated.')
