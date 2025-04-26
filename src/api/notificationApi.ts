import axios from 'axios'
import type { Message } from '@/models/chatModels'

// config the baseURL in environment variables
const api = axios.create({
  baseURL: ' https://meaf3dlqs8.execute-api.us-east-1.amazonaws.com/RESPONSE', // Replace with your actual base URL
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
    const response = await api.get('/text') //
    // const response_array = response.data // Extract the 'body' property from the response data
    // const response_text = JSON.parse(response.data['body']) // Extract the 'body' property from the response data
    const response_array = JSON.parse(response.data['body'])
    // console.log('Response:', response_array) // Log the response data

    const response_array_mapped = response_array.map((item: any) => {
      return {
        content: item.text,
        timestamp: item.time,
      }
    })
    // Convert timestamp to local string format
    // console.log('response_array_mapped:', response_array_mapped) // Log the response data
    return response_array_mapped
  } catch (error) {
    console.error('Error fetching data:', error)
    throw error
  }
}
