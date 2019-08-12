from pathlib import Path
import boto3
import click


@click.option('--profile', default=None, help="Specify AWS profile name")
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucketname')
@click.command()
def upload_file(profile, pathname, bucketname):
    """Upload file to S3 bucket."""

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(**session_cfg)
    s3 = session.resource('s3')

    bucket = s3.Bucket(bucketname)
    if bucket:
        path = Path(pathname).expanduser().resolve()
        bucket.upload_file(str(path), str(path.name))
    else:
        print("error")

if __name__ == 'main':
    upload_file()
