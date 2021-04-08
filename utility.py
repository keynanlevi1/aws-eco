class Utility:

    @staticmethod
    def map_department_to_account (account_number):

        if account_number in ("379959622371", "267564311969", "759786165482", "771250916586"):
            return "CB"
        elif account_number in ("656509302511"):
            return "Operation"
        elif account_number in ("359856697693", "544428519067", "425154196092", "238450497947", "185449903594", "092796063756"):
            return "SAST"        
        elif account_number in ("983555762431", "148244689188"):
            return "AST Integration"
        elif account_number in ("881053136306"):
            return "Architecture"
        elif account_number in ("666740670058", "006765415138"):
            return "SCA"
        elif account_number in ("941355383184","263675485306"):
            return "AST"
        elif account_number in ("866472756642"):
            return "IAST"
        elif account_number in ("002023477301","098770948573","844024982327","074002600390","185216882498","715799477975","748129348851","938742211667","457489196639","354891787287"):
             return "CxGo"
        else:
            return "Other"


    @staticmethod
    def map_account_name_to_account_number (account_number):
        if account_number == "379959622371":
            return "CodeBashingSharedSvc"
        elif account_number == "941355383184":
            return "Cx-Aws-Ast-Dev"
        elif account_number == "267564311969":
            return "CxAwsCodeBashing"
        elif account_number == "759786165482":
            return "CxAwsCodeBashingDevelopment"
        elif account_number == "771250916586":
            return "CxAwsCodeBashingStaging"
        elif account_number == "881053136306":
            return "CxAwsDataCollectionRnD" 
        elif account_number == "656509302511":
            return "CxAwsDevOps"       
        elif account_number == "666740670058":
            return "CxAWSLumoDev"
        elif account_number == "006765415138":
            return "CxAWSLumoPPE"
        elif account_number == "148244689188":
            return "CxAwsMandODev"
        elif account_number == "983555762431":
            return "cxflowci"
        elif account_number == "263675485306":
            return "CxAST-TS"        
        elif account_number == "359856697693":
            return "CxSastAccessControlDev"        
        elif account_number == "092796063756":
            return "CxSastAccessControlProductionBeta"        
        elif account_number == "544428519067":
            return "CxSastAccessControlSharedServices"
        elif account_number == "425154196092":
            return "CxSastAccessControlStaging"
        elif account_number == "238450497947":
            return "CxSastDev"
        elif account_number == "185449903594":
            return "CxSastDevTeam17"   
        elif account_number == "866472756642":
            return "CxAWSIastDev"                 
        elif account_number == "002023477301":
            return "MCSSsa"
        elif account_number == "098770948573":
            return "MCSPPE"
        elif account_number == "844024982327":
            return "MCSPPEReplica"
        elif account_number == "074002600390":
            return "MCSSandbox"
        elif account_number == "185216882498":
            return "MCSProdReplica"
        elif account_number == "715799477975":
            return "MCSDev"
        elif account_number == "748129348851":
            return "MCSFeatureOne"
        elif account_number == "938742211667":
            return "MCSFeatureTwo"
        elif account_number == "457489196639":
            return "MCSFeatureThree"
        elif account_number == "354891787287":
            return "MCSHSBCReplica"              
        else:
            return "Other"

    @staticmethod
    def get_service_namespace(service):
        
        dict = {    
            'AmazonCloudWatch':'AWS/Logs',
            'Tax':'Tax',
            'Amazon API Gateway':'AWS/ApiGateway',
            'AppStream 2.0':'AWS/AppStream',
            'AWS AppSync':'AWS/AppSync',
            'Amazon Athena':'AWS/Athena',
            'AWS Billing and Cost Management':'AWS/Billing',
            'ACM Private CA':'AWS/ACMPrivateCA',
            'AWS Chatbot':'AWS/Chatbot',
            'Amazon CloudFront':'AWS/CloudFront',
            'AWS CloudHSM':'AWS/CloudHSM',
            'Amazon CloudSearch':'AWS/CloudSearch',
            'Amazon CloudWatch Logs':'AWS/Logs',            
            'AWS CodeBuild':'AWS/CodeBuild',
            'Amazon CodeGuru Profiler':'AWS/CodeGuruProfiler',
            'Amazon Cognito':'AWS/Cognito',
            'Amazon Connect':'AWS/Connect',
            'AWS DataSync':'AWS/DataSync',
            'AWS Database Migration Service':'AWS/DMS',
            'AWS Direct Connect':'AWS/DX',
            'Amazon DocumentDB':'AWS/DocDB',
            'Amazon DynamoDB':'AWS/DynamoDB',
            'Amazon EC2':'AWS/EC2',
            'Amazon EC2 Elastic Graphics':'AWS/ElasticGPUs',
            'Amazon EC2 Spot Fleet':'AWS/EC2Spot',
            'Amazon EC2 Auto Scaling':'AWS/AutoScaling',
            'AWS Elastic Beanstalk':'AWS/ElasticBeanstalk',
            'Amazon Elastic Block Store':'AWS/EBS',
            'Amazon Elastic Container Service':'AWS/ECS',
            'Amazon Elastic File System':'AWS/EFS',
            'Amazon Elastic Inference':'AWS/ElasticInference',
            'Elastic Load Balancing':'AWS/ApplicationELB',
            'Elastic Load Balancing':'AWS/ELB',
            'Elastic Load Balancing':'AWS/NetworkELB',
            'Amazon Elastic Transcoder':'AWS/ElasticTranscoder',
            'Amazon ElastiCache for Memcached':'AWS/ElastiCache',
            'Amazon ElastiCache for Redis':'AWS/ElastiCache',
            'Amazon Elasticsearch Service':'AWS/ES',
            'Amazon EMR':'AWS/ElasticMapReduce',
            'AWS Elemental MediaConnect':'AWS/MediaConnect',
            'AWS Elemental MediaConvert':'AWS/MediaConvert',
            'AWS Elemental MediaPackage':'AWS/MediaPackage',
            'AWS Elemental MediaStore':'AWS/MediaStore',
            'AWS Elemental MediaTailor':'AWS/MediaTailor',
            'Amazon EventBridge':'AWS/Events',
            'Amazon FSx for Lustre':'AWS/FSx',
            'Amazon FSx for Windows File Server':'AWS/FSx',
            'Amazon GameLift':'AWS/GameLift',
            'AWS Glue':'AWS/Glue',
            'AWS Ground Station':'AWS/GroundStation',
            'Amazon Inspector':'AWS/Inspector',
            'Amazon Interactive Video Service (IVS)':'AWS/IVS',
            'AWS IoT':'AWS/IoT',
            'AWS IoT Analytics':'AWS/IoTAnalytics',
            'AWS IoT SiteWise':'AWS/IoTSiteWise',
            'AWS IoT Things Graph':'AWS/ThingsGraph',
            'AWS Key Management Service':'AWS/KMS',
            'Amazon Keyspaces (for Apache Cassandra)':'AWS/Cassandra',
            'Amazon Kinesis Data Analytics':'AWS/KinesisAnalytics',
            'Amazon Kinesis Data Firehose':'AWS/Firehose',
            'Amazon Kinesis Data Streams':'AWS/Kinesis',
            'Amazon Kinesis Video Streams':'AWS/KinesisVideo',
            'AWS Lambda':'AWS/Lambda',
            'Amazon Lex':'AWS/Lex',
            'Amazon Machine Learning':'AWS/ML',
            'Amazon Managed Streaming for Apache Kafka':'AWS/Kafka',
            'Amazon MQ':'AWS/AmazonMQ',
            'Amazon Neptune':'AWS/Neptune',
            'AWS OpsWorks':'AWS/OpsWorks',
            'Amazon Polly':'AWS/Polly',
            'Amazon QLDB':'AWS/QLDB',
            'Amazon Redshift':'AWS/Redshift',
            'Amazon Relational Database Service':'AWS/RDS',
            'AWS RoboMaker':'AWS/Robomaker',
            'Amazon Route 53':'AWS/Route53',
            'Amazon SageMaker':'AWS/SageMaker',
            'AWS SDK Metrics for Enterprise Support':'AWS/SDKMetrics',
            'AWS Service Catalog':'AWS/ServiceCatalog',
            'AWS Shield Advanced':'AWS/DDoSProtection',
            'Amazon Simple Email Service':'AWS/SES',
            'Amazon Simple Notification Service':'AWS/SNS',
            'Amazon Simple Queue Service':'AWS/SQS',
            'Amazon Simple Storage Service':'AWS/S3',
            'Amazon Simple Workflow Service':'AWS/SWF',
            'AWS Step Functions':'AWS/States',
            'AWS Storage Gateway':'AWS/StorageGateway',
            'AWS Systems Manager Run Command':'AWS/SSM-RunCommand',
            'Amazon Textract':'AWS/Textract',
            'AWS Transfer for SFTP':'AWS/Transfer',
            'Amazon Translate':'AWS/Translate',
            'AWS Trusted Advisor':'AWS/TrustedAdvisor',
            'Amazon VPC':'AWS/NATGateway',
            'Amazon VPC':'AWS/TransitGateway',
            'Amazon VPC':'AWS/VPN',
            'AWS WAF':'WAF',
            'Amazon WorkMail':'AWS/WorkMail',
            'Amazon WorkSpaces':'AWS/WorkSpaces'
            }
        if service in dict:
            return dict[service]
        return 'Other'


