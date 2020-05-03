<template>
  <div class="editor-toolbar">
    <i class="el-icon-arrow-left"></i>
    <div class="page-title">
      {{page.title}}
      <i class="el-icon-edit"></i>
    </div>

    <div class="tool-list">
      <el-button type="info" icon="el-icon-receiving" size="small" @click="handleSavePage">保存</el-button>
      <el-button type="info" icon="el-icon-back" size="small">上一步</el-button>
      <el-button type="info" icon="el-icon-right" size="small">下一步</el-button>
      <el-button type="info" icon="el-icon-data-analysis" size="small">预览</el-button>
      <el-button type="info" icon="el-icon-share" size="small">发布</el-button>
    </div>

    <div class="right-button">
      <el-button-group>
        <el-button v-for="device in deviceList" :type="editorSetting.device === device.value ? 'primary' : 'default'" size="small" @click="handleSelectDevices(device)">
          <i :class="`tefact-icon ${device.icon}`"></i>
        </el-button>
      </el-button-group>
    </div>
  </div>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, Prop, namespace } from 'nuxt-property-decorator'

  const editor = namespace('editor')

  @Component
  export default class Toolbar extends Vue {
    @Prop([Object]) page
    @Prop([Object]) editorSetting

    @editor.Action savePageDetails

    deviceList = [
      { icon: 'tf-icon-pc', name: 'PC', value: 'pc' },
      { icon: 'tf-icon-mobile-phone', name: 'h5', value: 'h5' },
    ]

    async handleSavePage() {
      const res = await this.savePageDetails()
      if (res.status === 200) {
        return this.$message({
          showClose: true,
          message: '页面保存成功！',
          type: 'success'
        });
      }

      this.$message({
        showClose: true,
        message: `页面保存失败：${res.data.message}`,
        type: 'success'
      });
    }

    handleSelectDevices(device) {
      this.$emit('editorSettingChange', { ...this.editorSetting, device: device.value })
    }
  }
</script>
<style lang="scss">
  @import "../../../../assets/styles/variables";

  .editor-toolbar {
    display: flex;
    align-items: center;

    .page-title {
      margin: 0 10px;
      cursor: pointer;

      &:hover {
        color: $editor-main-color;
      }
    }

    .tool-list {
      flex: 1;
      display: flex;
      justify-content: center;

      .el-button {
        border: 0;
        background: none;
        color: $editor-text-color;

        &:hover {
          color: $editor-text-active-color;
        }
      }
    }

    .right-button {
      float: right;
    }
  }

  .editor-toolbar {
    height: 32px;
    padding: 10px;
    background-color: white;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.12), 0 0 6px 0 rgba(0,0,0,.04);
  }
</style>
