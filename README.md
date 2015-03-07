# AWSAutoScalingWithF5
Flask based microservice to integrate AWS Autoscaling with F5 BIG-IP

### How it works:

AWS Autoscaling is a service which maintains a pool of servers at the desired level or helps to scale the numbers up and down based on traffic/load patterns. 

It comes very well coupled with AWS ELB where nodes are added and removed as the instances go up and down. But it becomes challenging when one cannot use ELB. Here we are going to integrate F5 BIG-IP with autoscaling.

Just select the Autoscaling group in the AS console. Go to the Notifications tab and create an HTTP notification for all the Autoscaling Events. You just need to run this application on a public server which is acessible to public. As the nodes are added/removed from the AutoScaling Group/s AWS sends out notifications to this endpoint and it adds/removed nodes from F5 pools accordingly.



### Dependencies:
* Requests
* Flask
* Boto

### How to setup:

**properties.py** file contains all the metadata/mapping that this aplication needs to know which pool to add/remove node to/from. Modify these attributes accordingly.

### How to run:

**python app.py**

The application run of port 5000 by default. Health Check url is **/** and the scaling endpoint is **/scale** which accepts JSON input which the AWS SNS send to it. 

 
