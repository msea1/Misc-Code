# https://docs.atlassian.com/software/jira/docs/api/REST/8.5.5/#api/2/worklog-getWorklogsForIds

from subprocess import call

API_BASE = 'https://jira.spaceflightindustries.com/rest/api/2'

user = 'mcarruth'
cred = call("cat ~/.one_login", shell=True)
curl_u = f'-u {user}:{cred}'
curl_cruft = '-X GET -H "Content-Type: application/json"'

# grab tickets created
made = f'curl {curl_u} {curl_cruft} {API_BASE}/search?jql=reporter={user}+AND+createdDate+%3E%3D+2020-06-01'

# grab tickets resolved
# have to be assigned to it unfortunately
done = f'curl {curl_u} {curl_cruft} {API_BASE}/search?jql=assignee={user}+status+in+(Closed,Resolved,Done,Canceled)+AND+resolutiondate+%3E%3D+2020-06-01'

# grab comments/work logged


# format it



# grab specific ticket
ticket = f'curl {curl_u} {curl_cruft} {API_BASE}/issue/GCS-3000'

# grab jql syntax from filter
filter_info = f'curl {curl_u} {curl_cruft} {API_BASE}/filter/13200'


# http -a mcarruth https://jira.spaceflightindustries.com/rest/api/2/issue/GCS-3000
