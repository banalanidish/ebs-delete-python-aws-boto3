
import boto3
import botocore

# Set the global variables
globalVars  = {}
globalVars['Owner']                 = "ezest"
globalVars['Environment']           = "dev"
globalVars['REGION_NAME']           = "us-east-1"
globalVars['tagName']               = "test-Serverless-EBS-volume-remove"
globalVars['findNeedle']            = "Name"
globalVars['tagsToExclude']         = "Do-Not-Delete"

ec2       = boto3.resource('ec2', region_name = globalVars['REGION_NAME'] )

def lambda_handler(event, context):

    deletedVolumes=[]

    # Get all the volumes in the region
    for vol in ec2.volumes.all():
         if  vol.state=='available' :

            # Check for Tags
            if vol.tags is None:
                vid=vol.id
                v=ec2.Volume(vol.id)
               
                
                v.delete()
                
                

                deletedVolumes.append({'VolumeId': vol.id,'Status':'Delete Initiated'})
                

                continue

            # Find Value for Tag with Key as "Name"
            for tag in vol.tags:
                if tag['Key'] == globalVars['findNeedle']:
                  value=tag['Value']
                  if value != globalVars['tagsToExclude'] and vol.state == 'available' :
                    vid = vol.id
                    v = ec2.Volume(vol.id)
                    snapshot=v.create_snapshot()
                    
        
                    # Add volume name to snapshot for easier identification
                    snapshot.create_tags(Tags=[{'Key': 'Name','Value': value}])
                    #while snapshot.status != completed
                    #wait for 5 sec 
                    
                    
                     
                    
                    
                    
                    
                    
                    v.delete()
                    
                    deletedVolumes.append( {'VolumeId': vol.id,'Status':'Delete Initiated'} )
                    
                    
    
    
    # If no Volumes are deleted, to return consistent json output
    if not deletedVolumes:
        deletedVolumes.append({'VolumeId':None,'Status':None})

    # Return the list of status of the snapshots triggered by lambda as list
    return deletedVolumes
