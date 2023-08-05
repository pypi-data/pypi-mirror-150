from googleapiclient.discovery import build
import upswingutil as ul

def create_dataflow_job_for_sending_emails(jobname: str, parameters: dict):
    dataflow = build('dataflow', 'v1b3')
    request = dataflow.projects().templates().launch(
        projectId=ul.G_CLOUD_PROJECT,
        gcsPath="gs://dataflow-content/Communication/EmailTrigger/templates/email_trigger",
        body={
            'jobName': jobname,
            'parameters': parameters,
            'environment': {
                "tempLocation": "gs://dataflow-content/Communication/EmailTrigger/staging/temp",
                "zone": "asia-south1"
            }
        }
    )
    response = request.execute()
    return response