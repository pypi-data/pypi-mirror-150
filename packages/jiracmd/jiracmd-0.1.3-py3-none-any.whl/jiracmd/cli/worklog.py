import json
import click
import datetime
from jiracmd.jira import JiraAPIClient
from jiracmd.objects import Worklog
from jiracmd.utils import output_table


@click.group(name="worklog")
def worklog_cli():
    pass

@click.command(name="get")
@click.option('-w', '--worklog-id', required=True)
@click.option('-i', '--issue', required=True)
@click.option('-o', '--output', default="json")
@click.option('--short', is_flag=True, default=False)
def worklog_get(worklog_id, issue, output, short):
    call = f"issue/{issue}/worklog/{worklog_id}"
    response = jira._get(call)
    print(Worklog(**response.json()).get_outputs(short=short).get(output))


@click.command(name="add")
@click.option('-i', '--issue', required=True)
@click.option('-d', '--date', type=click.DateTime(formats=["%Y-%m-%d"]), default=str(datetime.date.today()))
@click.option('-s', '--start', type=click.DateTime(formats=["%H:%M"]))
@click.option('-e', '--end', type=click.DateTime(formats=["%H:%M"]))
def worklog_add(issue, date, start, end):
    time_diff = end - start
    start_date = datetime.datetime.combine(date.date(), start.time())
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_spent = f"{hours}h {minutes}m"
    start_fmt = start_date.astimezone().strftime('%Y-%m-%dT%H:%M:%S.000%z')
    body = json.dumps({
        "started": start_fmt,
        "timeSpent": time_spent
    })
    validation = jira.validate_worklog(issue, start_fmt)
    if validation == "ok":
        response = jira._post(f'issue/{issue}/worklog?adjustEstimate=auto', body)
        click.echo(Worklog(**response.json()))
    else:
        print(f"Skiped worklog due to validation. {validation}")
        


@click.command(name="list")
@click.option('-i', '--issue', required=True)
@click.option('-s', '--sort-by', default="started")
def worklog_list(issue, sort_by):
    worklogs = jira.get_issue_worklogs(issue)
    worklogs_table = [w.to_short_dict() for w in worklogs]
    output_table(worklogs_table, sort_by=sort_by)

@click.command(name="delete")
@click.option('-i', '--issue', required=True)
@click.option('-w', '--worklog-id', required=True)
def worklog_delete(issue, worklog_id):
    response = jira._delete(f'issue/{issue}/worklog/{worklog_id}')
    try:
        response.json()
        click.echo(json.dumps(response.json(), indent=2))
    except ValueError:
        click.echo(response.content)

worklog_cli.add_command(worklog_get)
worklog_cli.add_command(worklog_add)
worklog_cli.add_command(worklog_delete)
worklog_cli.add_command(worklog_list)

jira = JiraAPIClient()
