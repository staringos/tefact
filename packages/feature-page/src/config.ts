import { IPropertiesComponents } from "@tefact/properties"
import { IProperties } from "@tefact/properties"
import { IBaseNode } from "@tefact/core"

export class PageProperties {
  static defaultPageSections(): IBaseNode {
    return {
      id: "",
      type: "section",
      pos: {
        h: 500,
        w: 500,
        x: 0,
        y: 0,
      },
      style: {},
      data: {},
      // section_type: 'editor',
      // page_id: null,
      children: [] as Array<IBaseNode>,
    }
  }

  static defaultProperties(title: string, dataComponents?: Array<IPropertiesComponents> | null, basicComponents?: Array<IPropertiesComponents>) {
    const res = {
      title,
      hasTab: true,
      tabs: [
        {
          title: '基本信息',
          components: [
            { type: 'PositionProperties', params: {} },
            { type: 'BackgroundProperties', params: {} },
            { type: 'BorderProperties', params: {} },
            { type: 'TextProperties', params: {} }
          ],
        },
      ],
    } as IProperties

    if (basicComponents) {
      res.tabs[0].components = [ ...res.tabs[0].components, ...basicComponents ]
    }

    if (dataComponents) {
      res.tabs.push({
        title: '数据展示',
        components: [ ...dataComponents ],
      })
    }

    return res;
  }

  static PROPERTIES = {
    page: {
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
                }]
              }
            }
          ],
        },
      ],
    },
    section: {
      title: '段落配置',
      hasTab: true,
      tabs: [
        {
          title: '基本信息',
          components: [
            {
              type: 'RowsProperties', params: {
                title: '样式设置',
                rows: [{
                  type: 'TextRow',
                  params: {
                    title: "高度",
                    type: "number",
                    suffix: "px",
                    path: "config.h"
                  }
                }]
              }
            },
            { type: 'BackgroundProperties', params: {} },
            { type: 'BorderProperties', params: {} },
          ],
        },
      ],
    },
  }
}
