### I. Introduction

Have you ever wanted to download a YouTube video to your iPhone, but both Youtube and iOS are just way too restrictive? Now you can, by a utilizing a combination of AWS Lambda (Python), S3 and glueing the user experience together with an easy to use Shortcut™

> **NOTE** This is intended for iOS users, as the final integration relies on Shortcuts™ but can be adapted be adapted to any platform which can make a POST request to an API endpoint

#### Getting Started

Pre-requisites: [AWS Account](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/prerequisites.html#prerequisites-sign-up), then install and configure the [SAM cli](http://https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

#### Quick Instructions for the impatient

```
❯ git clone https://github.com/robby-robby/ytwas
❯ cd ytwas
❯ sam build
❯ sam deploy
```

... then configure [the Shortcut](#shortcuts-the-glue-that-binds) with the API Gateway endpoint URL for the lambda function

### For the inquisitive, a bit about our lambda function

---

The python lambda is pretty simple, it just feeds a video_url json payload to the yt-dlp library...

```python
# ytwas/ytwas_function/app.py


# lambda handler expects a json object with a video_url key
def lambda_handler(event, context):
    ...
    video_url = body["video_url"]

```

---

[yt-dlp](https://github.com/yt-dlp/yt-dlp) is a fork of youtube-dl, and is most commonly used to download videos from YouTube using the command-line. It is also available as a Python library, which makes it a suitable fit for our python lambda function. This avoids the need to execute a shell command from within the lambda, which spawning a new process and psuedo terminal will be slower and most importantly less secure (not recommended)

In our lambda; using the [yt-dlp](https://github.com/yt-dlp/yt-dlp) python package, the given url is downloaded, then uploaded as an S3 object. The ydl_opts can be modified to suit your needs.

```python

def dlv(url: str) -> str:
  ...
  ydl_opts = {
    "format": "best[ext=mp4]/best",  # prioritize mp4 format
    ...
  }
  with YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
      downloaded = os.path.basename(
          ydl.prepare_filename(ydl.extract_info(url, download=False))
      )
```

Once the download and upload is complete, our bucket being private by default will require a pre-signed url to access the object. This is done by the following code:

```python
#The upload is given 5 minute time window to be accessible using a pre-signed url.
url = s3_client.generate_presigned_url(
    ClientMethod="get_object",
    Params={"Bucket": bucket_name, "Key": downloaded},
    ExpiresIn=300,#5 minutes, can be extending minutes*60
)
```

### II. Clone, Build, Deploy

Now that we have our Lambda function, we are ready to build and deploy! Once you have your AWS account ready, installed SAM CLI, and [configured your AWS credentials](https://docs.aws.amazon.com/general/latest/gr/aws-security-credentials.html)

---

#### Step 1. Clone the [**robby-robby/ytwas**](https://github.com/robby-robby/ytwas) repo if you already haven't:

```bash
git clone https://github.com/robby-robby/ytwas
```

```bash
cd ytwas
```

Then run the following to build the SAM application:

#### Step 2. Build the SAM application

```bash
❯ sam build
```

Example output of successful build:

```sh
❯ sam build
Building codeuri: /Users/robby-robby/ytwas/ytwas_function runtime: python3.11 metadata: {} architecture: x86_64 functions: YtwasFunction
 Running PythonPipBuilder:ResolveDependencies
 Running PythonPipBuilder:CopySource

Build Succeeded

Built Artifacts  : .aws-sam/build
Built Template   : .aws-sam/build/template.yaml

```

#### Step 3. Deploy the SAM application

```bash
sam deploy
```

A successful deployment will end with _outputs_ which look like this:

```sh
...
Key                 YtwasApi
Description         API Gateway endpoint URL for Prod stage for ytwas function
Value               https://xxxyyyzzzz.execute-api.us-east-2.amazonaws.com/Prod/convert/
...
```

From here copy the value url, it will be used in the **Shortcut** later

> **TROUBLESHOOTING** If there are any issues with the deployment, like a `FAILED` you can try to deploy again. If it is in a `ROLLBACK_COMPLETE` state, you can delete the stack with `sam delete` and try again.

### Shortcuts the glue that binds

[Download this Apple Shortcut](https://www.icloud.com/shortcuts/1c0b540c829044d48cfcff6894cd6811)

Find the Get Contents of URL action, and paste the url from the **outputs** of the `sam deploy` command into the URL field.

To refresh your memory, the URL would have looked something like this: `https://xxxyyyzzzz.execute-api.us-east-2.amazonaws.com/Prod/convert/`

### Try it out!

Since this Shortcut interfaces directly with the share sheet, it will be available in iOS share sheet in Safari.

[Navigate to a Youtube video which isn't copyrighted](https://www.youtube.com/watch?v=BBgghnQF6E4) then tap share, find and click our Shortcut

After a minute or so, once the video is downloaded and uploaded to S3, Safari will open the pre-signed S3 object link and you will be able to download the video.

### Conclusion

The combination of these three tools can give you some powerful processing capability that just isn't available on iOS, by restriction but also by processing capabilities. You could very well do similar processing with different tools using the Shortcut-lambda workflow for the cost of pennies to host per month (thanks lambda free tier!) SAM cli makes deployments easy, reproducible and sharable. Shortcuts and AWS Lambda is a winning combination, and I will be building more in the future.

### Going Further

Often times I've wanted to share a Youtube video via iMessage, but clicking links is just too much to ask from my friends. On top of that, sometimes the embedded video player in iMessage is **spotty** (am I alone here?) I think the next step for this would be to add a GIF'ing feature either to the Lambda or to the Shortcut. Then automatically opening a ready set iMessage with the GIF attached for instant gratification.

Maybe there's more to accomplish beyond just Youtube videos for the lolz. What if an endpoint could trigger a web-scraper or a even an LLM. The key is offloading the processing to the cloud, and using Shortcuts to glue the user experience together.
