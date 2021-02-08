import cloneDeep from 'lodash/cloneDeep'
import { IBaseNode, ITargetConfig } from "@tefact/core"

const ParamLengthReg = /width|height|size|radius/
const NotParamLengthReg = /background-size/

const transformStyle = (config: IBaseNode | ITargetConfig) => {
  if (!config) return {}

  const res = cloneDeep(config.style || {}) as any
  Object.keys(res).map(cur => {
    if (cur.match(ParamLengthReg) && !cur.match(NotParamLengthReg)) {
      res[cur] = `${res[cur]}px`
    }
  })

  if ((config as IBaseNode).pos) {
    const pos = (config as IBaseNode).pos;
    if (pos.h) res.height = `${pos.h}px`
    if (pos.w) res.width = `${pos.w}px`
  }
  return res
}

export default transformStyle;
