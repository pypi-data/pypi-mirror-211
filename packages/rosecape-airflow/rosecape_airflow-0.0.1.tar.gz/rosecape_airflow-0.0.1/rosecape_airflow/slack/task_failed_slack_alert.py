from airflow.hooks.base_hook import BaseHook
from airflow.operators.slack_operator import SlackAPIPostOperator

def task_failed_slack_alert(context, slack_conn_id):
    """
    Sends message to Slack about task failure.

    :param context: The execution context
    :type context: dict
    :param slack_conn_id: Slack connection ID
    :type slack_conn_id: str
    :return: None
    """
    
    slack_channel = BaseHook.get_connection(slack_conn_id).login
    slack_token = BaseHook.get_connection(slack_conn_id).password
    failed_alert = SlackAPIPostOperator(
        task_id='slack_failed',
        channel=slack_channel,
        token=slack_token,
        text="""
            :red_circle: Task Failed. 
            *Task*: {task}  
            *Dag*: {dag} 
            *Execution Time*: {exec_date}  
            *Log Url*: {log_url} 
            """.format(
            task=context.get('task_instance').task_id,
            dag=context.get('task_instance').dag_id,
            ti=context.get('task_instance'),
            exec_date=context.get('execution_date'),
            log_url=context.get('task_instance').log_url,
        )
    )
    return failed_alert.execute(context=context)