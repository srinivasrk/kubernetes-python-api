from __future__ import print_function
import time
from kubernetes import client, config
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint

def main():
    config.load_kube_config()
    v1 = client.BatchV1Api()
    namespace = 'default' # str | object name and auth scope, such as for teams and projects
    envdata = kubernetes.client.V1EnvVar('RABBITMQ_SERVER', '159.203.167.38')
    containers = kubernetes.client.V1Container(
            name='c',
            image='index.docker.io/srini92/cw:latest',
            env=[envdata]
            )
    podSpec = kubernetes.client.V1PodSpec(
            containers=[containers],
            restart_policy='OnFailure'
            )
    jobTemplate = kubernetes.client.V1PodTemplateSpec(
            spec=podSpec
            )
    jobSpec = kubernetes.client.V1JobSpec(  # if both parallelism and completions is unset it is defaulted to 1
            template=jobTemplate
            )
    metadata = kubernetes.client.V1ObjectMeta(
            name='test-api-kubernetes'
            )
    body = kubernetes.client.V1Job(
            api_version='batch/v1',
            kind='Job',
            metadata=metadata,
            spec=jobSpec
            )  # V1Job
    print(body)
    include_uninitialized = True # bool | If true, partially initialized resources are included in the response. (optional)
    pretty = 'true' # str | If 'true', then the output is pretty printed. (optional)
    try:
        api_response = v1.create_namespaced_job(namespace, body, include_uninitialized=include_uninitialized, pretty=pretty)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BatchV1Api->create_namespaced_job: %s\n" % e)

if __name__ == '__main__':
    main()

