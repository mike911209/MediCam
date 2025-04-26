import axios from 'axios'
import { useHomeStore } from '@/stores/home'
import { type OrderResponse } from '@/models/chatModels'
import { config } from '@/models/configModel'

// config the baseURL in environment variables
const api = axios.create({
  baseURL: config.value.API_BASE_URL, // Replace with your actual base URL
  headers: {
    'Content-Type': 'application/json',
  },
})

export const configureNotificationApiClient = (idToken: string, accessToken: string) => {
  api.defaults.headers['Authorization'] = `Bearer ${idToken}`
  api.defaults.headers['x-api-key'] = accessToken
}

export const getNotificationList = async () => {
  try {
    const store = useHomeStore()
    const { checkLoginState } = store
    if (!checkLoginState) {
      return []
    }
    const response = await api.get('/order') //
    // const response_array = response.data // Extract the 'body' property from the response data
    // const response_text = JSON.parse(response.data['body']) // Extract the 'body' property from the response data
    const response_array = JSON.parse(response.data['body'])

    const response_array_mapped = response_array.map((item: OrderResponse) => {
      return {
        role: 'assistant',
        status: 'normal',
        content: item.text,
        timestamp: item.time,
      }
    })
    // Convert timestamp to local string format

    return response_array_mapped
  } catch (error) {
    console.error('Error fetching data:', error)
    throw error
  }
}
