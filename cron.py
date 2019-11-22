from apscheduler.schedulers.blocking import BlockingScheduler
from modules.siteAdapter import RssParser


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=4)
def startSiteAdapter():
    print('tests')
    siteAdapter = RssParser()
    siteAdapter.start()

sched.start()
