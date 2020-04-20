import axios from 'axios'
import { auth } from '@arrplat/utils'

const token = auth.getToken()
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}
