curl -X POST "http://juztas.cern.ch:9200/job_history_crab3/_search?&size=0&pretty=true&q=*" -d '
{
  "aggs": {
    "runtime": {
      "filter": {
        "wildcard": {
          "WorkflowRAW": "*mmascher_crab_calpas62"
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
