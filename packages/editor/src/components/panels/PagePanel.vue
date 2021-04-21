<template>
  <BasePanel class="page-panel" title="页面">
    <div class="page-panel-content">
      <el-card class="page-item" :body-style="{ padding: '0px' }">
        <img src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png" class="image">
        <div class="page-item-content">
          <span>好吃的汉堡</span>
        </div>
      </el-card>
      <el-card class="page-item" :body-style="{ padding: '0px' }">
        <img src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png" class="image">
        <div class="page-item-content">
          <span>好吃的汉堡</span>
        </div>
      </el-card>
    </div>
  </BasePanel>
</template>
<style lang="scss" scoped>
.page-panel {
  display: flex;
  flex: 1;
  height: 100%;
  overflow-y: auto;

  .page-panel-content {
    padding: 5px;
  }

  .page-item {
    height: 220px;
    max-height: 220px;
    margin-bottom: 5px;

    .image {
      width: 100%;
      height: 180px;
    }

    .page-item-content {
      font-size: 14px;
      padding: 5px 10px 10px 10px;
    }
  }
}
</style>
<script lang="ts">
import { Component } from "vue-property-decorator";
import BasePanel from "./BasePanel.vue";
import {BaseView} from "../../../../core";

@Component({
  components: { BasePanel },
})
export default class PagePanel extends BaseView {

}
</script>