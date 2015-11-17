docker-machine create \
--driver amazonec2 \
--amazonec2-access-key $AWS_ACCESS_KEY_ID \
--amazonec2-secret-key $AWS_SECRET_ACCESS_KEY \
--amazonec2-vpc-id $AWS_VPC_ID \
--amazonec2-region eu-west-1 \
--amazonec2-zone c \
$1