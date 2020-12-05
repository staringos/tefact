import { Vue } from 'nuxt-property-decorator'
// import Element from 'element-ui'

// Vue.use(Element)

export default () => {
  Vue.component('ElButton', () => import('element-ui/lib/button'))
  Vue.component('ElSlider', () => import('element-ui/lib/slider'))
  Vue.component('ElPagination', () => import('element-ui/lib/pagination'))
  Vue.component('ElDropdown', () => import('element-ui/lib/dropdown'))
  Vue.component('ElDropdownItem', () => import('element-ui/lib/dropdown-item'))
  Vue.component('ElDropdownMenu', () => import('element-ui/lib/dropdown-menu'))
  Vue.component('ElMenu', () => import('element-ui/lib/menu'))
  Vue.component('ElMenuItem', () => import('element-ui/lib/menu-item'))
  Vue.component('ElMenuItemGroup', () => import('element-ui/lib/menu-item-group'))
  Vue.component('ElSubmenu', () => import('element-ui/lib/submenu'))
  Vue.component('ElInput', () => import('element-ui/lib/input'))
  Vue.component('ElInputNumber', () => import('element-ui/lib/input-number'))
  Vue.component('ElForm', () => import('element-ui/lib/form'))
  Vue.component('ElFormItem', () => import('element-ui/lib/form-item'))
  Vue.component('ElOption', () => import('element-ui/lib/option'))
  Vue.component('ElSelect', () => import('element-ui/lib/select'))
  Vue.component('ElTimeSelect', () => import('element-ui/lib/time-select'))
  Vue.component('ElRadio', () => import('element-ui/lib/radio'))
  Vue.component('ElContainer', () => import('element-ui/lib/container'))
  Vue.component('ElRow', () => import('element-ui/lib/row'))
  Vue.component('ElCol', () => import('element-ui/lib/col'))
  Vue.component('ElUpload', () => import('element-ui/lib/upload'))
  Vue.component('ElCheckbox', () => import('element-ui/lib/checkbox'))
  Vue.component('ElCheckboxButton', () => import('element-ui/lib/checkbox-button'))
  Vue.component('ElTabs', () => import('element-ui/lib/tabs'))
  Vue.component('ElTabPane', () => import('element-ui/lib/tab-pane'))
  Vue.component('ElCard', () => import('element-ui/lib/card'))
  Vue.component('ElTag', () => import('element-ui/lib/tag'))
  Vue.component('ElTable', () => import('element-ui/lib/table'))
  Vue.component('ElTableColumn', () => import('element-ui/lib/table-column'))
  Vue.component('ElButton', () => import('element-ui/lib/button'))
  Vue.component('ElAvatar', () => import('element-ui/lib/avatar'))
  Vue.component('ElDialog', () => import('element-ui/lib/dialog'))
  Vue.component('ElPopover', () => import('element-ui/lib/popover'))
  Vue.component('ElBadge', () => import('element-ui/lib/badge'))
  Vue.component('ElTooltip', () => import('element-ui/lib/tooltip'))
  Vue.component('ElButtonGroup', () => import('element-ui/lib/button-group'))
  Vue.component('ElColorPicker', () => import('element-ui/lib/color-picker'))
  Vue.component('ElCollapse', () => import('element-ui/lib/collapse'))
  Vue.component('ElCollapseItem', () => import('element-ui/lib/collapse-item'))
  Vue.component('ElPopconfirm', () => import('element-ui/lib/popconfirm'))
  Vue.component('ElCarousel', () => import('element-ui/lib/carousel'))
  Vue.component('ElCarouselItem', () => import('element-ui/lib/carousel-item'))
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
