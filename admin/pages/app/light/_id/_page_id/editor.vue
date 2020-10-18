<template>
  <div class="editor-wrapper" v-if="currentPage" @click="resetActive">
    <div class="editor-container">
      <Toolbar :page="page" :editorSetting="editorSetting"></Toolbar>
      <div class="editor-main">
        <NodeList />
        <div class="editor-container">
          <Page :page="currentPage" :pageId="pageId" />
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
        padding: 20px 20px 20px 20px;

        .editor-container {
          flex-grow: 1;
          overflow: auto;
          flex-direction: row;
          padding: 20px 20px 20px 20px;
          margin-left: 100px;
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
    pageId: string | null = null

    editorSetting = {
      device: 'pc',
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
