export default function verifyPhone(val: string) {
  const phone = /^((13[0-9])|(14[5,7,9])|(15[^4])|(18[0-9])|(17[0,1,3,5,6,7,8]))[0-9]{8}$/
  const ring = /^(\(\d{3,4}\)|\d{3,4}-|\s)?\d{7,14}$/
  return phone.test(val) || ring.test(val)
}
