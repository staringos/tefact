import isObjectLike from "./isObjectLike"
import getTag from "./getTag"

function isNumber(value: any) {
  return typeof value === 'number' ||
    (isObjectLike(value) && getTag(value) == '[object Number]')
}
export default isNumber
