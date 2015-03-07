from flask import Flask, request
import requests
import json
from properties import *
from boto.regioninfo import *
from boto.ec2.connection import EC2Connection
from boto.ec2.instanceinfo import InstanceInfo

app = Flask(__name__)


@app.route("/scale", methods=['POST','GET'])
def scale():
	input_json=json.loads(request.get_data())
	event = json.loads(input_json["Message"])["Event"]
	instance_id=json.loads(input_json["Message"])["EC2InstanceId"]
	as_group_name =json.loads(input_json["Message"])["AutoScalingGroupName"]
	aws_region = RegionInfo(name=metadata["aws_region"], endpoint=metadata["aws_region_endpoint"])
	conn = EC2Connection(metadata["access_key"],metadata["secret_key"], region=aws_region)
	network_interface = conn.get_all_network_interfaces(filters={"attachment.instance-id":instance_id})
	if len(network_interface) == 0:
		ip_address = instance_id
	else:
		ip_address = network_interface[0].private_ip_address
	
	if event == metadata["launch_event"] :
		
		if _does_node_exist(ip_address):
			status, pool_names = _is_node_in_a_pool(ip_address)
			if status:
				_delete_member_from_pool(ip_address,pool_names)
			_delete_node(ip_address)
		if mapping.get(as_group_name): # This is done to check if the properties file has the associated scaling group name 
			_add_node(ip_address, as_group_name, instance_id)
			_add_member_to_pool(ip_address, as_group_name, instance_id)
			return "OK"
		else:
			return "AS GROUP Does not exist"
	elif event == metadata["terminate_event"] or metadata["launch_fail_event"]:
	
		if _does_node_exist(ip_address):
			status, pool_name = _is_node_in_a_pool(ip_address)
			if status:
				_delete_member_from_pool(ip_address,pool_name)
			_delete_node(ip_address)
		return "OK"
	else:
		return "Event Not Handled"
			

def _get_node_list():
	url=metadata["base_url"] + "node?ver=11.5.0"
	r = requests.get(url, headers=metadata["headers"],auth=(metadata["username"], metadata["password"]),verify=False)
	node_list = json.loads(r.text)["items"]
	return node_list
		
def _does_node_exist(ip_address):
	node_list = _get_node_list()
	for node in node_list:
		if node["address"] == ip_address or node.get("description") == ip_address:
			return True
	return False

def _is_node_in_a_pool(ip_address):
	url=metadata["base_url"] + "pool?expandSubcollections=true"
	r = requests.get(url, headers=metadata["headers"],auth=(metadata["username"], metadata["password"]),verify=False)
	pools = json.loads(r.text)["items"]
	pool_names = []
	for pool in pools:
		members = pool["membersReference"].get("items")
		if members is not None:
			for member in members:
				if member["address"] == ip_address or member.get("description") == ip_address:
					pool_names.append(pool["name"])
	if len(pool_names) == 0:
		return (False, None)
	else:
		return (True, pool_names)
			
def _delete_member_from_pool(ip_address,pool_names):
	for pool_name in pool_names:
		url=metadata["base_url"] + "pool/"+pool_name+"/members?ver=11.5.0"
		r = requests.get(url, headers=metadata["headers"],auth=(metadata["username"], metadata["password"]),verify=False)
		members = json.loads(r.text)["items"]
		for member in members:	
			if member["address"] == ip_address or member.get("description") == ip_address:
				self_link = member["selfLink"]
				split_url = self_link.split("/")
				part_url = split_url[len(split_url) -1]
				url = metadata["base_url"] + "pool/" + pool_name + "/members/" + part_url
				r = requests.delete(url, headers=metadata["headers"],auth=(metadata["username"], metadata["password"]),verify=False)
	
def _delete_node(ip_address):
	node_list=_get_node_list()
	for node in node_list:
		if node["address"] == ip_address or node.get("description") == ip_address:
			self_link = node["selfLink"]
			split_url = self_link.split("/")
			part_url = split_url[len(split_url) -1]
			url = metadata["base_url"] +"node/" + part_url
			r = requests.delete(url, headers=metadata["headers"],auth=(metadata["username"], metadata["password"]),verify=False)
		
def _add_node(ip_address, as_group_name, instance_id):
	
	data={"name":ip_address,"partition":mapping[as_group_name]["node_attributes"]["partition"], "address":ip_address, "connectionLimit":mapping[as_group_name]["node_attributes"]["connectionLimit"], "dynamicRatio":mapping[as_group_name]["node_attributes"]["dynamicRatio"], "logging":mapping[as_group_name]["node_attributes"]["logging"], "monitor":mapping[as_group_name]["node_attributes"]["monitor"], "rateLimit":mapping[as_group_name]["node_attributes"]["rateLimit"], "ratio":mapping[as_group_name]["node_attributes"]["ratio"],"description":instance_id}
	url=metadata["base_url"] + "node?ver=11.5.0"
	r = requests.post(url, data=json.dumps(data), headers=metadata["headers"],auth=(metadata["username"], metadata["password"]),verify=False)
	
def _add_member_to_pool(ip_address, as_group_name, instance_id):
	data={"name":ip_address+":"+mapping[as_group_name]["node_attributes"]["port"], "description":instance_id}
	for pool in mapping[as_group_name]["pools"]:
		url=metadata["base_url"] + "pool/" + pool+"/members?ver=11.5.0"
		r = requests.post(url, data=json.dumps(data), headers=metadata["headers"],auth=(metadata["username"], metadata["password"]),verify=False)	

@app.route("/")
def hello():
	return "OK"

if __name__ == "__main__":
	app.run(host="0.0.0.0")
