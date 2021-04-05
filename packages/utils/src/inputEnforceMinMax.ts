const inputEnforceMinMax = (el: any) => {
  if (el.value != "") {
    if(parseInt(el.value) < parseInt(el.min)){
      el.value = el.min;
    }
    if(parseInt(el.value) > parseInt(el.max)){
      el.value = el.max;
    }
  }
}

export default inputEnforceMinMax
