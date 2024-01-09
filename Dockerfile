FROM public.ecr.aws/lambda/python:3.11

# Copy function code
COPY hello_world/* ${LAMBDA_TASK_ROOT}

# May need ffpemg install?
# COPY ffmpeg-5.1.1-amd64-static /usr/local/bin/ffmpeg
# RUN chmod 777 -R /usr/local/bin/ffmpeg

RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.lambda_handler" ]
