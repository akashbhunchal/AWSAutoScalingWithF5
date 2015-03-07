metadata={
	"headers":{'Content-Type':'application/json'},
	"base_url":"https://<f5_ip>/mgmt/tm/ltm/",
	"username":"<username>",
	"password":"<password>",
	"TopicArn":"<sns_topic_arn>",
	"launch_event":"autoscaling:EC2_INSTANCE_LAUNCH",
	"launch_fail_event":"autoscaling:EC2_INSTANCE_LAUNCH_ERROR",
	"terminate_event":"autoscaling:EC2_INSTANCE_TERMINATE",
	"access_key":"<access_key>",
	"secret_key":"<secret_key>",
	"aws_region":"ap-southeast-1",
	"aws_region_endpoint":"ec2.ap-southeast-1.amazonaws.com"
}



mapping={

"akash_temp_as":{
	"pools":["pool_1","pool_2"],
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

}
