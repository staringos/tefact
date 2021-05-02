<template>
  <BasePanel class="page-panel" title="页面">
    <div class="page-panel-content">
      <el-card
        v-for="target in targetList"
        :key="target.id"
        class="page-item"
        :body-style="{ padding: '0px' }"
        @click.native="handleCardClick(target)"
      >
        <img class="head-image" v-if="target.head_image" :src="target.head_image"/>
        <i v-else-if="target.display_type === 'form'" class="head-image tefact-icon tf-icon-icon-Platformlog"></i>
        <i v-else-if="target.display_type.indexOf('h5') !== -1" class="head-image tefact-icon tf-icon-phone"></i>
        <i v-else class="head-image tefact-icon tf-icon-pages"></i>
        <div class="page-item-content">
          <span>{{ target.title }}</span>
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
    cursor: pointer;

    .tefact-icon {
      height: 170px;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 170px;
      margin-top: 10px;
      margin-left: 10px;
      color: #38b0e4;
    }
  }

  .page-item {
    height: 220px;
    max-height: 220px;
    margin-bottom: 5px;
    padding-right: 5px;

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
import { BaseView, ITarget } from "@tefact/core";

@Component({
  components: { BasePanel },
})
export default class PagePanel extends BaseView {
  targetList = null as null | Array<ITarget>;

  handleCardClick(target) {
    location.href = `/app/light/${target.application_id}/${target.id}/editor`
  }

  async mounted() {
    const { onGetTargetList } = this.setting;
    if (!onGetTargetList) {
      return
    }
    this.targetList = await onGetTargetList()
  }
}
</script>
