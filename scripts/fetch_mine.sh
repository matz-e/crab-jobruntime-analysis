curl -X POST "http://juztas.cern.ch:9200/job_history_crab3/_search?&size=1&pretty=true&q=*" -d '
{
  "aggs": {
    "runtime": {
      "filter": {
        "wildcard": {
          "Workflow": "*matze*v30*"
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
