import { Vue } from 'nuxt-property-decorator'

// Vue.use(Element)

export default () => {
  Vue.component('ElButton', () => import(/* webpackChunkName: 'element-ui-button' */ 'element-ui/lib/button'))
  Vue.component('ElSlider', () => import(/* webpackChunkName: 'element-ui-slider' */ 'element-ui/lib/slider'))
  Vue.component('ElPagination', () => import(/* webpackChunkName: 'element-ui-pagination' */ 'element-ui/lib/pagination'))
  Vue.component('ElDropdown', () => import(/* webpackChunkName: 'element-ui-dropdown' */ 'element-ui/lib/dropdown'))
  Vue.component('ElDropdownItem', () => import(/* webpackChunkName: 'element-ui-dropdown-item' */ 'element-ui/lib/dropdown-item'))
  Vue.component('ElDropdownMenu', () => import(/* webpackChunkName: 'element-ui-dropdown-menu' */ 'element-ui/lib/dropdown-menu'))
  Vue.component('ElMenu', () => import(/* webpackChunkName: 'element-ui-menu' */ 'element-ui/lib/menu'))
  Vue.component('ElMenuItem', () => import(/* webpackChunkName: 'element-ui-menu-item' */ 'element-ui/lib/menu-item'))
  Vue.component('ElMenuItemGroup', () => import(/* webpackChunkName: 'element-ui-menu-item-group' */ 'element-ui/lib/menu-item-group'))
  Vue.component('ElSubmenu', () => import(/* webpackChunkName: 'element-ui-submenu' */ 'element-ui/lib/submenu'))
  Vue.component('ElInput', () => import(/* webpackChunkName: 'element-ui-input' */ 'element-ui/lib/input'))
  Vue.component('ElInputNumber', () => import(/* webpackChunkName: 'element-ui-input-number' */ 'element-ui/lib/input-number'))
  Vue.component('ElForm', () => import(/* webpackChunkName: 'element-ui-form' */ 'element-ui/lib/form'))
  Vue.component('ElFormItem', () => import(/* webpackChunkName: 'element-ui-form-item' */ 'element-ui/lib/form-item'))
  Vue.component('ElOption', () => import(/* webpackChunkName: 'element-ui-option' */ 'element-ui/lib/option'))
  Vue.component('ElSelect', () => import(/* webpackChunkName: 'element-ui-select' */ 'element-ui/lib/select'))
  Vue.component('ElTimeSelect', () => import(/* webpackChunkName: 'element-ui-time-select' */ 'element-ui/lib/time-select'))
  Vue.component('ElRadio', () => import(/* webpackChunkName: 'element-ui-radio' */ 'element-ui/lib/radio'))
  Vue.component('ElContainer', () => import(/* webpackChunkName: 'element-ui-container' */ 'element-ui/lib/container'))
  Vue.component('ElRow', () => import(/* webpackChunkName: 'element-ui-row' */ 'element-ui/lib/row'))
  Vue.component('ElCol', () => import(/* webpackChunkName: 'element-ui-col' */ 'element-ui/lib/col'))
  Vue.component('ElUpload', () => import(/* webpackChunkName: 'element-ui-upload' */ 'element-ui/lib/upload'))
  Vue.component('ElCheckbox', () => import(/* webpackChunkName: 'element-ui-checkbox' */ 'element-ui/lib/checkbox'))
  Vue.component('ElCheckboxButton', () => import(/* webpackChunkName: 'element-ui-checkbox-button' */ 'element-ui/lib/checkbox-button'))
  Vue.component('ElTabs', () => import(/* webpackChunkName: 'element-ui-tabs' */ 'element-ui/lib/tabs'))
  Vue.component('ElTabPane', () => import(/* webpackChunkName: 'element-ui-tab-pane' */ 'element-ui/lib/tab-pane'))
  Vue.component('ElCard', () => import(/* webpackChunkName: 'element-ui-card' */ 'element-ui/lib/card'))
  Vue.component('ElTag', () => import(/* webpackChunkName: 'element-ui-tag' */ 'element-ui/lib/tag'))
  Vue.component('ElTable', () => import(/* webpackChunkName: 'element-ui-table' */ 'element-ui/lib/table'))
  Vue.component('ElTableColumn', () => import(/* webpackChunkName: 'element-ui-table-column' */ 'element-ui/lib/table-column'))
  Vue.component('ElButton', () => import(/* webpackChunkName: 'element-ui-button' */ 'element-ui/lib/button'))
  Vue.component('ElAvatar', () => import(/* webpackChunkName: 'element-ui-avatar' */ 'element-ui/lib/avatar'))
  Vue.component('ElDialog', () => import(/* webpackChunkName: 'element-ui-dialog' */ 'element-ui/lib/dialog'))
  Vue.component('ElPopover', () => import(/* webpackChunkName: 'element-ui-popover' */ 'element-ui/lib/popover'))
  Vue.component('ElBadge', () => import(/* webpackChunkName: 'element-ui-badge' */ 'element-ui/lib/badge'))
  Vue.component('ElTooltip', () => import(/* webpackChunkName: 'element-ui-tooltip' */ 'element-ui/lib/tooltip'))
  Vue.component('ElButtonGroup', () => import(/* webpackChunkName: 'element-ui-button-group' */ 'element-ui/lib/button-group'))
  Vue.component('ElColorPicker', () => import(/* webpackChunkName: 'element-ui-color-picker' */ 'element-ui/lib/color-picker'))
  Vue.component('ElCollapse', () => import(/* webpackChunkName: 'element-ui-collapse' */ 'element-ui/lib/collapse'))
  Vue.component('ElCollapseItem', () => import(/* webpackChunkName: 'element-ui-collapse-item' */ 'element-ui/lib/collapse-item'))
  Vue.component('ElPopconfirm', () => import(/* webpackChunkName: 'element-ui-popconfirm' */ 'element-ui/lib/popconfirm'))
  Vue.component('ElCarousel', () => import(/* webpackChunkName: 'element-ui-carousel' */ 'element-ui/lib/carousel'))
  Vue.component('ElCarouselItem', () => import(/* webpackChunkName: 'element-ui-carousel-item' */ 'element-ui/lib/carousel-item'))
  Vue.component('ElCollapseTransition', () => import(/* webpackChunkName: 'element-ui-collapse-transition' */ 'element-ui/lib/transitions/collapse-transition'))
  Vue.component('ElLink', () => import(/* webpackChunkName: 'element-ui-link' */ 'element-ui/lib/link'))
}

// import { Vue } from 'nuxt-property-decorator'
// import {
//   Pagination,
//   Dialog,
//   Dropdown,
//   DropdownMenu,
//   DropdownItem,
//   Menu,
//   Submenu,
//   MenuItem,
//   MenuItemGroup,
//   Input,
//   InputNumber,
//   Radio,
//   RadioGroup,
//   RadioButton,
//   Checkbox,
//   CheckboxButton,
//   CheckboxGroup,
//   Switch,
//   Select,
//   Option,
//   OptionGroup,
//   Button,
//   ButtonGroup,
//   Table,
//   TableColumn,
//   DatePicker,
//   TimeSelect,
//   TimePicker,
//   Popover,
//   Tooltip,
//   Form,
//   FormItem,
//   Tabs,
//   TabPane,
//   Alert,
//   Slider,
//   Icon,
//   Row,
//   Col,
//   Upload,
//   Badge,
//   Collapse,
//   CollapseItem,
//   ColorPicker,
//   Loading,
//   MessageBox,
//   Message
// } from 'element-ui';
//
// Vue.use(Pagination);
// Vue.use(Dialog);
// Vue.use(Dropdown);
// Vue.use(DropdownMenu);
// Vue.use(DropdownItem);
// Vue.use(Menu);
// Vue.use(Submenu);
// Vue.use(MenuItem);
// Vue.use(MenuItemGroup);
// Vue.use(Input);
// Vue.use(InputNumber);
// Vue.use(Radio);
// Vue.use(RadioGroup);
// Vue.use(RadioButton);
// Vue.use(Checkbox);
// Vue.use(CheckboxButton);
// Vue.use(CheckboxGroup);
// Vue.use(Switch);
// Vue.use(Select);
// Vue.use(Option);
// Vue.use(OptionGroup);
// Vue.use(Button);
// Vue.use(ButtonGroup);
// Vue.use(Table);
// Vue.use(TableColumn);
// Vue.use(DatePicker);
// Vue.use(TimeSelect);
// Vue.use(TimePicker);
// Vue.use(Popover);
// Vue.use(Tooltip);
// Vue.use(Form);
// Vue.use(FormItem);
// Vue.use(Tabs);
// Vue.use(TabPane);
// Vue.use(Alert);
// Vue.use(Slider);
// Vue.use(Icon);
// Vue.use(Row);
// Vue.use(Col);
// Vue.use(Upload);
// Vue.use(Badge);
// Vue.use(Collapse);
// Vue.use(CollapseItem);
// Vue.use(ColorPicker);
//
// Vue.use(Loading.directive);
//

import { Loading } from "element-ui";
import { Message } from "element-ui";
import { MessageBox } from "element-ui";

Vue.prototype.$loading = Loading.service;
Vue.prototype.$alert = MessageBox.alert;
Vue.prototype.$confirm = MessageBox.confirm;
Vue.prototype.$message = Message;
