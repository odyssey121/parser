from apscheduler.schedulers.blocking import BlockingScheduler
from modules.siteAdapter import RssParser


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=10)
def startSiteAdapter():
    siteAdapter = RssParser()
    siteAdapter.start()

sched.start()