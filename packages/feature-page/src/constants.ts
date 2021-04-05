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
            "x": 20,
            "y": 20,
            "w": 100,
            "h": 100
          },
          "style": {
            "color": "#333"
          },
          "data": {
            "target": "请输入文字"
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
            "x": 20,
            "y": 20,
            "w": 100,
            "h": 100
          },
          "style": {
            "color": "#333"
          },
          "data": {
            "target": "请输入文字"
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
            "x": 20,
            "y": 20,
            "w": 100,
            "h": 100
          },
          "style": {
            "color": "#333"
          },
          "data": {
            "target": "请输入文字"
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
