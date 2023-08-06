#### This library enables you to report the status of tasks in your model at runtime

#### publish:

```shell
python setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

```

#### install: `pip install apeman-model-client==0.1.8`

#### How to use

```shell
export apeman_meta_server_addr='localhost:9090'
```

```python


from apeman.model.openapi import apemanOpenApi
from apeman.model.openapi.model_instance_task_status import TaskStatus
from apeman.model.openapi.model_instance_task_launch_type import TaskLaunchType
from apeman.model.openapi.model_instance_task_type import TaskType

client = apemanOpenApi.ApemanModelServiceClient()
# get endpoint of other model
client.get_endpoint(model_instance_id='test')
# report status
client.report(task_id='', status=TaskStatus.RUNNING, progress=0.1, message='test', token='')
# create new instance tak
task_id = client.add_model_instance_task(model_instance_id='test', tenant_id='test', task_token='token',
                               task_parameters='parameters', job_context='jobContext', start_time=1111, end_time=11111,
                               launch_type=TaskLaunchType.TASK_ADHOC, task_type=TaskType.TASK_TRAIN)
# get instance task
task = client.get_instance_task(model_instance_task_id='test', token='token')
print(task.taskProgress)
print(task.taskMessage)
print(task.taskStatus)

```
