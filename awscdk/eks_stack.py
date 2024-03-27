from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_iam as iam,
)
from constructs import Construct


class CdkEKStack(Stack):
    print("this is VPC")
    def __init__(self, scope: Construct, construct_id: str, environment: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        print("this is VPC")

        vpc_id="vpc-xxxxxxxx"
        vpc = ec2.Vpc.from_lookup(self, "vpc", vpc_id=vpc_id)
        print("This is the vpc ", vpc.vpc_id)
        vpc_subnets = [{'subnetType': ec2.SubnetType.PUBLIC}]
        # vpc_subnets=vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC).subnets

        # create eks admin role
        eks_master_role = iam.Role(self, 'EksMasterRole',
                                   role_name='EksAdminRole',
                                   assumed_by=iam.AccountRootPrincipal()
                                   )
        
        cluster = eks.Cluster(self, 'Cluster',
                              vpc=vpc,
                              version=eks.KubernetesVersion.V1_25,
                              masters_role=eks_master_role,
                              default_capacity=0,
                              vpc_subnets=vpc_subnets
                              )
        
        # create eks managed nodegroup
        nodegroup = cluster.add_nodegroup_capacity('eks-nodegroup',
                                                   instance_types=[ec2.InstanceType('t2.medium')],
                                                   disk_size=50,
                                                   min_size=2,
                                                   max_size=2,
                                                   desired_size=2,
                                                   subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC))
                                                #    remote_access=eks.NodegroupRemoteAccess(
                                                #        ssh_key_name='ie-prod-snow-common'),
                                                #    capacity_type=eks.CapacityType.SPOT)

