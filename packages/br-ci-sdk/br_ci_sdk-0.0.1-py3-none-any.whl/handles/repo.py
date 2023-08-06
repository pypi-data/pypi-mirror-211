import json
from subprocess import run
from sucloud.services.notebook.v1.client import Client as NotebookClient
from sucloud.common.config import ClientConfig
from sucloud.common.credentials import Credentials
from sucloud.services.notebook.v1.types import Image, ImageType, Notebook
import createPod
import yaml


def online_compile(path=None):
    # 生成dockerfile
    generate_dockerfile(path)

    # 生成docker镜像
    run("docker build -t supa -f Dockerfile-online-compile .", shell=True)

    # push镜像到sucloud的harabor仓库
    run("docker login https://br-harbor01.birentech.com -u e00928 -p brkj@2020!", shell=True)
    run("docker tag supa br-harbor01.birentech.com/online-compile/supa:latest", shell=True)
    run("docker push  br-harbor01.birentech.com/online-compile/supa:latest", shell=True)
    print("push image to harbor")
    # run("sudo docker run -itd --name supa br-harbor01.birentech.com/online-compile/supa:latest /bin/bash")

    # trigger sucloud在线代码编译
    # config = ClientConfig(
    #     Credentials(
    #         access_token="access_token",
    #     ),
    #     endpoint="sgc.birentech.com:443",
    #     group="a1aa1cc1-bd80-11ed-96df-e65d07784674",
    # )

    # notebook_client = NotebookClient(
    #     config=config
    # )

    # try:
    #     request = Notebook(name="supa-ci-test", image=Image(name="br-harbor01.birentech.com/online-compile/supa:latest", image_type=ImageType.Preset))
    #     notebook_client.create(request)
    #     print("创建开发环境")

    # except Exception as e:
    #     print(e)

    # infra k8s集群资源在线代码编译
    generate_yaml_file()
    createPod.create_pod()
    status = createPod.read_pod_status("supa-pod", "default")
    print("状态: " + str(status))


def generate_dockerfile(path: str):
    if path == None:
        path = "./Dockerfile-online-compile"
    file = open(path, 'w')
    file.write("# online compile dockerfile")   
    file.write("\n" + "FROM br-harbor01.birentech.com/ci/ubuntu-18.04/ubuntu-18.04-fullstack:3487")
    file.write("\n" + "WORKDIR /app")
    file.write("\n" + "COPY ./ /app")
    file.write("\n" + "CMD bash build.sh --internal -p /usr/local/supa")


# 生成yaml文件
def generate_yaml_file():
    apiData = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": "supa-pod",
            "namespace": "default",
            "labels": {
                "name": "supa-pod"
            }
        },
        "spec": {
            "containers":[
                {
                "name": "supa-container",
                "image": "br-harbor01.birentech.com/online-compile/supa:latest",
                "imagePullPolicy": "IfNotPresent",
                "command": ["/bin/sh","-c","bash build.sh --internal -p /usr/local/supa"]
                }
            ],
            "restartPolicy": "Always"
        }
    }

    with open('./test_pod.yml', mode='w', encoding='utf-8') as f:
        yaml.dump(data=apiData, stream=f, allow_unicode=True)


def yaml_to_json():
    with open("/home/e00928/code/br_ci_db_sdk/test.yaml", encoding="utf-8") as f:
        datas = yaml.load(f,Loader=yaml.FullLoader)  # 将文件的内容转换为字典形式
    jsonDatas = json.dumps(datas, indent=5) # 将字典的内容转换为json格式的字符串
    print(jsonDatas)
