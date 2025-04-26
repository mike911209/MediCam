import axios from 'axios'
import { useHomeStore } from '@/stores/home'
import { config } from '@/models/configModel'

// config the baseURL in environment variables
const api = axios.create({
  baseURL: config.value.API_BASE_URL, // Replace with your actual base URL
  headers: {
    'Content-Type': 'application/json',
  },
})

export const configureStreamingApiClient = (idToken: string, accessToken: string) => {
  api.defaults.headers['Authorization'] = `Bearer ${idToken}`
  api.defaults.headers['x-api-key'] = accessToken
}

export const startStreaming = async () => {
  try {
    const store = useHomeStore()
    const { checkLoginState } = store
    if (!checkLoginState) {
      return []
    }

    await api.post('/stream/start')

    return
  } catch (error) {
    console.error('Error fetching data:', error)
    throw error
  }
}

export const endStreaming = async () => {
  try {
    const store = useHomeStore()
    const { checkLoginState } = store
    if (!checkLoginState) {
      return []
    }

    await api.post('/stream/end')

    return
  } catch (error) {
    console.error('Error fetching data:', error)
    throw error
  }
}

export const plusFocus = async () => {
  try {
    const store = useHomeStore()
    const { checkLoginState } = store
    if (!checkLoginState) {
      return []
    }
    await api.post('/focus/add')

    return
  } catch (error) {
    console.error('Error fetching data:', error)
    throw error
  }
}

export const minusFocus = async () => {
  try {
    const store = useHomeStore()
    const { checkLoginState } = store
    if (!checkLoginState) {
      return []
    }

    await api.post('/focus/sub')

    return
  } catch (error) {
    console.error('Error fetching data:', error)
    throw error
  }
}
