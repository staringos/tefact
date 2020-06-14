<template>
  <div :class="(where === 'search' ? 'search-form' : '') + ' field-form'">
    <template v-for="(field, i) in entity.entity_fields">
      <el-form-item :label="field.name" :prop="field.key" :key="i" v-if="justifyIfExists(field)" :required="field.verify_require && where === 'modify'">
        <el-select v-if="field.data_type === 'dict'" v-model="form[field.key]" :placeholder="`请选择${field.name}`">
          <el-option v-for="(item, i) in field.dict_list" :key="i" :label="item.value" :value="item.key"></el-option>
        </el-select>
        <div v-else-if="(field.data_type === 'key_value' || field.data_type === 'foreign-key') && field.dict_list.length !== 2" >
          <el-select v-if="fieldOptions" v-model="form[field.key]" :placeholder="`请选择${field.name}`" :multiple="field.foreign_type === 'many-to-many'">
            <el-option v-for="(item, i) in fieldOptions[field.key]" :key="i" :label="item.value" :value="item.key"></el-option>
          </el-select>
        </div>
        <component v-else-if="field.data_type === 'global-component'" :is="field.form_component" :field="field" :row="form" @change="handleCustomComponentChange"></component>
        <el-switch v-else-if="field.data_type === 'boolean'" v-model="form[field.key]" inactive-text="否" active-text="是" :active-value="1" :inactive-value="0"></el-switch>
        <!--            <el-switch v-else-if="field.data_type === 'dict' && field.dict_list.length === 2" v-model="form[field.key]" :active-text="field.dict_list[0].value" :inactive-text="field.dict_list[1].value" :active-value="field.dict_list[0].key" :inactive-value="field.dict_list[1].key"></el-switch>-->
        <el-date-picker v-else-if="date_type.indexOf(field.data_type) !== -1" placeholder="选择时间" v-model="form[field.key]" :type="field.data_type" value-format="timestamp"></el-date-picker>
        <el-input-number v-else-if="field.data_type === 'number'" v-model="form[field.key]" controls-position="right"></el-input-number>
        <el-input v-else-if="field.data_type === 'text-area'" type="textarea" v-model="form[field.key]"></el-input>
        <Editor api-key="6qz693srcr57q01vyzi8l8lgxh2jwf14sy402ikj6nkppcff" v-else-if="field.data_type === 'rich_text'" v-model="form[field.key]" :init="richEditorConfig" ></Editor>
        <el-input v-else v-model="form[field.key]"></el-input>
      </el-form-item>
    </template>
  </div>
</template>
<style lang="scss">
  .field-form {
    .search-form {
    }
  }

  .tox {
    &.tox-silver-sink {
      z-index: 3999;
    }
  }
</style>
<script lang="ts">
  import { Component, Vue, Prop, Emit, Watch, namespace } from 'nuxt-property-decorator'
  import { EntityField, Entity } from '~/services/common'
  import { deepCopy } from '~/utils'
  import Editor from '@tinymce/tinymce-vue'
  import { auth } from '~/utils'

  const entities = namespace('entities')
  const app = namespace('app')

  const imageUploadUrl = process.env.ARRPLAT_BASE_URL + '/core/upload-files/arrplat'

  @Component({
    components: { Editor }
  })
  export default class Search extends Vue {
    @Prop(Object) entity!: Entity
    @Prop(Object) field!: EntityField
    @Prop() form
    @Prop({ default: 'modify' }) where

    @entities.Action getEditorOptions
    @app.Getter currentOrgIdGetter

    date_type: string[] = ['date', 'time', 'datetime']
    tmpForm: any = {}
    fieldOptions: any = null
    richEditorConfig = {
      menubar: false,
      toolbar: `styleselect | fontselect | formatselect | fontsizeselect | forecolor backcolor | bold italic underline strikethrough | image  media | table | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist | preview removeformat  hr | paste code  link | undo redo | fullscreen `,
      plugins: `
        paste
        image
      `,
      selector: "textarea",
      automatic_uploads: true,
      images_reuse_filename: true,
      images_upload_handler: function(blobInfo, success, failure) {
        let xhr = new XMLHttpRequest(), formData = new FormData()
        xhr.withCredentials = false
        xhr.open('POST', imageUploadUrl)
        xhr.setRequestHeader('Authorization', `Bearer ${auth.getToken()}`)
        formData.append('file', blobInfo.blob())
        xhr.onload = function(res) {
            let json;

            if (xhr.status != 200)
              return failure('HTTP Error: ' + xhr.status);

            json = JSON.parse(xhr.responseText);

            if (!json || typeof json[0] != 'string')
              return failure('Invalid JSON: ' + xhr.responseText);

            success(`http://${json[0]}`)
        }
        xhr.send(formData)
        return
      }
    }


    justifyIfExists(field) {
      if (this.where === 'modify')
        return field.exists_type.indexOf('modify') !== -1

      return field.has_search
    }

    async initOptionsData() {
      const res = await this.getEditorOptions({ entityId: this.entity.id, orgId: this.currentOrgIdGetter })
      this.fieldOptions = res.data.data
    }

    @Watch('tmpForm')
    @Emit('change')
    onTmpFormChanged() {

    }

    @Emit('change')
    handleCustomComponentChange(data) {
      return { ...this.form, ...data }
    }

    mounted() {
      if (!this.fieldOptions) {
        this.initOptionsData()
      }
    }
  }
</script>
