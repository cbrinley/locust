'''
this file will handle different reporting subsystems.
report subsystem will subscribe to events for which they know 
the signature and handle accordingly.

reporting engines can be turned on from command line via
-R/--report <name>
report engine specific options:
-O/--subsystem-option <report_name>:<opt_name>:<opt_value>

incidentally --subsys-opt will probably be extended as a general feature to provide
all subsystems with ability to take specific configuration on command line
applied to the class object for the subsystem.

reporting engines from a locust file can be activated like so:

from locust.reporting import graphite
graphite.base_metric_name = "load_tests.mywebapp"
graphite.input_server = "carbon-relay.mydomain.com"
graphite.input_port = 12345
graphite.output_server = "graphite-webapp.mydomain.com"
graphite.output_port = "8080"
graphite()

MyTasks(TaskSet):
  @task
  def do_stuff(self):
    self.client.action() #fires events that graphite can handle

for the implementer of a client:
Client(BaseClient):
  def action(self):
    # do stuff
    events.time_series_metric.fire("action.latency_ms",400)

for the reporting implementer
Graphite(BaseReport):
  option_name = None #supply me via command line or task file
  def __init__(self,*args,**kwargs):
    events.time_series_metric += self.submit_metrics

  @prepend_base_metric_name
  def submit_metrics(self,name,value):
    self.send_or_queue(name,value)


 Reports will have one general and one modified "base class"
 general will do what all good base classes do, sit around and
 collect the credit for the real work.
 The more specific base class will be SingletonReport
 this will allow only one instance of a report to ever be created.
'''