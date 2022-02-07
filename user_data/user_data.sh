#!/bin/bash
sudo yum update -y
sudo yum -y install httpd php
sudo chkconfig httpd on
sudo service httpd start


echo curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone/ > hello
chmod +x hello