import time
import email
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3
import json
from airflow.models import Variable
import logging as log
from utils.constants import email_template, email_body, col_name, row_data

def get_credentials(SecID):
    log.info('Getting creds from secrete manager')
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=SecID)
    result = json.loads(response['SecretString'])
    log.info('Got creds got successfully from secrete manager')
    return result

def sender_email_function(context):
  region = 'ap-south-1'
  recipient_email = ["ujjawal.mandhani@lumiq.ai"]
  dag_id = context['dag'].dag_id
  task_id = context['task'].task_id
  exception_from_dag = context["exception"]
  log.error(f"DAG ID: {dag_id}")
  log.error(f"Task ID: {task_id}")
  log.error(f"exception_from_dag: {exception_from_dag}")
  ses_client = boto3.client('ses', region_name=region)
  sender_email =  'baxa.alerts@lumiq.ai'
  msg = MIMEMultipart()
  msg['Subject'] = f"Dag failure on UAT {dag_id}"
  msg['From'] = sender_email
  msg['To'] = ', '.join(recipient_email)
  col_names = ["Description", "Message"]
  col_final = ""
  for item in col_names:
      col_final = col_final + col_name.replace("col_name", item) + "\n"
  row_final = ""
  row_alert_data = [
      {
          "dag_id": dag_id,
          "task_id": task_id,
          "exception_from_dag": exception_from_dag
      }
  ]
  for item in row_alert_data:
    for key, value in item.items():
      row = "<tr> \n"
      row = row + row_data.replace("value_name", str(key))
      row = row + row_data.replace("value_name", str(value))
      row = row + "</tr>"
      row_final = row_final + row
  final_data = col_final + row_final
  email_body_updated = email_body.replace('Report_header_name', 'Airflow UAT EMR Failure Alert').replace('TABLEBODY', final_data)
  email_final_template = email_template.replace('TABLEBODY', email_body_updated).replace("reportTitle", '').replace('reportMessageHeader', '')
  log.info(email_final_template)
  msg.attach(MIMEText(email_final_template, "html"))
  try:
      response = ses_client.send_raw_email(
          Source=sender_email,
          Destinations=recipient_email,
          RawMessage={
              'Data': msg.as_string(),
          }
      )
      log.info("Email sent! Message ID:", response['MessageId'])
  except Exception as e:
      log.info("Error sending email:", e)