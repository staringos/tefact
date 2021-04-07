import cloneDeep from 'lodash/cloneDeep'
import isNumber from 'lodash/isNumber'
import type { IBaseNode, ITargetConfig } from "@tefact/core"

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
    if (pos.h) res.height = isNumber(pos.h) ? `${pos.h}px` : pos.h;
    if (pos.w) res.width = isNumber(pos.w) ? `${pos.w}px` : pos.w;
  }

  return res
}

export default transformStyle;
