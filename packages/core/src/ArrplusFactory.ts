import { createRoutes } from '@nuxt/utils'
import Glob from 'glob'
import pify from 'pify'
import { Route } from '@arrplat/common'
import { ArrplusConfig, ArrplusOptions, PluginOptions, PlusConfig } from '@arrplat/common'
import _ from 'lodash'

const fs = require('fs-extra')
const path = require('path')
const glob = pify(Glob)

const defaultPlusConfig = {
  name: '',
  description: '',
  icon: '',
  apiRoute: '',
  globalComponents: [],
  adminRoute: '',
  entities: [],
  pages: [],
  menus: []
} as PlusConfig

// tslint:disable-next-line:variable-name
const _defaultConfig: ArrplusConfig = {
  plusDir: path.join(__dirname, '../../../', 'plugins/'),
  routeNameSplitter: '-',
  dir: {
    pages: 'admin/pages',
  },
  plus: [],
}

export default class ArrplusFactory {
  constructor(config: ArrplusConfig) {
    this.config = {
      ..._defaultConfig,
      ...config,
    }

    this.options = {
      ...ArrplusFactory._defaultOptions,
      ...this.config,
      plus: [],
    } as ArrplusOptions
  }

  public static _defaultConfig: ArrplusConfig = _defaultConfig
  // tslint:disable-next-line:variable-name
  public static _defaultOptions: ArrplusOptions = {
    ..._defaultConfig,
    plus: [],
  }

  public config: ArrplusConfig
  public options: ArrplusOptions
  public supportedExtensions: string[] = ['vue']

  public globPathWithExtensions(p) {
    return `${p}/**/*.vue`
  }

  public async resolveFiles(dir, cwd = this.options.plusDir) {
    return await glob(this.globPathWithExtensions(dir), {
      cwd,
      ignore: [],
      follow: false,
    })
  }

  public static async load(config: ArrplusConfig) {
    const factory = new ArrplusFactory(config)

    await Promise.all(factory.config.plus.map(async plugin => {
      const newConfig = await factory.loadPluginsConfig(plugin)
      const globalComponents = await factory.loadGlobalComponents(plugin, newConfig.name)

      const options = {
        ...newConfig,
        path: plugin,
        globalComponents,
      } as PluginOptions

      options.routes = await factory.generateRoutes(options)
      factory.options.plus.push(options)
    }))

    factory.options.plus = _.sortBy(factory.options.plus, (item) => item.sort || 10)
    return factory
  }

  public async loadGlobalComponents(plugin, name) {
    const configPath = path.join(this.config.plusDir, plugin, '/admin/components/global')
    if (fs.existsSync(configPath)) {
      const readDir = fs.readdirSync(configPath)
      const components = []

      readDir.map(current => {
        if (current.indexOf('.vue') === -1) return
        components.push({
          name: `${plugin}-${current.split('.')[0].toLowerCase()}`,
          path: `${name}/admin/components/global/${current}`
        })
      })

      return components
    }

    return []
  }

  public async loadPluginsConfig(plugin) {
    let option = {} as PlusConfig

    const defaultConfig = {
      ...defaultPlusConfig,
      name: plugin,
      description: plugin,
      icon: plugin,
      apiRoute: plugin,
      adminRoute: plugin,
    }

    try {
      const configPath = path.join(this.config.plusDir, plugin, '/arrplus.config.json')

      if (fs.existsSync(configPath)) {
        const files = JSON.parse(fs.readFileSync(configPath, 'utf-8'))

        option = {
          ...defaultConfig,
          ...files,
        } as PlusConfig
      } else {
        option = {
          ...defaultConfig,
        } as PlusConfig
      }
    } catch(e) {
      option = {
        ...defaultConfig,
      } as PlusConfig
    }

    return option
  }

  public async generateRoutes(plugin) {
    const files = {}
    const pluginPageDir = path.join(plugin.path, '/admin/pages')
    const ext = new RegExp(`\\.(${this.supportedExtensions.join('|')})$`)

    for (const page of await this.resolveFiles(pluginPageDir)) {
      const key = page.replace(ext, '')
      if (/\.vue$/.test(page) || !files[key]) {
        files[key] = page.replace(/(['"])/g, '\\$1')
      }
    }

    const routes: Route[] = await createRoutes({
      files: Object.values(files),
      srcDir: '/',
      pagesDir: this.options.dir ? this.options.dir.pages : '',
      routeNameSplitter: this.options.routeNameSplitter,
      supportedExtensions: this.supportedExtensions,
      trailingSlash: undefined,
    }).map(router => {
      const res = { ...router }
      res.name = `plugins-${plugin.adminRoute}${router.name.replace('admin-pages', '')}`
      res.path = `/plugins/${plugin.adminRoute}${router.path.replace('/admin/pages', '')}`

      // Components need to be installed
      res.component = res.component.replace(`/${plugin.path}`, `${plugin.name}`)

      return res
    })

    return routes
  }
}
