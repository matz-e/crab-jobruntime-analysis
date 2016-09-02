curl -X POST "http://juztas.cern.ch:9200/job_history_crab3/_search?&size=0&pretty=true&q=*" -d '
{
  "aggs": {
    "runtime": {
      "filter": {
        "wildcard": {
          "WorkflowRAW": "*160901*calpas*DYJetsM50*"
        }
      },
      "aggs": {
        "runtime_inner": {
          "histogram": {
            "field": "CommittedTime",
            "interval":1
          }
        }
      }
    }
  }
}'
exit $?
