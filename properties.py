metadata={
	"headers":{'Content-Type':'application/json'},
	"base_url":"https://<f5_ip>/mgmt/tm/ltm/", #public ip of your F5 box
	"username":"<username>", # F5 console username
	"password":"<password>", #F5 console password
	"TopicArn":"<sns_topic_arn>",# SNS topic ARN created for AutoScaling group HTTP notification
	"launch_event":"autoscaling:EC2_INSTANCE_LAUNCH",
	"launch_fail_event":"autoscaling:EC2_INSTANCE_LAUNCH_ERROR",
	"terminate_event":"autoscaling:EC2_INSTANCE_TERMINATE",
	"access_key":"<access_key>",
	"secret_key":"<secret_key>",
	"aws_region":"ap-southeast-1",
	"aws_region_endpoint":"ec2.ap-southeast-1.amazonaws.com"
}



mapping={

"<autoscaling_group_name>":{ # AS Group name as it appears on the AWS console
	"pools":["<F5 pool 1 name>","<F5 pool 2 name>"], # List of F5 pools this node should belong.
	"node_attributes":{
		"partition":"Common",
		"connectionLimit":0, 
		"dynamicRatio":1,
		"logging":"disabled",
		"monitor":"default",
		"rateLimit":"disabled",
		"ratio":1,	
		"port":"80"		
		}
	}
# ......
# Keep adding more AS Groups to this mapping object

}
