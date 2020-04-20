# Arrplat Entities

### 列表接口

- URL: app/{app_id}/page/{page_id}
- Methods: GET
- Params:

```json
{
  "page": {
    "page": 1,
    "size": 10
  },
  "search_condition": [{
    "field_id": "12",
    "value": ""
  }],
  "sort": {
    "field_id": "12",
    "order": "desc"
  }
}
```

- Response: 

```json
{
  "data": {
    "direction": 2, 
    "id": "84da60a6a17d4e1eb38e440fd0e4ddc3", 
    "key": "customer-page", 
    "page_section": [
      {
        "entity": {
          "data_type": 1, 
          "entity_data": [{
            "id": "",
            "name": "张三",
            "options": [{
              "name": "修改",
              "type": "edit"
            }, {
              "name": "修改",
              "type": "edit"
            }]  
          }], 
          "entity_fields": [
            {
              "data_type": "string", 
              "display_type": 1, 
              "entity": "cdfda7aa4a0744ec81b030323c1b0693", 
              "exists_type": "", 
              "has_go_details": true, 
              "has_search": true, 
              "has_sort": true, 
              "id": "31714535917a4bc3ac1a553d30c29aac", 
              "is_primary": false, 
              "key": "name", 
              "name": "\u5ba2\u6237\u540d\u79f0", 
              "query_sql": null, 
              "sort": 1, 
              "type": 1
            }, 
            {
              "data_type": "string", 
              "display_type": 1, 
              "entity": "cdfda7aa4a0744ec81b030323c1b0693", 
              "exists_type": "", 
              "has_go_details": true, 
              "has_search": true, 
              "has_sort": true, 
              "id": "71c59f48efb244368be88d69c2d007ba", 
              "is_primary": false, 
              "key": "description", 
              "name": "\u5ba2\u6237\u63cf\u8ff0", 
              "query_sql": null, 
              "sort": 1, 
              "type": 1
            }, 
            {
              "data_type": "string", 
              "display_type": 1, 
              "entity": "cdfda7aa4a0744ec81b030323c1b0693", 
              "exists_type": "", 
              "has_go_details": true, 
              "has_search": true, 
              "has_sort": true, 
              "id": "99cf67e8664f434f853fa79200189123", 
              "is_primary": false, 
              "key": "options", 
              "name": "\u5ba2\u6237\u64cd\u4f5c", 
              "query_sql": null, 
              "sort": 1, 
              "type": 1
            }, 
            {
              "data_type": "string", 
              "display_type": 1, 
              "entity": "cdfda7aa4a0744ec81b030323c1b0693", 
              "exists_type": "", 
              "has_go_details": true, 
              "has_search": true, 
              "has_sort": true, 
              "id": "c3103d46727f4daeb1efb9609c2e1bb0", 
              "is_primary": true, 
              "key": "id", 
              "name": "id", 
              "query_sql": null, 
              "sort": 1, 
              "type": 1
            }
          ], 
          "id": "cdfda7aa4a0744ec81b030323c1b0693", 
          "key": "crm_customer", 
          "table_name": "crm_customer", 
          "title": null
        }, 
        "html_content": null, 
        "id": "5aa5c2a174b2409da1700e191df8ade1", 
        "page_section_to": [], 
        "section_type": null, 
        "title": null
      }
    ], 
    "title": "\u5ba2\u6237\u5217\u8868", 
    "type": null, 
    "unique_id": "ad1c2378996748dcb6e7f3d740485254"
  }, 
  "message": null, 
  "page": null
}

```
