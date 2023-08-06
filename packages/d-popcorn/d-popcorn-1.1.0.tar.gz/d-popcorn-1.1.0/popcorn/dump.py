from popcornS3 import *

# def upload(self, args):
#     # generate unique hash for file
#     file_hash = self._generate_hash(args.file)
#     # set polaplot link
#     link = "http://polarplot.d-ice.net/polarplot/" + file_hash
#     # get file name from path
#     file_name = os.path.basename(args.file)
#
#     # check if file with same hash already exists
#     for f in self.get_file_hashes():
#         if f == file_hash:
#             print(f"The file {file_name} already exists with the same hash {file_hash}.")
#             print(f"You can visualize the uploaded data using this link: {link}")
#             return
#
#     # TODO: tester si project est valide (RDX, SCE etc...)
#     pattern = "^(" + "|".join(__dice_projects_prefixes__) + ")[0-9]{3}$"
#     if not bool(re.match(pattern, args.project)):
#         raise RuntimeError(f"Projects names must have the following form: <prefix><number> where "
#                            f"prefix is in {__dice_projects_prefixes__} and "
#                            f"number is a 3-digit number referencing the project number."
#                            f"\nExample: SCE072")
#
#     # upload file to bucket with client and project metadata
#     metadata_tags = {'client': args.client,
#                      'project': args.project,
#                      'project-description': args.project_description,
#                      'file-description': args.file_description}
#     with open(args.file, 'rb') as f:
#         self._bucket.put_object(Body=f, Key=file_hash + '.nc', Metadata=metadata_tags)
#
#     # retrieve the existing metadata file
#     response = self._bucket.get_object(Key=self.meta_file)
#     existing_metadata = json.loads(response['Body'].read().decode('utf-8'))

#     # add the new metadata to the existing metadata
#     existing_metadata[file_hash] = metadata_tags
#
#     # write updated metadata file
#     self._bucket.put_object(Body=json.dumps(existing_metadata), Key=self.meta_file)
#     print(f"{file_name} uploaded successfully. File hash {file_hash} ")
#     print(f"You can visualize the uploaded data using this link: {link}")

"""


"""

#
# def upload(self, args):
#     # test if project prefix is valid (RDX, SCE etc...)
#     pattern = "^(" + "|".join(__dice_projects_prefixes__) + ")[0-9]{3}$"
#     if not bool(re.match(pattern, args.project)):
#         raise RuntimeError(f"Projects names must have the following form: <prefix><number> where "
#                            f"prefix is in {__dice_projects_prefixes__} and "
#                            f"number is a 3-digit number referencing the project number."
#                            f"\nExample: SCE072")
#     # Build metadata tags dictionary for the file
#     file_metadata_tags = {'project': args.project,
#                           'file-description': args.file_description}
#     project_metadata_tags = {'client': args.client,
#                              'project-description': args.project_description}
#
#     # generate unique hash for file
#     file_hash = self._generate_hash(args.file)
#     # set polaplot link
#     link = "http://polarplot.d-ice.net/polarplot/" + file_hash
#     # get file name from path
#     file_name = os.path.basename(args.file)
#     # Get existing metadata
#     metadata = self._get_metadata()
#
#     # check if file with same hash already exists
#     if file_hash in metadata['files']:
#         print(f"The file {file_name} already exists with the same hash {file_hash}.")
#         print(f"You can visualize the uploaded data using this link: {link}")
#         return
#
#     # upload file to bucket with client and project metadata
#     with open(args.file, 'rb') as f:
#         self._bucket.put_object(Body=f, Key=file_hash + '.nc', Metadata=file_metadata_tags)
#
#     # add file metadata to metadata file with hash as key
#     metadata['files'][file_hash] = file_metadata_tags
#     metadata['projects'][args.project] = project_metadata_tags
#
#     # write updated metadata file
#     self._bucket.put_object(Body=json.dumps(metadata), Key=self.meta_file)
#     print(f"{file_name} uploaded successfully. File hash {file_hash} ")
#     print(f"You can visualize the uploaded data using this link: {link}")

# def list_files(self, args):
#     with self._bucket.Object(self.meta_file).get()['Body'] as f:
#         file_content = f.read().decode('utf-8')
#         metadata = json.loads(file_content)
#
#     if args.project:
#         if args.project not in metadata['projects']:
#             print(f"No such project: {args.project}")
#             return
#
#         project_metadata = metadata['projects'][args.project]
#         print(f"Project : {args.project}")
#         print(f"Client : {project_metadata['client']}")
#         print(f"Project Description: {project_metadata['project-description']}")
#
#         file_metadata = {k: v for k, v in metadata['files'].items() if v['project'] == args.project}
#         for hash_key, file_data in file_metadata.items():
#             print(f"\n\t File: {hash_key}")
#             print(f"\t\t File Description: {file_data['file-description']}")
#
#     else:
#         for hash_key, file_data in metadata['files'].items():
#             print("File : {}".format(hash_key))
#             print(f"\t Project: {file_data['project']}")
#             project_data = metadata['projects'][file_data['project']]
#             print(f"\t Client: {project_data['client']}")
#             print(f"\t Project Description: {project_data['project-description']}")
#             print(f"\t File Description: {file_data['file-description']}")


class Args:
    def __init__(
        self,
        project=None,
        file_description=None,
        client=None,
        project_description=None,
        file=None,
        file_hash=None,
    ):
        self.project = project
        self.file_description = file_description
        self.client = client
        self.project_description = project_description
        self.file = file
        self.file_hash = file_hash


file_delete = "0b1fc55e1201876f4a3703a4f6f7e171939c68785f75efc68422fe57b9cd31f1"

popcorn = Popcorn()

# args = Args(project='SCE070', file_description='no_sail', client='beyond_the_sea',
#             project_description='', file='/home/oelbakouchi/Documents/polarsNC/polar_FPP_og.nc')
#
# popcorn.upload(args)

# list_args = Args(project='SCE070')
# popcorn.list_files(list_args)

# project_args = Args(project='SCE072', client='test', project_description='test')
# popcorn.create_project(project_args)

# delete_args = Args(file_hash=file_delete)
# popcorn.delete_file(delete_args)
