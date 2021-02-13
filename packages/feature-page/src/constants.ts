export const DefaultPageSection = {
  config: {
    h: 500,
    style: {}
  },
  section_type: 'editor',
  page_id: null,
  nodes: [],
}

export const DEFAULT = {
  "title": "这是一个新页面",
  "featureType": "page",
  "config": {
    "viewMode": "fixed",
    "style": {},
    "children": [
      {
        "id": "1",
        "type": "section",
        "style": {
          "background-color": "#fff"
        },
        "data": {
          "target": ""
        },
        "pos": {
          "w": 1200,
          "h": 500,
          "x": 0,
          "y": 0
        },
        "children": [{
          "id": "12",
          "type": "TextNode",
          "pos": {
            "x": 10,
            "y": 10,
            "width": 100,
            "height": 100
          },
          "style": {
            "color": "#333"
          },
          "data": {
            "target": "这是一段文字呀"
          }
        }]
      }
    ]
  }
}
