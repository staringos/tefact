<div align="center">
  <img src="./admin/src/assets/images/logo-banner.png">
</div>
<div align="center">
  <a href="https://tefact.com">官网</a> | 
  <a href="https://saas.tefact.com">立即使用</a> | 
  <a href="https://tefact.com/docs">文档</a> | 
  <a href="https://tefact.com/docs/com">社区</a> | 
  <a href="https://tefact.com/docs/joinus">加入我们</a>
</div>

<div align="center">

  [![license](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](https://github.com/Tefact/tefact-saas)
  [![Actions Status](https://github.com/tefact/tefact-saas/workflows/deploy/badge.svg)](https://github.com/tefact/tefact-saas/actions)
  [![Release Version](https://img.shields.io/badge/release-0.0.1-green.svg)](https://github.com/Tefact/tefact-saas/releases)
  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Tefact/tefact-saas/pulls)
  [![Total alerts](https://img.shields.io/lgtm/alerts/g/Tefact/tefact-saas.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Tefact/tefact-saas/alerts/)

</div>

# Tefact 低代码平台


让你通过无需任何代码即可生成简单CRUD后台，方便的管理您的应用、页面、数据源、工作流 
Build your admin panel without code!

![Tefact Overview](./docs/images/editor.png)

[点击查看DEMO](http://saas.tefact.com)

![Tefact Overview](./docs/images/home-page.png)

#### 自定义丰富的企业应用

![APP Overview](./docs/images/app.png)

#### 更方便的在您的K8S集群中部署Docker镜像

![APP Overview](./docs/images/k8s.png)

#### Front End

- NodeJS = 12.2.0
- Lerna
- Typescript
- Vue
- Nuxt
- Python >3.6
- [Flask](https://www.palletsprojects.com/p/flask/): Web Framework
- [SQLAlchemy](https://github.com/pallets/flask-sqlalchemy): ORM Framework
- [FlaskMigrate](https://github.com/miguelgrinberg/Flask-Migrate): Database migrations
- Redis
- Mysql >5.6
- Docker
- Kubernetes

## Getting Start

### Config your application

Copy `config.example.py` as `config.py` and change database and redis configuration in it.

### Docker启动 Run In Docker

Build Docker Image

```shell script
docker build -t tefact .
```

Run it

```shell script
docker run -it -p 5000:5000 --name terfact-run -d Tefact
```

### 手动启动 Run Manually

**!! NodeJS = 12.2.0 !!**

Install Dependencies

```
cd admin
RUN npm config set unsafe-perm true
npm install
npm run generate
```

Install server requirements

```
cd ../
pip install -r requirements.txt
```

Start server

```
python main.py
```

Start admin panel

```
yarn run dev
```

goto your bower: http://localhost:8800/

## 初始化数据库 Init Database (If a new server)

Generate an initial migration:

```bash
python manage.py db migrate
```

Then you can apply the migration to the database:

```bash
python manage.py db upgrade
```

Init Plugin Config

```bash
./bin/startup.sh
```

Init product structure data

```bash
python manage.py init-data
```

## 获取技术支持

关注 `真科技Tefact` 微信公众号，回复 `技术支持` 加入微信群，获取 1v1 人工技术支持.

![qrcode](./docs/images/qrcode.jpg)

## Contributing

[CONTRIBUTING](./CONTRIBUTING.md)
