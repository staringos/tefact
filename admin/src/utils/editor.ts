import cloneDeep from 'lodash/cloneDeep'

const ParamLengthReg = /width|height|size/

export const transformStyle = styles => {
  if (!styles) return {}
  const res = cloneDeep(styles)
  Object.keys(res).map(cur => {
    if (cur.match(ParamLengthReg)) {
      res[cur] = `${res[cur]}px`
    }
  })
  return res;
}
