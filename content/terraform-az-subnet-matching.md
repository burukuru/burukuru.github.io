Title: Create VPC Endpoints only in a subset of availability zones
Date: 2020-06-06 14:20
Author: Thanh
Category: DevOps
Tags: devops, terraform, aws
Status: draft

# Reduced availability
A common practice when using AWS is to deploy to multiple availability zones (AZs) for resiliency, usually this would be 3 AZs, though some bigger [AWS regions have more than 3 AZs](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/): us-east-1 (6), us-west-2 (4), ap-northeast-1 (4).

When making a decision to deploy your services to only a few of those AZs, for cost savings or otherwise, you will need to match the resources in the VPC that consumes those services to subnets/availability zones where the services are available. This should be easy except that AWS availability zone names do not represent the same AZ in each account, you need [AZ IDs](https://docs.aws.amazon.com/ram/latest/userguide/working-with-az-ids.html) for that. You could hard code AZ IDs everywhere but that sounds like more headache down the line.

Instead, what we can do is look up which AZs the services are in from the consumer account and deploy to the matching subnets.

# Terraform
In Python this would be a list comprehension, in any other language a for loop, in Terraform we will need to use the [matchkeys() function](https://www.terraform.io/docs/configuration/functions/matchkeys.html).

In this specific example, we are deploying a service in one AWS account and exposing it to another AWS account via a VPC endpoint service.  The consumer account needs to deploy a VPC endpoint in the subnet matching the AZ of the service.

## AZ to subnet mapping

In the VPC module of your consumer account, we need to create a new output which is a map of AZs to subnets. This will later allow us to look up the AZ of the service and obtain the corresponding subnet that we need to use for our 'consumer' resource.
```tf
output "az_subnet_map" {
        value = zipmap(aws_subnet.private[*.availability_zone, aws_subnet.private[*].id)
}
```

## Get availability zones for the endpoint services
In terraform.tfvars, specify the VPC endpoints services to connect to.
```tf
vpc_endpoint_services ={ 
        service1 = {
                service_name = "com.amazonaws.us-east-1.service1"
                description  = "Service1 from Account A"
        }
}
```

Obtain the endpoint services' AZs by doing a data lookup. This will return the AZ as named in the consumer account, which is not necessarily the same as the service's account.

```tf
data "aws_vpc_endpoint_service" "selected" {
        for_each = var.vpc_endpoint_services

        service_name = each.value[service_name]
}
```

## Match the endpoint services to our subnets
Use `matchkeys` to look up the AZs of the endpoint services in the AZ->subnet map of our VPC and return the corresponding subnets.
This will create VPC endpoints in AZs where the endpoint services are deployed.

```tf
resource "aws_vpc_endpoint" "vpc_endpoints" {

        for_each = var.vpc_endpoint_services

        service_name        = each.value[service_name]
        subnet_ids          = flatten([matchkeys(
                        values(module.vpc.az_subnet_map),
                        keys(module.vpc.az_subnet_map),
                        data.aws_vpc_endpoint_service.selected[each.key].availability_zones
                        )])

        vpc_id              = module.vpc.vpc_id
        security_group_ids  = [aws_security_group.endpoint.id]
        vpc_endpoint_type   = "Interface"
        private_dns_enabled = false
        auto_accept         = true

}
```

# Considerations
Despite saving money on the deployments, you will incur cross-AZ data transfer costs if your consumer account uses more AZs than the service provider account. You need to weight up the benefits in your deployment.
