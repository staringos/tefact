import json
import importlib.util
import os
import time

from flask_script import Command
from jinja2.utils import import_string

from arrplat.resources.application.models import Application, ApplicationMenus
from arrplat.resources.page.models import Page, PageSection, Entity, EntityField, Button, EntityFieldButton
from arrplat.config import basedir
from extensions import db


class SetupPlugins(object):
    def __init__(self):
        self.plugins_config_file = '.arrplat.json'
        self.base_path = basedir
        self.plugins_path = self.plugins_info()['plus_base_path']
        # self.source_venv = os.system(f'source {basedir}/venv/bin/activate')

    def install_dependency(self):
        """
        安装依赖
        扫描plugins下所有文件夹，判断每个插件是否有req.txt文件 如果有就需要安装req.txt依赖
        :return:
        """
        plugins = os.listdir(self.plugins_path)
        for plugin in plugins:
            each_path = f'{self.plugins_path}{plugin}'
            if 'requirements.txt' in os.listdir(each_path):
                os.system(f'pip install -r {each_path}/requirements.txt')

    def install_blueprint(self, app):
        """
          批量导入蓝图，注册蓝图
              遍历所有的文件夹
              再拼接字符串，利用import_string导入蓝图
              最后再注册蓝图
        """

        for plugin in self.plugins_info()['plus_list']:
            # 加载目录
            plugin_path_dir_list = [i for i in os.listdir(self.plugins_path + plugin['path']) if "." not in i]
            for plugin_path_dir in plugin_path_dir_list:
                if os.path.exists(self.plugins_path + plugin['path'] + f'/{plugin_path_dir}/urls.py'):
                    bp = import_string(f'plugins.{plugin["path"]}.{plugin_path_dir}.urls.blueprint')
                    app.register_blueprint(bp, url_prefix=f'{bp.name}')

    def install_models(self):
        """
        动态导入models，相当于导包，将所有模块的models文件找到，动态导入
        1. 获取插件根目录
        :return:
        """
        # 插件根目录
        plus_about = self.plugins_info()
        plugins_base_path = plus_about['plus_base_path']
        plus_list = plus_about['plus_list']
        # 所有的插件
        for plus in plus_list:
            if os.path.isdir(plugins_base_path + plus['path']):
                if 'models' in os.listdir(plugins_base_path + plus['path']):
                    plus_item_all_models_file = os.listdir(plugins_base_path + plus['path'] + '/models')
                    for count, plus_item_models in enumerate(plus_item_all_models_file):
                        if '.py' not in plus_item_models:
                            plus_item_all_models_file.pop(count)
                        else:
                            print(f'引入models{plus["path"]}')
                            importlib.import_module(f'plugins.{plus["path"]}.models.{plus_item_models.split(".")[0]}')

    def plugins_info(self):
        """
        读取json配置文件，查找到所有的插件信息
        :return:
        """
        with open(self.plugins_config_file, 'r', encoding='utf-8') as f:
            file = json.loads(f.read())

        name = file['name']
        description = file['description']
        plus = file['plus']['plus']
        plus_base_path = file['plus']['plusDir']

        context = {
            'name': name,
            'des': description,
            'plus_list': plus,
            'plus_base_path': plus_base_path,
        }
        return context


class ApplicationData(Command):
    config = []
    plus = []
    plus_keys = []

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.config_name = '.arrplat.json'
        self.config_file_path = ''
        self.config = self.serialized_file(self.config_name)
        self.plus = self.get_plus(self.config)
        self.plus_keys = list(map(lambda plus: plus.get('key'), self.plus))
        print('start!')

    def run(self):
        print('---- begin to run')

        self.delete_application_data()
        self.save_data()

    @staticmethod
    def serialized_file(file_path):
        """
        解析config json文件
        :param file_path:
        :return:
        """
        print('开始解析文件')
        is_file = os.path.isfile(file_path)
        assert is_file, '插件的配置文件路径有误,读取路径{}'.format(file_path)
        with open(file_path, mode='r', encoding='utf-8') as f:
            context = f.read()
        print('文件解析完成')
        return json.loads(context)

    @staticmethod
    def get_plus(context):
        """
        获取plus信息
        :param context:
        :return:
        """
        # print('开始获取文件中plus信息')
        return context['plus']['plus']

    @staticmethod
    def insert_application_data(app):
        """
        插入app信息
        :return:
        """

        name = app.get('name')
        description = app.get('description')
        icon = app.get('icon')
        title = app.get('title')
        sort = app.get('sort')
        key = app.get('key')
        menus = app.get('menus')
        pages = app.get('pages')
        entities = app.get('entities')
        admin_route = app.get('adminRoute')
        api_route = app.get('apiRoute')

        application_obj = Application.query.filter(Application.key == app.get('key')).first()

        if not application_obj:
            print('开始创建应用:{}信息'.format(app.get('name')))
            application_obj = Application(
                name=name,
                title=title,
                admin_route=admin_route,
                api_route=api_route,
                description=description,
                icon=icon,
                visible=1,
                deletable=1,
                is_official=1,
                sort=sort,
                key=key,
                create_time=time.time()
            )
        else:
            print('开始更新应用:{}信息'.format(app.get('name')))
            application_obj.name = name
            application_obj.title = title
            application_obj.description = description
            application_obj.icon = icon
            application_obj.visible = 1
            application_obj.admin_route = admin_route,
            application_obj.api_route = api_route,
            application_obj.deletable = 1
            application_obj.is_official = 1
            application_obj.sort = sort
            application_obj.key = key

        db.session.add(application_obj)
        db.session.flush()
        return {'app': application_obj, 'menus': menus, 'pages': pages, 'entities': entities}

    @staticmethod
    def insert_application_menu_data(application_id, menu, sort):
        if not menu:
            return
        """
        插入app信息
        :param menu: menu
        :param application_id: int
        :return:
        """
        app_menu_obj = ApplicationMenus(application_id=application_id,
                                        name=menu['name'],
                                        icon=menu.get('icon', ''),
                                        link=menu.get('link', ''),
                                        parent_id=menu.get('parent_id', '0'),
                                        sort=sort,
                                        type=ApplicationMenus.string_to_page_type(menu.get('type', 'custom')),
                                        page_key=menu.get('page_key'),
                                        platform=''.join([i + ',' for i in menu.get('platform')]) if menu.get(
                                            'platform') else 'pc,mobile')

        db.session.add(app_menu_obj)
        db.session.flush()
        return app_menu_obj.id

    @staticmethod
    def insert_section_data(section, page_id, index):
        """
        插入section数据
        :param section:
        :param page_id:
        :param index:
        :return:
        """
        title = section.get('title')
        html_content = section.get('html_content')
        section_type = section.get('type')
        entity_key = section.get('entity_key')
        entity_params = section.get('entity_params')
        sort = section.get('sort', index)
        has_add_btn = section.get('has_add_btn', False)
        entity_id = db.session.query(Entity.id).filter(Entity.key == entity_key).first()
        section_obj = PageSection(
            title=title,
            page_id=page_id,
            html_content=html_content,
            entity_params=entity_params,
            has_add_btn=has_add_btn,
            sort=sort,
            section_type=PageSection.string_to_data_type(section_type),
            entity_id=entity_id[0]
        )
        db.session.add(section_obj)
        # db.session.flush()
        # return section_obj.id

    @staticmethod
    def insert_entity_data(entity):
        """
        插入entity数据
        :param entity:
        :return:
        """
        title = entity.get('title')
        table_name = entity.get('table_name')
        query_sql = entity.get('sql')
        data_type = entity.get('data_type')
        key = entity.get('key')
        has_connect_org = entity.get('has_connect_org')

        entity_obj = Entity(
            title=title,
            table_name=table_name,
            query_sql=query_sql,
            has_connect_org=has_connect_org,
            data_type=Entity.string_to_data_type(data_type),
            key=key
        )
        db.session.add(entity_obj)
        db.session.flush()
        return entity_obj

    @staticmethod
    def insert_entity_field_data(entity, entity_id, index):
        """
        插入entity数据
        :param entity:
        :param entity_id:
        :param index:
        :return:
        """
        link_button = entity.get('link_button')
        if link_button:
            link_button = Button.converter(link_button)
            db.session.add(link_button)

        field = EntityField.converter(entity, entity_id, index)
        if link_button and link_button.id:
            field.link_button_id = link_button.id

        db.session.add(field)
        db.session.flush()
        return field

    @staticmethod
    def insert_page_data(page, app_id):
        """
        插入page数据
        :param page:
        :param app_id:
        :return:
        """
        title = page.get('title')
        key = page.get('key')
        params = page.get('params')
        direction = page.get('direction')
        page_obj = Page(
            title=title,
            direction=Page.string_to_direction_type(direction),
            params=json.dumps(params),
            key=key,
            application_id=app_id
        )
        db.session.add(page_obj)
        db.session.flush()
        return {'page_id': page_obj.id}

    @staticmethod
    def insert_button_data(button):
        name = button.get('name')
        button_type = button.get('type')
        link = button.get('link')
        button_obj = Button(
            name=name,
            link=link,
            button_type=Button.string_to_button_type(button_type)
        )
        db.session.add(button_obj)
        db.session.flush()
        return button_obj

    @staticmethod
    def insert_entity_field_button_data(button_id, entity_id):
        button_obj = EntityFieldButton(
            button_id=button_id,
            entity_field_id=entity_id
        )
        db.session.add(button_obj)
        db.session.flush()
        return button_obj

    def save_data(self):
        print('开始插入app信息')
        for plus_detail in self.plus:
            app = self.insert_application_data(plus_detail)

            menus = app.get('menus') or []
            entities = app.get('entities') or []
            pages = app.get('pages') or []
            app_id = app.get('app').id
            print('APP ID: {}'.format(app_id))

            print('开始插入app menu信息')
            for i, menu in enumerate(menus):
                menu_id = self.insert_application_menu_data(app['app'].id, menu, i)
                children = menu.get('children', [])
                for j, child in enumerate(children):
                    print('开始插入menu child信息')
                    child['icon'] = ''
                    child['parent_id'] = menu_id
                    self.insert_application_menu_data(app['app'].id, child, j)

            print('开始插入entities信息')
            for entity in entities:
                entity_obj = self.insert_entity_data(entity)
                print('开始插入entity {} field信息'.format(entity.get('key')))
                for index, field in enumerate(entity.get('fields', [])):
                    entity_field_obj = self.insert_entity_field_data(field, entity_obj.id, index)
                    if field.get('buttons'):
                        print('开始插入button信息')
                        for button in field['buttons']:
                            button_obj = self.insert_button_data(button)
                            self.insert_entity_field_button_data(button_obj.id, entity_field_obj.id)

            print('开始插入page信息')
            for page in pages:
                page_obj = self.insert_page_data(page, app_id)
                print('开始插入page sections信息')
                for index, section in enumerate(page['sections']):
                    self.insert_section_data(section, page_obj['page_id'], index)
        db.session.commit()

    def delete_application_data(self):
        """
        每次安装应用时先删除非官方可移除的应用以及相关的所有非业务数据
        :return:
        # """
        print('开始删除无配置应用及相关信息')
        print(self.plus_keys)

        Application.query.filter(~Application.key.in_(self.plus_keys)).delete(synchronize_session=False)

        ApplicationMenus.query.delete(synchronize_session=False)
        Page.query.delete(synchronize_session=False)
        PageSection.query.delete(synchronize_session=False)
        Entity.query.delete(synchronize_session=False)
        Button.query.delete(synchronize_session=False)

        db.session.commit()
        print('应用相关信息删除成功')


class WritePid(object):

    def __init__(self):
        self.pid_file = 'pid.txt'

    def run(self):
        with open(self.pid_file, 'w') as f:
            f.write(str(self.get_pid()))

    @staticmethod
    def get_pid():
        return os.getpid()


setup_plugins = SetupPlugins()
application_data = ApplicationData()
write_pid = WritePid()
