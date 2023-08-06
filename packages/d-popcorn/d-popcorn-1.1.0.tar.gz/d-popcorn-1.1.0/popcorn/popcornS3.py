import hashlib
import json
import os
import re
import boto3


MANDATORY_REGION = "us-east-1"
AWS_ARN_PATTERN = (
    R"^arn:(?P<Partition>[^:\n]*):"
    R"(?P<Service>[^:\n]*):"
    R"(?P<Region>[^:\n]*):"
    R"(?P<AccountID>[^:\n]*):"
    R"(?P<Ignore>(?P<ResourceType>[^:\/\n]*)[:\/])?(?P<Resource>.*)$"
)
__dice_projects_prefixes__ = [
    "SCE",
    "RDX",
    "RDI",
    "RDS",
    "OCX",
    "SQD",
    "RBK",
    "SHY",
    "THX",
    "FG",
]


class Popcorn:
    def __init__(self):
        self._bucket_name = "polarplot-data"
        self.meta_file = "popcorn_meta.json"
        self._session = boto3.session.Session(region_name=MANDATORY_REGION)
        self.s3 = boto3.resource("s3")
        self._bucket = self.s3.Bucket(self._bucket_name)

    def _get_normalized_sns_topic_name(self):
        return f"{self._bucket_name}-sns-topic"

    def get_bucket_topic(self):
        sns = self._session.resource("sns")
        topic_name = self._get_normalized_sns_topic_name()

        bucket_topic = None
        for topic in sns.topics.all():
            if re.match(AWS_ARN_PATTERN, topic.arn)["Resource"] == topic_name:
                bucket_topic = topic
                break

        if bucket_topic is None:
            # No topic associated with this bucket, creating it with proper name
            print(f"No topic with name {topic_name} were found. We just created it...")

            bucket_topic = sns.create_topic(Name=topic_name)

            # https://stackoverflow.com/questions/49961491/using-boto3-to-send-s3-put-requests-to-sns

            # Set topic policy to accept s3 events
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Client.set_topic_attributes
            sns_topic_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "sns:Publish",
                        "Resource": bucket_topic.arn,
                        "Condition": {
                            "ArnLike": {
                                "AWS:SourceArn": f"arn:aws:s3:*:*:{self._bucket_name}"
                            },
                        },
                    },
                ],
            }

            bucket_topic.set_attributes(
                AttributeName="Policy", AttributeValue=json.dumps(sns_topic_policy)
            )

            # Set notification config
            notification = self._bucket.Notification()

            notification.put(
                NotificationConfiguration={
                    "TopicConfigurations": [
                        {
                            "TopicArn": bucket_topic.arn,
                            "Events": [  # s3 Events we want to trig notification
                                "s3:ObjectCreated:*",
                                "s3:ObjectRemoved:*",
                                "s3:ObjectRestore:*",
                            ],
                        }
                    ]
                }
            )

        return bucket_topic

    def subscribe_to_bucket_notifications(self, email: str):
        # 1- on veut recuperer le topic associe a ce bucket
        bucket_topic = self.get_bucket_topic()

        # Getting subscriptions
        for subscription in bucket_topic.subscriptions.all():
            if subscription.arn == "PendingConfirmation":
                continue

            if subscription.attributes["Endpoint"] == email:
                return None

        subscription = bucket_topic.subscribe(Protocol="email", Endpoint=email)

        return subscription

    def list_subscriptions(self):
        bucket_topic = self.get_bucket_topic()

        subscriptions = []
        for subscription in bucket_topic.subscriptions.all():
            if subscription.arn == "PendingConfirmation":
                subscriptions.append("Pending Subscription")

            else:
                subscriptions.append(subscription.attributes["Endpoint"])

        return subscriptions

    def remove_subscription(self, email: str):
        bucket_topic = self.get_bucket_topic()

        subscription_to_delete = None
        for subscription in bucket_topic.subscriptions.all():
            if subscription.arn == "PendingConfirmation":
                continue

            if subscription.attributes["Endpoint"] == email:
                subscription_to_delete = subscription

        if subscription_to_delete is not None:
            subscription_to_delete.delete()
            print(f"This subscription is deleted")
        else:
            print(
                f"\t> Email address {email} was not subscribing to the bucket notifications"
            )

    def subscribe(self, args):
        if args.list:
            print("\nList of subscriptions:")
            for subscription_email in self.list_subscriptions():
                print(f"\t* {subscription_email}")

        if args.email:
            print(f"\nSubscribing to notifications with email address {args.email}")
            if self.subscribe_to_bucket_notifications(args.email) is not None:
                input(
                    f"\n\tConfirmation email sent to {args.email}."
                    f"\n\tPlease check your messages and follow the instructions."
                    f"(\n\tDon't forget to check your junk box"
                    f"\n\n\tPLEASE PROCEED RIGHT NOW! :-)"
                    f"\n\n\tPress Enter to continue..."
                )
            else:
                print(f"\t> {args.email} was already subscribing")

        if args.remove:
            print(f"\nRemoving email address {args.remove} from the subscriptions")
            self.remove_subscription(args.remove)

    def list_files(self, args):
        with self._bucket.Object(self.meta_file).get()["Body"] as f:
            file_content = f.read().decode("utf-8")
            meta_data = json.loads(file_content)
        if args.project:
            if args.project not in meta_data["projects"]:
                print(f"No such project: {args.project}")
                return
            project_metadata = meta_data["projects"][args.project]
            print(f"Project : {args.project}")
            print(f"Client : {project_metadata['client']}")
            print(f"Project Description: {project_metadata['project-description']}")

            file_metadata = {
                k: v
                for k, v in meta_data["files"].items()
                if v["project"] == args.project
            }
            for hash_key, file_data in file_metadata.items():
                print(f"\n\t File: {hash_key}")
                print(f"\t\t File Description: {file_data['file-description']}")

            # for hash_key, metadata_dict in meta_data.items():
            #     project_name = metadata_dict['project']
            #     if project_name not in new_metadata:
            #         new_metadata[project_name] = {}
            #     new_metadata[project_name][hash_key] = {
            #         'client': metadata_dict['client'],
            #         'file-description': metadata_dict['file-description'],
            #     }
            #     new_metadata[project_name]["project-description"] = metadata_dict['project-description']
            #
            # for project_key, metadata_dict in new_metadata.items():
            #     print("Project : {}".format(project_key))
            #     print(f"Project Description:               {metadata_dict['project-description']}")
            #     for hash_key, file_data in metadata_dict.items():
            #         if hash_key != "project-description":
            #             print(f"\n\t File: {hash_key}")
            #             print(f"\t\t Client:                          {file_data['client']}")
            #             print(f"\t\t File Description:                {file_data['file-description']}")
        else:
            for hash_key, file_data in meta_data["files"].items():
                print("File : {}".format(hash_key))
                print(f"\t Project:                         {file_data['project']}")
                project_data = meta_data["projects"][file_data["project"]]
                print(f"\t Client:                          {project_data['client']}")
                print(
                    f"\t Project Description:             {project_data['project-description']}"
                )
                print(
                    f"\t File Description:                {file_data['file-description']}"
                )
            return

    def get_file_hashes(self):
        hashes = []

        # get all objects with .nc extension in bucket
        objects = self._bucket.objects.all()
        files = [obj.key for obj in objects if obj.key.endswith(".nc")]

        # calculate hash for each file and add to hashes list
        for file in files:
            response = self._bucket.Object(file).get()
            hasher = hashlib.sha256()
            hasher.update(response["Body"].read())
            hashes.append(hasher.hexdigest())
        return hashes

    def _get_metadata(self):
        try:
            # with self._bucket.Object(self.meta_file).get() as f:
            #     metadata = json.loads(f.read().decode('utf-8'))
            #     print(metadata)
            #     return metadata
            response = self._bucket.Object(self.meta_file).get()
            existing_metadata = json.loads(response["Body"].read().decode("utf-8"))
            print(existing_metadata)
            return existing_metadata
        except Exception as e:
            print("here", e)
            return {"files": {}, "projects": {}}

    def _generate_hash(self, file):
        hasher = hashlib.sha256()
        with open(file, "rb") as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def upload(self, args):
        #####################
        #  HANDLE METADATA  #
        #####################
        # Get existing metadata
        metadata = self._get_metadata()
        # generate unique hash for file
        file_hash = self._generate_hash(args.file)
        # set polarplot link
        link = "http://polarplot.d-ice.net/polarplot/" + file_hash
        # get file name from path
        file_name = os.path.basename(args.file)
        # Build metadata tags dictionary for the file
        file_metadata_tags = {
            "project": args.project,
            "file-description": args.file_description,
        }
        # test if project prefix is valid (RDX, SCE etc...)
        pattern = "^(" + "|".join(__dice_projects_prefixes__) + ")[0-9]{3}$"
        if not bool(re.match(pattern, args.project)):
            raise RuntimeError(
                f"Projects names must have the following form: <prefix><number> where "
                f"prefix is in {__dice_projects_prefixes__} and "
                f"number is a 3-digit number referencing the project number."
                f"\nExample: SCE072"
            )

        if args.project not in metadata["projects"]:
            print("Adding project metadata to json")
            project_metadata_tags = {
                "client": args.client,
                "project-description": args.project_description,
            }
            metadata["projects"][args.project] = project_metadata_tags

        if file_hash not in metadata["files"]:
            print("Adding file metadata to json")
            metadata["files"][file_hash] = file_metadata_tags

        self._bucket.put_object(Body=json.dumps(metadata), Key=self.meta_file)
        print(f"Metadata for {file_name} added successfully.")
        #####################
        #    HANDLE FILE    #
        #####################
        # check if file with same hash already exists
        for f in self.get_file_hashes():
            if f == file_hash:
                print(
                    f"The file {file_name} already exists with the same hash {file_hash}."
                )
                print(f"You can visualize the uploaded data using this link: {link}")
                return

        # upload file to bucket with client and project metadata
        with open(args.file, "rb") as f:
            self._bucket.put_object(
                Body=f, Key=file_hash + ".nc", Metadata=file_metadata_tags
            )

        print(f"{file_name} uploaded successfully. File hash {file_hash} ")
        print(f"You can visualize the uploaded data using this link: {link}")

    def download(self, args):
        # retrieve metadata for file with hash
        metadata = self._get_metadata()
        nc_file = args.hash + ".nc"
        if not any(obj.key == nc_file for obj in self._bucket.objects.all()):
            # print(f"The file {key} does not exist in the bucket {bucket_name}.")
            print(f"No file with hash {args.hash} found.")
            print(self.list_files(args))
            return
        # Get the S3 object
        s3_object = self.s3.Object(self._bucket_name, nc_file)
        # Download the file from S3 to a local file
        local_file_path = str(
            os.path.join(args.output, os.path.basename(s3_object.key))
        )
        print(f"Downloading file to: {local_file_path}")
        s3_object.download_file(local_file_path)
        print("Download succeeded")
        return

    def create_project(self, args):
        pattern = "^(" + "|".join(__dice_projects_prefixes__) + ")[0-9]{3}$"
        if not bool(re.match(pattern, args.project)):
            raise RuntimeError(
                f"Projects names must have the following form: <prefix><number> where "
                f"prefix is in {__dice_projects_prefixes__} and "
                f"number is a 3-digit number referencing the project number."
                f"\nExample: SCE072"
            )

        project_metadata_tags = {
            "client": args.client,
            "project-description": args.project_description,
        }

        metadata = self._get_metadata()

        if args.project in metadata["projects"]:
            print(f"The project {args.project} already exists.")
            return

        metadata["projects"][args.project] = project_metadata_tags

        self._bucket.put_object(Body=json.dumps(metadata), Key=self.meta_file)
        print(f"Project {args.project} created successfully.")

    def delete_file(self, args):
        metadata = self._get_metadata()

        # Check if file hash exists in the metadata
        if args.file_hash not in self.get_file_hashes():
            print(f"No file found with the hash {args.file_hash}.")
            return

        try:
            self._bucket.Object(args.file_hash + ".nc").delete()
            print(f"File {args.file_hash} deleted successfully from the bucket.")
        except Exception as e:
            print(
                f"An error occurred while deleting the file from the bucket: {str(e)}"
            )
            return

        if args.file_hash in metadata["files"]:
            del metadata["files"][args.file_hash]
            self._bucket.put_object(Body=json.dumps(metadata), Key=self.meta_file)
            print("Metadata updated successfully.")
