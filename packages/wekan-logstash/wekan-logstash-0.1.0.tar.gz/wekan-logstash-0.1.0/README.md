# wekan-logstash

To format data for logstash and ELK (Kibana) - Format below :

```json
{
  "id": "7WfoXMKnmbtaEwTnn",
  "title": "Card title",
  "storyPoint": 2.0,
  "nbComments": 1,
  "createdBy": "fmonthel",
  "labels": [
    "I-U",
    "I-Nu"
  ],
  "assignees": "fmonthel",
  "members": [
    "fmonthel",
    "Olivier"
  ],
  "boardSlug": "test",
  "description": "A subtask description",
  "startAt": "2021-06-07T20:36:00.000Z",
  "endAt": "2021-06-07T20:36:00.000Z",
  "requestedBy": "LR",
  "assignedBy": "MM",
  "receivedAt": "2021-06-07T20:36:00.000Z",
  "archivedAt": "2021-06-07T20:36:00.000Z",
  "createdAt": "2021-06-07T20:36:00.000Z",
  "lastModification": "2017-02-19T03:12:13.740Z",
  "list": "Done",
  "dailyEvents": 5,
  "board": "Test",
  "isArchived": true,
  "dueAt": "2021-06-07T20:36:00.000Z",
  "swimlaneTitle": "Swinline Title",
  "customfieldName1": "value1",
  "customfieldName2": "value2",
  "boardId": "eJPAgty3guECZf4hs",
  "cardUrl": "http://localhost/b/xxQ4HBqsmCuP5mYkb/semanal-te/WufsAmiKmmiSmXr9m",
  "checklists": [
      {"TODO": [
          {"isfinished": false, "title": "todo1"},
          {"isfinished": false, "title": "todo2"}
        ]
      },
      {"DONE": [
          {"isfinished": true, "title": "done1"},
          {"isfinished": true, "title": "done2"}
        ]
      }
  ]
}
```

Goal is to export data into Json format that we can be used as input for Logstash and ElastisSearch / Kibana (ELK)

Import in logstash should be done daily basic (as we have field daily event)
