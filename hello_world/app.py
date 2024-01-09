import json
import os

import tempfile
import boto3
from yt_dlp import YoutubeDL
import random
import string


def random_string(length=32):
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def dlv(url: str) -> str:
    # Generate a random slug-friendly string
    randfile = f"{random_string()}.mp4"
    # Create a temporary file and write content into this file
    tmpfile = os.path.join("/tmp", randfile)
    ydl_opts = {
        "format": "best[ext=mp4]/best",  # prioritize mp4 format
        "outtmpl": tmpfile,  # set output to temp file
        "logtostderr": True,
        "continue": True,
        "no_overwrites": False,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        downloaded = os.path.basename(
            ydl.prepare_filename(ydl.extract_info(url, download=False))
        )

    # Now that the file is on disk, we can read and upload it to S3 in a streaming manner
    s3 = boto3.resource("s3")

    bucket_name = os.environ["MY_S3_BUCKET"] or "ytwas-s3bucket"

    with open(tmpfile, "rb") as data:
        s3.Bucket(bucket_name).put_object(Key=downloaded, Body=data)

    # Return the full path to the created S3 object
    s3_client = boto3.client("s3")
    url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": downloaded},
        ExpiresIn=300,
    )

    return url


def lambda_handler(event, context):
    body = json.loads(event["body"])
    video_url = body["video_url"] if "video_url" in body else None
    if not video_url:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "video_url is required"}),
        }
    upload_url = dlv(video_url)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"upload_url": upload_url}),
    }


if __name__ == "__main__":
    print(dlv("https://www.youtube.com/watch?v=TLwhqmf4Td4"))
