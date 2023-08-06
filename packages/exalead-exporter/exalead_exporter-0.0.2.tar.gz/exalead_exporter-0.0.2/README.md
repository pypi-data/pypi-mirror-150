# exalead_exporter

## Description
Prometheus exporter for Exalead solution

This exporter collect metrics from Exalead HTTP API.

It is a python HTTP server that exposes metrics to http (default port 9271) that can be then scrapped by [Prometheus](https://github.com/prometheus).

![exporter_diagram](screenshots/exalead_licences.png)

Several Exalead servers can be polled by adding them to the YAML config file, by adding a host section:

**Config**: (see config.yml)

```yaml
exaleads:
  - host: host.domain
    port: 9398
#   protocol: https
#   verify_ssl: false
#   timeout: 20
#   keep_session: true # default
#   default_labels:
#     - name: veeam_em
#       value: my_veeam_em_server.domain
#   proxy:
#     url: http://my.proxy.domain:port/
#     protocol: https

weblisten:
  address: 0.0.0.0
  port: 9247

logger:
  level: info
  facility: syslog

metrics_file: "metrics/*_metrics.yml"
```

## Usage

The exporter may run as a unix command with module installation or as standalone python script without instalation.
<summary>Usage as a system command</summary>

the easiest way is to install from pip:

```shell
pip3 install --upgrade exalead-exporter
```

then you can use the entry point create by the installer of the module in /usr/local/bin/exalead_exporter or in [venv]/bin/exalead_exporter for venv context.
The commanded usage is in venv.

<summary>Usage as a Python Script</summary>

<br>

To use the exporter, few packages needs to be installed. This can be done using:

```shell
pip3 install -r pip_requirements.txt
```

<details>

Contents of requirements.txt

```python
xmltodict==0.12.0
tenacity==6.2.0
requests>=2.20.0
Jinja2==3.0.3
urllib3==1.24.2
prometheus_client==0.14.1
PyYAML>=5.3.1
python-dateutil>=2.7.0
```

</details>

+ Consider, to extract the archiv file in /tmp folder; this will generate a folder /tmp/exalead_exporter_[version].
+ create a directory where you want by example /opt/exalead_exporter_[version],
+ move the /tmp/exalead_exporter_[version]/exalead_exporter_package directory to /opt/eeam_exporter_[version]
+ create a command file to launch the exporter in dir /opt/exalead_exporter_[version]
```shell
vi /opt/exalead_exporter_X.Y.Z/exalead_exporter_cmd
#!/usr/libexec/platform-python
# -*- coding: utf-8 -*-
import re
import sys

from exalead_exporter.exalead_exporter import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())

```
+ Then edit the conf/config.yml file and add your settings.
+ Try your config by executing the command in try mode

example with the default dumy config file:
```shell
python3 exalead_exporter_cmd -n -v

exalead_exporter[227114]: level=INFO - exalead_exporter 0.0.2 starting....
exalead_exporter[227114]: level=DEBUG - config is {'exaleads': [{'host': 'host.domain', 'port': 9398, 'verify_ssl': False, 'timeout': 20}], 'weblisten': {'address': '0.0.0.0', 'port': 9271}, 'logger': {'level': 'info', 'facility': 'syslog'}, 'metrics_file': 'metrics/*.yml'}
exalead_exporter[227114]: level=WARNING - [Errno 2] No such file or directory: '/home/users/d107684/python/exalead-exporter-package/exalead_exporter/metrics'
exalead_exporter[227114]: level=ERROR - no metrics found
exalead_exporter[227114]: level=INFO - exalead_exporter 0.0.2 stopped.
[ /home/users/d107684/python/exalead-exporter-package ]d107684@dal-v-survdadc $ python3 cli.py -v -n
exalead_exporter[228511]: level=INFO - exalead_exporter 0.0.2 starting....
exalead_exporter[228511]: level=DEBUG - config is {'exaleads': [{'host': 'host.domain', 'port': 9398, 'verify_ssl': False, 'timeout': 20}], 'weblisten': {'address': '0.0.0.0', 'port': 9271}, 'logger': {'level': 'info', 'facility': 'syslog'}, 'metrics_file': 'conf/metrics/*.yml'}
exalead_exporter[228511]: level=ERROR - Connection Exception: Host host.domain: HTTPConnectionPool(host='host.domain', port=9398): Max retries exceeded with url: /mami/ (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f02ab6be7f0>: Failed to establish a new connection: [Errno -2] Name or service not known',))
exalead_exporter[228511]: level=DEBUG - # HELP exalead_up probe success  login status: 0 Down / 1 Up
exalead_exporter[228511]: level=DEBUG - # TYPE exalead_up gauge
exalead_exporter[228511]: level=DEBUG - exalead_up 0.0
exalead_exporter[228511]: level=INFO - exalead_exporter 0.0.2 stopped
```

## exporter command line options

to start the exporter:

```shell
./exalead_exporter &
```

By default, it will load the file config.yml to perform action.

<details>
<summary>Detail options</summary>

```shell

Usage: exalead_exporter [-h] [-b BASE_PATH] [-c CONFIG_FILE]
                      [-f LOGGER.FACILITY] [-l {error,warning,info,debug}]
                      [-o  METRICS_FILE] [-m  METRIC] [-n] [-t  TARGET]
                      [-w WEB.LISTEN_ADDRESS] [-V] [-v]

collector for exalead.

optional arguments:
  -h, --help            show this help message and exit
  -b BASE_PATH, --base_path BASE_PATH
                        set base directory to find default files.
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        path to config files.
  -f LOGGER.FACILITY, --logger.facility LOGGER.FACILITY
                        logger facility (syslog or file path).
  -l {error,warning,info,debug}, --logger.level {error,warning,info,debug}
                        logger level.
  -o  METRICS_FILE, --metrics_file METRICS_FILE
                        collect the metrics from the specified file instead of
                        config.
  -m  METRIC, --metric METRIC
                        collect only the specified metric name from the
                        metrics_file.
  -n , --dry_mode       collect the metrics then exit; display results to
                        stdout.
  -t  TARGET, --target TARGET
                        In dry_mode collect metrics on specified target.i
                        Default first from config file.
  -w WEB.LISTEN_ADDRESS, --web.listen-address WEB.LISTEN_ADDRESS
                        Address to listen on for web interface and telemetry.
  -V, --version         display program version and exit..
  -v , --verbose        verbose mode; display log message to stdout.
```

</details>

To test your configuration you can launch the exporter in dry_mode:

```shell
./exalead_exporter -v -n -t host.domain
```

This command will try to connect to the 'host.domain' exaleas server with parameters specified in config.yml, expose the collected metrics, and eventually the warning or errors, then exits.

## Prometheus config

Since several exalead servers can be set in the exporter, Prometheus addresses each server by adding a target parameter in the url. The "target" must be the same (lexically) that in exporter config file.

```yaml
  - job_name: "exalead"
    scrape_interval: 120s
    scrape_timeout: 60s
    metrics_path: /metrics

    static_configs:
      - targets: [ exaleadhost.domain ]
        labels:
          environment: "PROD"
#    file_sd_configs:
#      - files: [ "/etc/prometheus/exalead_exp/*.yml" ]
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: "exalead-exporter-hostname.domain:9247"  # The exalead exporter's real hostname.

```
## Metrics

The collected metrics are defined in separeted files positionned the folder conf/metrics.
All Values, computations, labels are defined in the metrics files, meaning that the exporter doesn't nothing internally on values. The configuration fully drive how values are rendered.

### Collected Metrics

All metrics are defined in the configuration file (conf/metrics/*.yml). You can retrive all metric names here. Most of them have help text too.
All metrics are prefixed with "exaled_".

file | domain | metrics
---- | ------ | -------
none | default | exalead_up : 0 or 1.<br>define if exalead server can be reached or not.
licence_status.yml | general licences elements | prefix: exalead_license_ .<br><li> licence status, <li> expiration, <li>token usage, <li>licence components activation.<br>(see [licences dashboard](screenshots/exalead_licences.png))
deploymentsStatus.yml | general indexing processes | prefix: exalead_process_.<br> <li> status labeled by process name, <li> start_timestamp"backedup", <li>unexpected restart count, <li> loop crashing.<br>(see [processes dashboard](screenshots/exalead_processes.png))
connectorStatus.yml | indexation | Prefix: exalead_connectors_.<br> gauge by connector name: <li>active_documents, <li>added, <li>deleted, <li>failed deleted, <li>indexed documents, <li>partial update, <li>replaced, <li>total <li>scan_status, <li>scan_retries, <li>scan_duration, <li>scan_deleted_objects, <li>scan_pushed_objects<br>(see [processes dashboard](screenshots/exalead_connectors.png))

## Extending metrics

Exported metrics, are defined the YAML config file. The value can use Jinja2 templating language. The format of the configuration is inspired from Ansible task representation.
So a metric configuration file, consists in a list of action to perform.

There are five possible actions:

- url: to collect metrics from HTTP API
- set_fact: to assign vlaue to variables
- actions: to perform a list of (sub-)actions
- metrics: to define metrics to expose/return to Prometheus
- debug: to display debug text to logger.

All actions have default "attributes":

- name: the name of action or metric counter for metrics action.
- vars: to set vars to global symbols' table.
- with_items: to loop on current action with a list of items.
- loop_var: to set the name of the variable that will receive the current value in the loop. Default is 'item'.
- when: a list of condition (and) that must be check and be true to perform the action.

The "attributes" are analyzed in the order specified in previous table; it means that you can't use "item" var (obtained from 'with_items' directive) in the vars section because it is not yet defined when the 'vars' section is evaluated. If you need that feature, you will have to consider 'with_items' in an 'actions' section (see metrics/connectorStatus.yml).

action | parameter | description | remark
------ | ----------- | ------ | ------
url | &nbsp; |a string that's representing the entity to collect without '/api' | http://host.domain:port/api**[url]**. e.g.: /reports/summary/overview
 &nbsp; | var_name |the name of the variable to store the results. Default is '_root' meaning that the resulting JSON object is directly store in symbols table. | &nbsp;
 &nbsp; | &nbsp; | &nbsp; | &nbsp; 
 set_fact | &nbsp; | list of variable to define | &nbsp; 
 &nbsp; | var_name: value| &nbsp;  
 &nbsp; | &nbsp; | &nbsp; | &nbsp; 
metrics | &nbsp; | define the list of metrics to expose
 &nbsp; | metric_prefix | a prefix to add to all metric name | final name will be [metric_prefix]_[metric_name]
 'a metric' | name | the name of the metric
 &nbsp; | help | the help message added to the metric (and displayed in grafana explorer)
 &nbsp; | type 'gauge' or 'counter' | the type of the prometheus metric | &nbsp;
 &nbsp; | value | the numeric value itself | &nbsp;
 &nbsp; | labels | a list of name value pairs to qualify the metric | &nbsp;

