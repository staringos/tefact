<template>
  <div>
    <div class="app-base-details">
      <div class="title-part">
        <AvatarUploader
          :size="100"
          :link="app.icon"
          :actionUrl="uploadUrl"
          @onChange="handleAvatarChanged"
        ></AvatarUploader>

        <h3>
          <a :href="`/light/${app.admin_route}`" class="app-title">{{app.title}}</a>
          <el-button type="text" size="small" icon="el-icon-edit" @click="handleDialogOpen" />
        </h3>
      </div>
      <div class="flex2">
        <AttributeList :attributes="attributes" />
      </div>

      <el-dialog
        title="应用基本信息编辑"
        :visible.sync="dialogVisible"
        :close-on-click-modal="false"
        :close-on-press-escape="false"
        width="30%">
        <el-form label-width="80px" :model="form">
          <el-form-item label="应用包名">
            <el-input v-model="form.name" disabled></el-input>
          </el-form-item>
          <el-form-item label="应用标题">
            <el-input v-model="form.title"></el-input>
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="form.description"></el-input>
          </el-form-item>
          <el-form-item label="排序">
            <el-input v-model="form.sort"></el-input>
          </el-form-item>
          <el-form-item label="key">
            <el-input v-model="form.key"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleSave()">确 定</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>
<style lang="scss" scoped>
  @import "../../../assets/styles/variables";

  .app-base-details {
    display: flex;

    .title-part {
      margin-right: 50px;
      justify-content: center;
      display: flex;
      flex-direction: column;

      h3 {
        margin-top: 10px;

        .app-title {
          color: $mainColor;
          text-decoration: none;
        }
      }
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop, Watch, namespace, Emit } from 'nuxt-property-decorator'

  const app = namespace("app")
  const system = namespace("system")

  @Component
  export default class AppDetails extends Vue {
    @Prop() app
    @Prop() onChange
    @app.Action modifyApp
    @system.Getter uploadUrl

    dialogVisible = false
    form = {} as any

    @Emit('change')
    public async handleSave() {
      await this.modifyApp({ id: this.app.id, app: this.form })
      this.dialogVisible = false
    }

    public async handleAvatarChanged(icon) {
      this.form.icon = icon;
      this.handleSave();
    }

    public async handleDialogOpen() {
      this.dialogVisible = true
    }

    get attributes() {
      return [
        { key: '应用包名', value: this.app.name },
        { key: '应用中文名', value: this.app.title },
        { key: '描述', value: this.app.description },
        { key: '后台路由', value: this.app.adminRoute },
        { key: '接口路由', value: this.app.apiRoute }]
    }

    public init() {
      if (!this.app) return

      this.form = {
        name: this.app.name,
        title: this.app.title,
        description: this.app.description,
        key: this.app.key,
        icon: this.app.icon
      }
    }

    @Watch('app')
    public handleAppChange() {
      this.init()
    }

    mounted() {
      this.init()
    }
  }
</script>
