import type { IPropertiesComponents } from "@tefact/properties"
import type { IProperties } from "@tefact/properties"
import type { IBaseNode } from "@tefact/core"

export class PageProperties {
  static defaultPageSections(displayType: string = "page"): IBaseNode {
    let w = "100%";
    let h = 500 as number | string;

    if (displayType === "h5page" || displayType === "h5swift") h = 667;

    return {
      id: "",
      type: "section",
      pos: {
        h,
        w,
        x: 0,
        y: 0,
      },
      style: {
        "background-color": "white"
      },
      data: {},
      // section_type: 'editor',
      // page_id: null,
      children: [] as Array<IBaseNode>,
    }
  }

  static defaultProperties(
    title: string,
    dataComponents?: Array<IPropertiesComponents> | null,
    basicComponents?: Array<IPropertiesComponents> | null,
    exclude: Array<string> = []
  ) {
    let more = [
      { type: 'PositionProperties', params: {} },
      { type: 'BackgroundProperties', params: {} },
      { type: 'BorderProperties', params: {} },
      { type: 'TextProperties', params: {} }
    ] as Array<any>;
    if (exclude && exclude.length > 0) {
      more = more.filter(cur => {
        return exclude.indexOf(cur.type) === -1
      });
    }

    const res = {
      title,
      hasTab: true,
      tabs: [
        {
          title: '基本信息',
          components: [
            ...more
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
              type: 'RowsProperties',
              params: {
                title: '布局设置',
                showInDisplayType: ['page'],
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
                  type: 'NoticeRow',
                  params: {
                    label: "适配模式需在预览时查看效果，编辑器中都是固定模式"
                  }
                }, {
                  type: 'NumberRow',
                  params: {
                    title: "页面宽度",
                    suffix: "px",
                    path: "config.pos.w"
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
                  type: 'NumberRow',
                  params: {
                    title: "高度",
                    type: "number",
                    suffix: "px",
                    path: "pos.h"
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
