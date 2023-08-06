import argparse
import os

from popcorn import __version__
from popcorn.popcornS3 import Popcorn


def upload_file(args):
    popcorn = Popcorn()
    popcorn.upload(args)


def download_file(args):
    popcorn = Popcorn()
    popcorn.download(args)


def list(args):
    popcorn = Popcorn()
    popcorn.list_files(args)


def subscribe(args):
    popcorn = Popcorn()
    popcorn.subscribe(args)


def create_project(args):
    popcorn = Popcorn()
    popcorn.create_project(args)


def delete_file(args):
    popcorn = Popcorn()
    popcorn.delete_file(args)


def main():
    parser = argparse.ArgumentParser(
        prog="popcorn",
        description="A command line tool to upload .nc files to the Polarplot dedicated S3 bucket",
        epilog="Copyright: D-ICE ENGINEERING",
    )

    parser.add_argument(
        "-v", "--version", action="store_true", help="Show version and exit"
    )

    # Add subparsers
    subparsers = parser.add_subparsers(
        title="sub-commands", help="available sub-commands"
    )
    subscribe_parser = subparsers.add_parser(
        "subscribe",
        help="Command to subscribe an email address to the bucket notifications",
    )
    subscribe_parser.add_argument(
        "--email",
        type=str,
        help="The email address to use to subscribe to this bucket notification service",
    )
    subscribe_parser.add_argument(
        "--remove", type=str, help="Remove the subscription of this email address"
    )
    subscribe_parser.add_argument(
        "--list", action="store_true", help="List every active subscription emails"
    )
    subscribe_parser.set_defaults(func=subscribe)

    # Sub-parser for the list command
    list_parser = subparsers.add_parser("list", help="List all projects archives")
    list_parser.add_argument(
        "--project", type=str, help="Ask a list for this specific project code"
    )
    list_parser.set_defaults(func=list)

    # Sub-parser for the upload command
    upload_parser = subparsers.add_parser("upload", help="Upload a file to the bucket")
    upload_parser.add_argument(
        "--project", type=str, required=True, help="Project code"
    )
    upload_parser.add_argument(
        "--file-description",
        type=str,
        required=True,
        help="Description of the file being uploaded",
    )
    upload_parser.add_argument(
        "--client",
        type=str,
        default="",
        help="The project client. Required if project does not exist.",
    )
    upload_parser.add_argument(
        "--project-description",
        type=str,
        default="",
        help="The project one sentence description. Required if project does not exist.",
    )
    upload_parser.add_argument("file", type=str, help="File to upload")
    upload_parser.set_defaults(func=upload_file)

    # Sub-parser for the download command
    download_parser = subparsers.add_parser(
        "download", help="Download a file from the bucket"
    )
    download_parser.add_argument("hash", type=str, help="Hash of the file to download")
    download_parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=os.getcwd(),
        help="Output directory for downloaded file",
    )
    download_parser.set_defaults(func=download_file)

    # Sub-parser for the create_project command
    create_project_parser = subparsers.add_parser(
        "create_project", help="Create a new project"
    )
    create_project_parser.add_argument("project", type=str, help="project name")
    create_project_parser.add_argument(
        "--client", type=str, required=True, help="client name", default=""
    )
    create_project_parser.add_argument(
        "--project-description",
        required=True,
        type=str,
        help="project description",
        default="",
    )
    create_project_parser.set_defaults(func=create_project)

    # Sub-parser for the create_project command
    delete_file_parser = subparsers.add_parser(
        "delete", help="Delete a file from the bucket and its metadata"
    )
    delete_file_parser.add_argument(
        "file_hash", type=str, help="The hash of the file to delete"
    )
    delete_file_parser.set_defaults(func=delete_file)

    args = parser.parse_args()
    print(args)

    if args.version:
        print(__version__)
        exit(1)

    func = None
    try:
        func = args.func
    except AttributeError:
        # Necessary when popcorn is called without any arguments to avoid AttributeError
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()
