import time

import boto3

# Instantiate a boto3 client for RDS
rds = boto3.client('rds')

# User defined variables
username: str = 'user1'
password: str = '1234Ty'
db_subnet_group: str = 'vpc-test'
db_cluster_id: str = 'rds-id'

try:
    response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
    print(f'The DB cluster named {db_cluster_id} already exists. Skipping creation.')
except rds.exceptions.DBClusterNotFoundFault:
    response = rds.create_db_cluster(
        Engine='aurora-mysql',
        EngineVersion='5.7.mysql_aurora.2.11.1',
        DBClusterIdentifier=db_cluster_id,
        MasterUsername=username,
        MasterUserPassword=password,
        DatabaseName='rds_test_db',
        DBSubnetGroupName=db_subnet_group,
        EngineMode='serverless',
        EnableHttpEndpoint=True,
        ScalingConfiguration={
            'MinCapacity': 1,
            'MaxCapacity': 8,
            'AutoPause': True,
            'SecondUntilAutoPause': 300
        }
    )
    print(f'The DB cluster named {db_cluster_id} has been created.')

    while True:
        response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
        status = response['DBClusters'][0]['Status']
        print(f'The status of the cluster is {status}')
        if status == 'available':
            break

        print('Waiting for the DB Cluster to become available...')
        time.sleep(40)

# Modify the DB
response = rds.modify_db_cluster(
    DBClusterIdentifier=db_cluster_id,
    ScalingConfiguration={
        'MinCapacity': 1,
        'MaxCapacity': 16,
        'SecondUntilAutoPause': 600
    }
)
print(f'Updated the scaling configuration for DB cluster {db_cluster_id}.')

# Delete the DB cluster

delete_response = rds.delete_db_cluster(
    DBClusterIdentifier=db_cluster_id,
    SkipFinalSnapshot=True
)
print(f'The {db_cluster_id} is being deleted.')
