import appGenerator from './app'
import orgGenerator from './org'
import userGenerator from './user'
import authGenerator from './auth'
import entitiesGenerator from './entities'
import platformGenerator from './platform'
import educationGenerator from './education'
import editorGenerator from './editor'

const ServicesGenerator = (request) => {
  return {
    app: appGenerator(request),
    org: orgGenerator(request),
    user: userGenerator(request),
    auth: authGenerator(request),
    entities: entitiesGenerator(request),
    platform: platformGenerator(request),
    education: educationGenerator(request),
    editor: editorGenerator(request),
  }
}

export default ServicesGenerator
