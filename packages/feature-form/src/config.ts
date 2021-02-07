import { IPropertiesComponents } from "@tefact/properties"
import { IPropertiesRow, IPropertiesTab } from "@tefact/properties"

export class FormProperties {
  static defaultStyledProperties() {
    return {
      title: '基本信息',
      components: [
        {
          type: 'RowsProperties', params: {
            title: '字段基本信息',
            rows: [{
              type: 'TextRow',
              params: {
                title: "描述文字",
                path: "config.text"
              }
            }]
          }
        },
        { type: 'BackgroundProperties', params: {} },
        { type: 'BorderProperties', params: {} },
        { type: 'TextProperties', params: {} }
      ],
    }
  }

  static defaultProperties(type: string, components?: Array<IPropertiesComponents>, rowComponents?: Array<IPropertiesRow>) {
    const res = {
      title: '基本信息',
      components: [
        {
          type: 'RowsProperties',
          params: {
            title: '字段基本信息',
            rows: [{
              type: 'TextRow',
              params: {
                title: "字段名",
                path: "config.label"
              }
            }, {
              type: type,
              params: {
                title: "默认值",
                path: "config.default"
              }
            }, {
              type: 'TextRow',
              params: {
                title: "描述",
                path: "config.desc"
              }
            }, {
              type: 'TextRow',
              params: {
                title: "提示",
                path: "config.placeholder"
              }
            }, {
              type: 'SwitchRow',
              params: {
                title: "是否必填",
                path: "config.notNull"
              }
            }]
          }
        },
        { type: 'BackgroundProperties', params: {} },
        { type: 'BorderProperties', params: {} }
      ],
    } as IPropertiesTab

    if (components) {
      res.components = [ ...res.components, ...components ]
    }

    if (rowComponents) {
      const params = res.components[0].params
      if (params.rows) {
        params.rows = [ ...(params.rows as Array<IPropertiesRow>), ...rowComponents ]
      } else {
        params.rows = rowComponents;
      }
    }

    return res;
  }

  static PROPERTIES = {
    title: '页面配置',
    hasTab: true,
    tabs: [
      {
        title: '基本信息',
        components: [
          { type: 'BackgroundProperties', params: {} },
          { type: 'BorderProperties', params: {} },
          {
            type: 'RowsProperties', params: {
              title: '布局设置',
              rows: [{
                type: 'SelectRow',
                params: {
                  title: "布局模式",
                  path: "config.viewMode",
                  selectOptions: [
                    {value: 'fixed', label: '固定'},
                    {value: 'adapt', label: '适配'},
                  ]
                }
              }, {
                type: 'NumberRow',
                params: {
                  title: "页面宽度",
                  unit: "px",
                  path: "config.style.width"
                }
              }, {
                type: 'NumberRow',
                params: {
                  title: "标签宽度",
                  unit: "px",
                  path: "config.labelWidth"
                }
              }]
            }
          },
          {
            type: 'ListProperties',
            params: {
              title: '按钮设置',
              path: 'config.buttons',
              rows: [{
                type: 'TextRow',
                params: {
                  title: "按钮名",
                  path: "label"
                }
              }, {
                type: 'SelectRow',
                params: {
                  title: "按钮类型",
                  path: "type",
                  selectOptions: [
                    { value: 'submit', label: '提交' },
                    { value: 'clear', label: '重置' },
                    { value: 'link', label: '连接' },
                  ]
                }
              }, {
                type: 'SelectRow',
                params: {
                  title: "样式",
                  path: "styleType",
                  selectOptions: [
                    { value: 'primary', label: 'Primary' },
                    { value: 'info', label: 'Info' },
                    { value: 'warning', label: 'Warning' },
                    { value: 'danger', label: 'Danger' },
                    { value: 'text', label: 'Text' },
                    { value: 'success', label: 'Success' },
                    { value: 'default', label: '默认' },
                  ]
                }
              }, {
                type: 'TextRow',
                params: {
                  title: "链接",
                  path: "link"
                }
              }]
            }
          }
        ],
      },
    ],
  }
}
