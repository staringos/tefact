import { PROPERTIES as formsProperties, NodeList as formNodes } from '@tefact/feature-form'
import { PROPERTIES as pageProperties, NodeList as pageNodes } from '@tefact/feature-page'

export const PROPERTIES_CONFIGS = { ...formsProperties, ...pageProperties }
export const FORM_NODE_LIST = formNodes
export const PAGE_NODE_LIST = pageNodes

// TODO className | customStyle
export const FixedTabs = [
    {
        title: "样式定制",
        components: [
            {

            }
        ]
    }
]