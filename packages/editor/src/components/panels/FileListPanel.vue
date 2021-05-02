<template>
  <BasePanel class="config-panel" title="配置">
    <ul class="file-list">
      <li class="file-item" v-for="(item) in list" :key="item.id">
        <img :src="`https://${item.path + '?imageView2/0/w/70'}`" />
        <i class="el-icon-delete"></i>
      </li>
    </ul>
  </BasePanel>
</template>
<style lang="scss" scoped>
.file-list {
  display: flex;
  flex-direction: row;
  flex-flow: row wrap;
  margin: 5px 0 0 5px;

  .file-item {
    width: 70px;
    min-height: 50px;
    border-radius: 3px;
    margin-right: 5px;
    list-style: none;
    position: relative;
    cursor: pointer;

    img {
      width: 70px;
      min-height: 50px;
    }
  }

  .el-icon-delete {
    display: none;
  }

  .file-item:hover {
    .el-icon-delete {
      display: block;
      position: absolute;
      top: 1px;
      right: 1px;
      width: 20px;
      text-align: center;
      height: 20px;
      background: white;
      font-size: 12px;
      border-bottom-left-radius: 50%;
      line-height: 20px;
      color: #333;
    }
  }
}
</style>
<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import BasePanel from "TEFACT_EDITOR/components/panels/BasePanel.vue";
import {BaseView, IFile} from "@tefact/core";

@Component({
  components: {
    BasePanel
  }
})
export default class FileListPanel extends BaseView {
  list = [] as Array<IFile>;

  async mounted() {
    if (!this.setting.onGetFileList) return;
    this.list = (await this.setting.onGetFileList());
  }
}
</script>