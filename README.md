
# AWS-CDK-ARCH

This project content demonstrates an AWS CDK app with an instance of a stack (`aws-cdk-arch_stack.py`) which contains two auto-scaling groups to be deployed two different subnets (AZs) fronted by an ALB. After deployment of 
ASGs, regarded EC2 instances contain user data that installs and starts httpd. User data also contains a custom script that returns AZ that the instance deployed on by simply executing `./hello` command.

Bonus: There is a python script in get_az folder that leverages boto3 lib to return info about deployed EC2 instances including their AZs.

Stack-file: spring_boot_app/aws-cdk-arch_stack.py
## Building Steps

* `npm install -g aws-cdk`                install aws-cdk

* `python3 -m venv .venv`                 create virtualenv

MAC and Linux
 * `source .venv/bin/activate`            activate your virtualenv

Windows
 * `.venv\Scripts\activate.bat`           activate your virtualenv     

After activating virtualenv:
 * `pip install -r requirements.txt`      install requirements into virtualenv 


Deployment

 * `cdk bootstrap aws://ACCOUNT-NUMBER-1/REGION-1`       bootstrap cdk with your account and a specific region
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk diff`        compare deployed stack with current state
 * `cdk deploy`      deploy this stack to your default AWS account/region


To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

