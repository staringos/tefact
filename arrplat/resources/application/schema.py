from marshmallow import fields, post_dump, pre_dump

from arrplat.resources.application.models import Application, ApplicationMenus, OrgApplication, Message, \
    ApplicationCategory
from extensions import ma


class ApplicationMenusSchema(ma.ModelSchema):
    link = fields.String(default='')

    class Meta:
        model = ApplicationMenus
        fields = ('id', 'name', 'icon', 'link', 'sort', 'parent_id', 'page_key', 'type')

    @post_dump
    def default_string(self, data):
        for key, value in data.items():
            if value is None:
                data[key] = ''
        return data


class ApplicationCategorySchema(ma.ModelSchema):
    class Meta:
        model = ApplicationCategory
        fields = ('name',)


class ApplicationSchema(ma.ModelSchema):
    menus = fields.Nested(ApplicationMenusSchema, many=True)
    application_category = fields.Nested(ApplicationCategorySchema)

    def __init__(self, platform='pc', *args, **kwargs):
        super(ma.ModelSchema, self).__init__(*args, **kwargs)
        self.platform = platform


    @post_dump
    def format_type(self, data):
        return Application.format(data)

    class Meta:
        model = Application
        fields = ('id', 'name', 'title', 'description', 'official_website', 'install_number',
                  'version', 'icon', 'head_image', 'visible', 'deletable', 'is_official',
                  'images', 'sort', 'api_route', 'admin_route', 'menus', 'create_time',
                  'application_category', 'type', 'own_org_id')

    @post_dump
    def data_format(self, data):

        def images_format():
            images = data.get('images')
            if images and isinstance(images, str):
                image_list = images.split(',')
                data.update({'images': image_list})
            else:
                data['images'] = list()

        if self.only:
            if 'images' in self.only:
                images_format()
        else:
            images_format()

    @pre_dump
    def step(self, data, **kwargs):
        print(kwargs)
        data.menus = data.menus.filter(ApplicationMenus.platform.contains(self.platform))
        return data


class OrgApplicationSchema(ma.ModelSchema):
    application = ma.Nested(ApplicationSchema)

    class Meta:
        model = OrgApplication


class MessageSchema(ma.ModelSchema):
    class Meta:
        model = Message
