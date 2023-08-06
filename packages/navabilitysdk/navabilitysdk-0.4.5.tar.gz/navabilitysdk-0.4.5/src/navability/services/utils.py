import time
from typing import List

# use markdown to link to graph and map visualizations
from IPython.display import Markdown as md

from navability.entities import NavAbilityClient
from navability.services import getStatusesLatest


async def waitForCompletion(
    navAbilityClient: NavAbilityClient,
    requestIds: List[str],
    maxSeconds: int = 60,
    expectedStatuses: List[str] = None,
    exceptionMessage: str = "Requests did not complete in time",
):
    """Wait for the requests to complete, poll until done.

    Args:
        requestIds (List[str]): The request IDs that should be polled.
        maxSeconds (int, optional): Maximum wait time. Defaults to 60.
        expectedStatus (str, optional): Expected status message per request.
            Defaults to "Complete".
    """
    if expectedStatuses is None:
        expectedStatuses = ["Complete", "Failed"]
    wait_time = maxSeconds
    tasksComplete = False
    while not tasksComplete:
        statuses = (await getStatusesLatest(navAbilityClient, requestIds)).values()
        tasksComplete = all(s.state in expectedStatuses for s in statuses)
        if tasksComplete:
            break
        else:
            time.sleep(2)
            wait_time -= 2
            if wait_time <= 0:
                raise Exception(exceptionMessage)


# Helper functions for NavAbility App visualizations
def GraphVizApp(client, variableStartsWith=None):
    topography_vis_link = f"https://app.navability.io/cloud/graph/?userId={client.userId}&robotStartsWith={client.robotId}&sessionStartsWith={client.sessionId}"
    if variableStartsWith!=None:
        topography_vis_link = topography_vis_link + '&variableStartsWith'
        if 0 < len(variableStartsWith):
            topography_vis_link = topography_vis_link + '=' + variableStartsWith
    print(topography_vis_link)
    try:
        return md(f"""[![Navigate to Factor Graph](http://www.navability.io/wp-content/uploads/2022/03/factor_graph.png)]({topography_vis_link})""")
    except:
        return

def MapVizApp(client, variableStartsWith=None):
    geometry_vis_link = f"https://app.navability.io/cloud/map/?userId={client.userId}&robotStartsWith={client.robotId}&sessionStartsWith={client.sessionId}"
    if variableStartsWith!=None:
        geometry_vis_link = geometry_vis_link + '&variableStartsWith'
        if 0 < len(variableStartsWith):
            geometry_vis_link = geometry_vis_link + '=' + variableStartsWith
    print(geometry_vis_link)
    try:
        return md(f"""[![Navigate to Factor Graph](http://www.navability.io/wp-content/uploads/2022/03/geometric_map.png)]({geometry_vis_link})""")
    except:
        return
