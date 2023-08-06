from azureml.core import Workspace, Datastore
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.core import Dataset
from azure.ai.ml import command

#subscription_id = #use your subscription id
#resource_group = #use your resource group
#workspace_name = #use your workspace name

subscription_id = "0a94de80-6d3b-49f2-b3e9-ec5818862801"
resource_group = "buas-y2"
workspace_name = "MLOpsRobotics"

# Log in using interactive Auth
auth = InteractiveLoginAuthentication()

# Declare workspace & datastore.
workspace = Workspace(subscription_id=subscription_id,
                      resource_group=resource_group,
                      workspace_name=workspace_name,
                      auth=auth,
                      )

# configure job
job = command(
    code="./src",
    command="python train.py",
    environment="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu@latest",
    compute="aml-cluster",
    display_name="train-model",
    experiment_name="train-classification-model"
    )

# submit job
returned_job = ml_client.create_or_update(job)