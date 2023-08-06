##### Logs-in and extract all instances data grouped by regions #####
#it needs config file $home\costngn\config.toml

import os, sys, time
from os.path import exists
from pathlib import Path
from itertools import count
from datetime import date, datetime
import copy
import pprint as pp
import boto3
import threading, concurrent.futures
import json
import toml
from botocore.config import Config
from termcolor import colored
#from ngn.aws.cred01 import * #now from config.toml
from ngn.config.classes import *
from ngn.aws.prices00 import *
#from resource00 import *

client_lock = threading.Lock()
inst_lock= threading.Lock()
#global company
#global my_ids


def conc_cli(region): # thread safely instantiate client
    with client_lock:
        return boto3.client('ec2',            
            region_name= region,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY)

def each_reg(region): #called with ThreadPoolExecutor
    #print('.',end=''); sys.stdout.flush()
    #get_res_data(region)
    #try:
    #print('Region:',region)
    #company='aws'
    #print(colored('.','blue'),end=''); sys.stdout.flush()
    ec2_cli = conc_cli(region) #call instantiate client in a function    
    """
    ec2_cli = boto3.client('ec2',            
        region_name= region,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY)
    """
    #start_time = time.time()
    instances=  ec2_cli.describe_instances()["Reservations"] 
    #duration = time.time() - start_time; print(f"It took {round(duration,4)} seconds")  
    region_has_inst=False      
    
    for instance in instances:
        region_has_inst=True
        #print('__________________________________________')
        print(colored('.','green'),end=''); sys.stdout.flush()            
        #Initiate Reg and Inst dictios
        inst=copy.deepcopy(InstBase)
        #pp.pprint(instance)
        
        try: #look for the name, if exists
            for tag in instance["Instances"][0]["Tags"]:
                if 'Name'in tag['Key']:
                    inst['name']=tag['Value']
        except: pass
        
        inst['id']=instance["Instances"][0]["InstanceId"] #
        inst['provider']=company.upper() #
        inst['region']= region #
        inst['status']=instance["Instances"][0]["State"]["Name"] #
        # normalize datetime created
        birth_obj = instance["Instances"][0]["LaunchTime"] #
        inst['birthday']= birth_obj.strftime(birth_format)
        inst['ipv4priv']=instance["Instances"][0]["PrivateIpAddress"] #           
        inst['ipv4pub']= instance["Instances"][0]["PublicIpAddress"] #           
        inst['type']= instance["Instances"][0]["InstanceType"] #
        inst['cpus']=instance["Instances"][0]["CpuOptions"]["CoreCount"] #
        inst['image']=instance["Instances"][0]["ImageId"] #
        inst['os']='Linux' if 'Linux' in instance["Instances"][0]["PlatformDetails"] else 'Windows'
        inst['avzone']=instance["Instances"][0]["Placement"]["AvailabilityZone"]
        inst['vpc_id']=instance["Instances"][0]["VpcId"]
        #Get memory size from _types        
        r_typ =ec2_cli.describe_instance_types(InstanceTypes=[inst['type']])
        inst['memory']=r_typ["InstanceTypes"][0]["MemoryInfo"]["SizeInMiB"]
        #Get nominal hourly price from AWS Pricing (call prices, which is free)
        region_code = inst['region']
        instance_type = inst['type']
        operating_system = inst['os']
        inst['ihprice']=get_ec2_instance_hourly_price(
            AWS_ACCESS_KEY,
            AWS_SECRET_KEY,
            region_code=region_code, 
            instance_type=instance_type, 
            operating_system=operating_system,                
        )

        if inst['ihprice']is not None:
            inst['imprice']=inst['ihprice']*744
        else:            
            inst['imprice']=0
            inst['ihprice']= 0
        
        #Store the instance id and data in lists
        with inst_lock:
            rep['instances'].append(inst)
        

# load all regions in list regions
def available_regions(service):
    regions = []
    client = boto3.client(service,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,        
        region_name= 'us-east-2', 
    )
    response = client.describe_regions()
    for item in response["Regions"]:
        #print(item["RegionName"])
        regions.append(item["RegionName"])
    return regions

######################################################################
##### Acceess to AWS and scan all available regions and instances #### 
#def aws_main(some_a:str):
def aws_main(nick, config_file):    
    #start_time = time.time()
    print("Scanning all instances (wait please)",end=' '); sys.stdout.flush()
    #print("Scanning all instances (wait please)")    
    #print('XXXX NICK FROM MAIN',nick)
    global company
    company='aws'
    #if ce_enable:
    #    print('Cost Explore Enabled')
    #print("Reading configuration file") #config.toml
    global AWS_ACCESS_KEY ; global AWS_SECRET_KEY; global AWS_AUTH_REGION 
    AWS_ACCESS_KEY=''; AWS_SECRET_KEY=''; AWS_AUTH_REGION=''
    #config_file=os.path.join(Path.home(), 'costngn','config.toml')    
    prof=toml.load(config_file)    
    #Load the account for the given nickname    
    acc=prof[nick]
    AWS_ACCESS_KEY= acc['ACCESS_KEY']
    AWS_SECRET_KEY=acc['SECRET_KEY']
    AWS_AUTH_REGION=acc['AUTH_REGION']
    #print('')   
    regions=[
    'eu-north-1',
    'ap-south-1',
    'eu-west-3',
    'eu-west-2',
    'eu-west-1',
    'ap-northeast-3',
    'ap-northeast-2',
    'ap-northeast-1',
    'sa-east-1',
    'ca-central-1',
    'ap-southeast-1',
    'ap-southeast-2',
    'eu-central-1',
    'us-east-1',
    'us-east-2',
    'us-west-1',
    'us-west-2']
    

    # Scan all of EC2 in each region
    cnt = 0
    my_ids=[]; insts={}
    global rep
    rep=copy.deepcopy(RepBase)     
    #for region in regions:
    #    each_reg(region)
    #duration = time.time() - start_time; print(f"It took {round(duration,4)} seconds")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(each_reg, regions)
        
        #rep['globalmprice']=ce_costs['global']
        #pp.pprint(ce_costs)
 
    #print('Instance information', end=' ')
    #if ce_enable:print('-charged query (because includes Cost Explorer data)')
    #else: print('-free query (because does not include Cost Explorer data)')

    #rep['month_cost']=round(rep['month_cost'],5)
    print('')
    #pp.pprint(rep)
    #duration = time.time() - start_time; print(f"It took {round(duration,4)} seconds")
    return(rep)

'''
# call function
if __name__ == "__main__":
    aws_main()
'''