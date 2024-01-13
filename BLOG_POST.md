### I. Introduction

Have you ever wanted to download a YouTube video to your iPhone, but both the platform and iOS are way too restrictive? Now you can, by offloading the heavy lifting to AWS Lambda (Python) and S3. Then gluing it all together with an easy to use Siri shortcut.

Setup and deployment is simplified by using the [SAM cli](http://https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html), but before installing that; you'll need an [AWS Account](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/prerequisites.html#prerequisites-sign-up)

### II. Three-Step Deployment Made Easy with SAM CLI

Once you have your AWS account ready, installed SAM CLI, and [configured your AWS credentials](https://docs.aws.amazon.com/general/latest/gr/aws-security-credentials.html), you're ready to deploy the application.

Clone the [**robby-robby/ytwas**](https://github.com/robby-robby/ytwas) repo:

#### Step 1: Clone the repo

```bash
git clone https://github.com/robby-robby/ytwas
```

```bash
cd ytwas
```

#### Step 2: Build the SAM application

Then run the following to build the SAM application:

```bash
sam build
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
sam deploy --guided
```

> **NOTE** Prompts can be skipped with [⏎ Enter] except `YtwasFunction has no authentication. Is this okay? [y/N]:` which should be answered with `y`

A successful deployment will end with _outputs_ which look like this:

```sh
...
Key                 YtwasApi
Description         API Gateway endpoint URL for Prod stage for ytwas function
Value               https://908asa0d.execute-api.us-east-2.amazonaws.com/Prod/convert/
...
```

From here copy the value url, it will be used in the **Siri-Shortcut**

> **TROUBLESHOOTING** If there are any issues with the deployment, like a `FAILED` you can try to deploy again. If it is in a `ROLLBACK_COMPLETE` state, you can delete the stack with `sam delete` and try again.

III. Solution Architecture
A. Description of the Python Lambda
B. How the Lambda integrates with YouTube
C. Storing videos in the S3 Bucket and configuring it
D. Integrating the Siri Shortcut with the AWS Lambda function

IV. Simplified Management and Teardown
A. The ease of management with this SAM solution
B. Steps to remove the application with sam delete

V. Benefits and Use Cases
A. Cost-effectiveness of the AWS solution
B. Adaptability of the lambda script
C. Processing capabilities enhancing iOS iPhone utility

VI. Conclusion
A. Emphasis on the convenience and simplicity of the two-step process
B. Encouragement for readers to explore and modify the solution

VII. References
A. Links to relevant documentation and resources
B. GitHub link/code, if applicable.
