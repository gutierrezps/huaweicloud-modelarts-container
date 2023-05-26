# HUAWEI CLOUD ModelArts Container

This repository contains a simple example of how to deploy an image
classification Tensorflow/Keras model as a Container in
[HUAWEI CLOUD ModelArts][modelarts].

**DISCLAIMER**: this is only a demonstration code, for learning purposes only.
This example is not production-grade. See
"[How to not deploy Keras/TensorFlow models][how-to-not-deploy]" published by
Christian Freischlag in Towards Data Science for more information.

## Requirements

- [HUAWEI CLOUD account][hwc-account]
- [HUAWEI CLOUD SWR organization][swr-org] in the same region you wish to
  deploy your model in ModelArts
- Docker - <https://docs.docker.com/desktop/>
- Miniconda - <https://docs.conda.io/en/latest/miniconda.html>

## Installation (Python)

1. Install Miniconda if not already installed;
2. Create a Conda virtual environment (e.g. `modelarts`) with Python 3.10:
   `conda create -n modelarts python=3.10 -y`
3. Activate the environment and install the requirements inside it:
   `conda activate modelarts; pip install -r requirements.txt`

## Model development

Train your model in [ModelArts DevEnvion notebook][devenviron]. This particular
example is based on the "[Image Classification from Scratch][keras-tutorial]"
tutorial from Keras.

After your model is trained, save its configuration and weights using the
following code:

```python
#  model JSON
model_config = model.to_json()
with open('model_config.json', 'w') as fp:
   fp.write(model_config)

# model weights
model.save_weights('model_weights')
```

After that, you should have a file named `model_config.json` which holds the
model configuration, and some files named `model_weights.index` and
`model_weights.data...`. Get all those files and place it into the `models`
folder.

## Deploy in ModelArts

1. Build Docker image: `docker build -t {image name}:{image version} .`
2. Test Docker image locally:
   `docker run -it -p 8080:8080 {image name}:{image version}`
3. Go to the HUAWEI CLOUD SWR Console in the same region you wish to deploy
   your model in ModelArts, obtain the login command and run it;
4. Tag the local image:
   `docker tag {image name}:{image version} swr.{region}.myhuaweicloud.com/{SWR organization}/{image name}:{image version}`
5. Push the image to SWR:
   `docker push swr.{region}.myhuaweicloud.com/{SWR organization}/{image name}:{image version}`
6. [Create an AI Application using the SWR image][ai-app-container]
7. [Deploy the AI Application as a Real-Time Service][real-time-svc]

Using `myapp` as image name, `0.0.1` as image version, `region` as
`sa-brazil-1` (LA-Sao Paulo1 Region), and `myorg` as SWR organization,
the commands above would become:

```plain
docker build -t myapp:0.0.1 .

docker run -it -p 8080:8080 myapp:0.0.1

docker tag myapp:0.0.1 swr.sa-brazil-1.myhuaweicloud.com/myorg/myapp:0.0.1

docker push swr.sa-brazil-1.myhuaweicloud.com/myorg/myapp:0.0.1
```

## References

- Creating a Custom Image and Using It to Create an AI Application:
  <https://support.huaweicloud.com/intl/en-us/docker-modelarts/modelarts_23_0270.html>
- Flask Quickstart: <https://flask.palletsprojects.com/en/2.3.x/quickstart/>

[modelarts]: <https://www.huaweicloud.com/intl/en-us/product/modelarts.html>
[how-to-not-deploy]: <https://towardsdatascience.com/how-to-not-deploy-keras-tensorflow-models-4fa60b487682>
[hwc-account]: <https://support.huaweicloud.com/intl/en-us/usermanual-account/account_id_001.html>
[swr-org]: <https://support.huaweicloud.com/intl/en-us/usermanual-swr/swr_01_0014.html>
[devenviron]: <https://support.huaweicloud.com/intl/en-us/devtool-modelarts/devtool-modelarts_0001.html>
[keras-tutorial]: <https://keras.io/examples/vision/image_classification_from_scratch/>
[ai-app-container]: <https://support.huaweicloud.com/intl/en-us/inference-modelarts/inference-modelarts-0009.html>
[real-time-svc]: <https://support.huaweicloud.com/intl/en-us/inference-modelarts/inference-modelarts-0018.html>
