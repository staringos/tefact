var render = function() {
  var _vm = this;
  var _h = _vm.$createElement;
  var _c = _vm._self._c || _h;
  return _c(
    'div',
    {
      class: ("panel " + (_vm.border && 'panel-bordered') + " " + (_vm.header && "panel-headed"))
    },
    [(_vm.title) ?
      _vm._ssrNode("<div class=\"panel-title\">", "</div>",
        [
          _vm._ssrNode(
            _vm._ssrEscape("\n    " + _vm._s(_vm.title) + "\n    ")
          ),
          (_vm.headerButton) ?
            _c('el-button', {
              staticClass: "create-btn",
              attrs: {
                "icon": _vm.headerButton,
                "circle": "",
                "size": "mini"
              },
              on: {
                "click": _vm.handleHeaderButtonClick
              }
            })
            : _vm._e()
        ], 2
      )
      : _vm._e(), _vm._ssrNode("<div" + (_vm._ssrClass(null, ("panel-content " + (_vm.noPadding && "panel-no-padding")))) + ">", "</div>", [_vm._t("default")], 2)]
  )
}
