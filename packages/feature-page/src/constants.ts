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
    "viewMode": "adapt",
    "style": {},
    "pos": {
      "w": 1200
    },
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

export const DEFAULT_H5_PAGE = {
  "title": "这是一个长页h5",
  "featureType": "page",
  "displayType": "h5page",
  "config": {
    "viewMode": "adapt",
    "style": {},
    "pos": {
      "w": 375
    },
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
          "w": 375,
          "h": 667,
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

export const DEFAULT_H5_SWIFT = {
  "title": "这是一个翻页H5",
  "featureType": "page",
  "displayType": "h5swift",
  "config": {
    "viewMode": "adapt",
    "style": {},
    "pos": {
      "w": 375
    },
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
          "w": 375,
          "h": 667,
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

export const getDefault = (displayType: string) => {
  switch(displayType) {
    case "page":
      return DEFAULT;
    case "h5swift":
      return DEFAULT_H5_SWIFT;
    case "h5page":
      return DEFAULT_H5_PAGE;
  }
  return null;
}
