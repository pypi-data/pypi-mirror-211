import requests
import time
from tabulate import tabulate

class transportcb:
    def __init__(self, sourceip, destip, user, password):
        self.sourceip = sourceip
        self.destip = destip
        self.user = user
        self.password = password
        self.createdXdcrRef=False
        self.canMigrated=False
        self.migrateBucketList=[]
        self.checkClusterVersions()
        self.checkXdcrReference()
        self.filterMigratableBuckets()
        self.startMigration()
        self.printResults()


    def checkClusterVersions(self):
        urlfordestinaion = f"http://{self.destip}:8091/pools"
        urlforsource = f"http://{self.sourceip}:8091/pools"
        sourceversion = requests.get(url=urlforsource, auth =(self.user,self.password))
        destinationversion = requests.get(url=urlfordestinaion, auth =(self.user,self.password))
        sourceresult = int(str(sourceversion.json()['implementationVersion']).split('.')[0])
        destinationresult = int(str(destinationversion.json()['implementationVersion']).split('.')[0])
        print("[INFO] : Checking cluster versions.")
        if destinationresult >= sourceresult:
            self.equalOrGreaterVersion = True
        else:
            self.equalOrGreaterVersion = False

    def checkXdcrReference(self):
        sourceClusterXdcrUrl=f'''http://{self.sourceip}:8091/pools/default/remoteClusters'''
        sourceClusterXdcrData=requests.get(url=sourceClusterXdcrUrl,auth=(self.user,self.password))
        sourceClusterJsonXdcrData=sourceClusterXdcrData.json()
        destinationIp=self.destip
        if len(sourceClusterJsonXdcrData)> 0:
            for singleXdcrRef in sourceClusterJsonXdcrData:
                referenceXdcrIp=str(singleXdcrRef.get('hostname')).split(':')[0]
                if destinationIp==referenceXdcrIp:
                    print("[ERROR]: XDCR reference found. Program will create one.")
                    self.xdcrReferenceExists=True
                    break
                else:
                    print("[INFO]: Program will create one XDCR")
                    self.xdcrReferenceExists=False
        else:
            print("[INFO] : No XDCR reference found. Program will create one.")
            self.xdcrReferenceExists=False


    def filterMigratableBuckets(self):
        # collect buckets from source cluster.
        destinationBucket=[]
        try:
            sourceBucketUrl=f'''http://{self.sourceip}:8091/pools/default/buckets'''
            destinationBucketUrl=f'''http://{self.destip}:8091/pools/default/buckets'''
            sourceBucketData=requests.get(url=sourceBucketUrl,auth=(self.user,self.password))
            destinationBucketData=requests.get(url=destinationBucketUrl,auth=(self.user,self.password))
            destinationBucketJsonList=destinationBucketData.json()
            sourceBucketJsonList=sourceBucketData.json()
            for singleDestinationBucket in destinationBucketJsonList:
                destinationBucket.append(singleDestinationBucket.get('name'))
            for singleBucket in sourceBucketJsonList:
                sourceBucketName=singleBucket.get('name')
                sourceBucketType=singleBucket.get('bucketType')
                sourceBucketReplica=singleBucket.get('numReplica')
                sourceBucketLimits=singleBucket.get('quota')
                sourceBucketMemory=sourceBucketLimits.get('rawRAM')
                if sourceBucketName in destinationBucket:
                    print(f'''[INFO]: In destination cluster {sourceBucketName} exists.''')
                else:
                    singleBucketModel={
                        "bucketName": sourceBucketName,
                        "bucketMemory": sourceBucketMemory,
                        "bucketType" :sourceBucketType,
                        "bucketReplica": sourceBucketReplica
                    }
                    self.migrateBucketList.append(singleBucketModel)
        except Exception as bucketCollectException:
            print(bucketCollectException)

    def startMigration(self):
        if self.equalOrGreaterVersion==True and self.xdcrReferenceExists==False:
            print('[INFO] : All conditions are met. Program will create XDCR reference and create replication for each bucket.')
            # buraya referansı olusturalım.
            destinationNewIp = self.destip + ':8091'
            referenceRecord = {
                'name': 'transferc_generated_xdcr',
                'hostname': destinationNewIp,
                'username': self.user,
                "password": self.password
            }
            if self.xdcrReferenceExists==False:
                sourceReferenceUrl = f"http://{self.sourceip}:8091/pools/default/remoteClusters"
                createNewReference = requests.post(url=sourceReferenceUrl, data=referenceRecord, auth=(self.user, self.password))
                if createNewReference.status_code==200:
                    print('[INFO] : Created XDCR Reference.')
                    self.createdXdcrRef=True
                    for singleBucket in self.migrateBucketList:
                        createCouchbaseBucketUrl=f'''http://{self.destip}:8091/pools/default/buckets'''
                        payloadData={
                            "name": singleBucket.get('bucketName'),
                            "replicaNumber":singleBucket.get('bucketReplica'),
                            "bucketType": singleBucket.get('bucketType'),
                            "ramQuota":int(singleBucket.get('bucketMemory')/1024/1024)
                        }
                        createBucketDestination=requests.post(url=createCouchbaseBucketUrl,auth=(self.user,self.password),data=payloadData)
                        if createBucketDestination.status_code==202:
                            print(f'''[INFO]: {singleBucket.get('bucketName')} Created.''')
                            replRecord = {
                                'fromBucket': singleBucket.get('bucketName'),
                                'toCluster': referenceRecord.get('name'),
                                'toBucket': singleBucket.get('bucketName'),
                                "replicationType": 'continuous'
                            }
                            time.sleep(30)
                            replicationBucketUrl = f"http://{self.sourceip}:8091/controller/createReplication"
                            createNewReplicationForBucket = requests.post(url=replicationBucketUrl, data=replRecord, auth=(self.user, self.password))
                            if createNewReplicationForBucket.status_code==200:
                                print(f"[INFO] : Added reference for bucket {replRecord.get('fromBucket')}")
                            else:
                                print(f"[INFO] : Failed to add reference for bucket {replRecord.get('fromBucket')}")
                                print(createNewReplicationForBucket.status_code)
                        else:
                            print(f'''{singleBucket.get('bucketName')} Failed.''')
            else:
                print("[ERROR]: XDCR reference exists.")

    def printResults(self):
        versionControlCheck= "✓" if self.equalOrGreaterVersion else "✗"
        referenceCreateCheck= "✓" if self.createdXdcrRef else "✗"
        xdcrReferenceCheck= "✗" if self.xdcrReferenceExists else "✓"
        tableFomat=[
            ["Version Control Check Between Source and Destination",versionControlCheck,"Destination cluster version can not be smaller than source cluster version"],
            ["XDCR Reference Check",xdcrReferenceCheck,"Program is assuming there is no XDCR reference for the new destination."],
            ["Create XDCR Reference",referenceCreateCheck,"Reference for XDCR created."],
        ]
        headers=['Issue','Result','Recommendation']
        resultTable=tabulate(tableFomat,headers,tablefmt="grid")
        print(resultTable)