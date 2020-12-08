<template>
  <div class="editor-wrapper" v-if="currentPage" @click="resetActive">
    <div class="editor-container">
      <Toolbar :page="currentPage" :editorSetting="editorSetting" :editorType="editorType"></Toolbar>
      <div class="editor-main">
        <NodeList :editorType="editorType" />
        <div class="editor-container">
          <div class="page-pad">
            <Page :page="currentPage" :pageId="pageId" />
          </div>
        </div>
      </div>
    </div>
    <Sidebar />
  </div>
</template>
<style lang="scss" scoped>
  @import "../../../../../assets/styles/variables";

  .editor-wrapper {
    display: flex;
    flex: 1;
    overflow: hidden;

    .editor-container {
      background: #f0f2f5;
      flex: 3;
      display: flex;
      flex-direction: column;

      .editor {
        flex: 1;
        overflow: auto;
      }

      .editor-main {
        -webkit-box-flex: 1;
        flex-grow: 1;
        display: flex;
        overflow: auto;
        flex-direction: row;
        padding: 0;

        .editor-container {
          flex-grow: 1;
          overflow: auto;
          flex-direction: row;
          padding: 20px 20px 0 20px;
          width: 0;

          .page-pad {
            padding-right: 20px;
            flex: 1;
          }
        }
      }
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, namespace } from 'nuxt-property-decorator'
  import Page from '~/components/app/light/editor/Page.vue'
  import Toolbar from '~/components/app/light/editor/Toolbar.vue'
  import NodeList from '~/components/app/light/editor/NodeList.vue';
  import Sidebar from '~/components/app/light/editor/Sidebar.vue';

  const editor = namespace('editor')

  @Component({
    layout: 'UserAdmin',
    components: { Sidebar, NodeList, Page, Toolbar }
  })
  export default class EditorPage extends Vue {
    page = {
      title: '这是一个新页面'
    }

    @editor.Action getPageDetails
    @editor.Action resetActive
    @editor.Getter currentPage
    @editor.Getter currentNode
    pageId: string | null = null

    editorSetting = {
      device: 'pc'
    }

    get editorType() {
      console.log("currentPage:", this.currentPage)
      if (this.currentNode && this.currentNode.type === 'FormNode') {
        return 'form'
      }

      if (this.editorSetting.device) {
        return this.editorSetting.device
      }

      return 'pc'
    }

    init(pageId) {
      this.getPageDetails(pageId)
    }

    async mounted() {
      this.pageId = this.$route.params.page_id
      await this.init(this.pageId)
    }
  }
</script>
