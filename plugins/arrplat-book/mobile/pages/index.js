(wx["webpackJsonp"] = wx["webpackJsonp"] || []).push([["../../../plugins/arrplat-crm/mobile/pages/index"],{

/***/ "../../plugins/arrplat-crm/mobile/pages/index.tsx":
/*!********************************************************************************************************************!*\
  !*** /Users/zousongqi/Documents/WORK/Arrway/ArrwayCloud/arrplat-python/plugins/arrplat-crm/mobile/pages/index.tsx ***!
  \********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _taroWeapp = __webpack_require__(/*! @tarojs/taro-weapp */ "../../node_modules/@tarojs/taro-weapp/index.js");

var _taroWeapp2 = _interopRequireDefault(_taroWeapp);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var UserDetailsPage = function (_Taro$Component) {
  _inherits(UserDetailsPage, _Taro$Component);

  function UserDetailsPage() {
    _classCallCheck(this, UserDetailsPage);

    var _this = _possibleConstructorReturn(this, (UserDetailsPage.__proto__ || Object.getPrototypeOf(UserDetailsPage)).apply(this, arguments));

    _this.$usedState = ["id"];
    _this.customComponents = [];
    return _this;
  }

  _createClass(UserDetailsPage, [{
    key: "_constructor",
    value: function _constructor(props) {
      _get(UserDetailsPage.prototype.__proto__ || Object.getPrototypeOf(UserDetailsPage.prototype), "_constructor", this).call(this, props);
      this.$$refs = new _taroWeapp2.default.RefsArray();
    }
  }, {
    key: "_createData",
    value: function _createData() {
      this.__state = arguments[0] || this.state || {};
      this.__props = arguments[1] || this.props || {};
      var __isRunloopRef = arguments[2];
      var __prefix = this.$prefix;
      ;
      var id = this.__props.id;

      Object.assign(this.__state, {
        id: id
      });
      return this.__state;
    }
  }]);

  return UserDetailsPage;
}(_taroWeapp2.default.Component);

UserDetailsPage.$$events = [];
UserDetailsPage.$$componentPath = "Users/zousongqi/Documents/WORK/Arrway/ArrwayCloud/arrplat-python/plugins/arrplat-crm/mobile/pages/index";
exports.default = UserDetailsPage;

Component(__webpack_require__(/*! @tarojs/taro-weapp */ "../../node_modules/@tarojs/taro-weapp/index.js").default.createComponent(UserDetailsPage, true));

/***/ })

},[["../../plugins/arrplat-crm/mobile/pages/index.tsx","runtime","vendors"]]]);