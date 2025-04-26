import axios from 'axios'
import type { Message } from '@/models/chatModels'

// config the baseURL in environment variables
const api = axios.create({
  baseURL: 'https://meaf3dlqs8.execute-api.us-east-1.amazonaws.com/RESPONSE',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const configureChatApiClient = (idToken: string, accessToken: string) => {
  api.defaults.headers['Authorization'] = `Bearer ${idToken}`
  api.defaults.headers['x-api-key'] = accessToken
}

export const getBotResponse = async (userInput: Message) => {
  try {
    console.log('api config: ', api.defaults.headers) // Log the Authorization header
    const body = {
      input: userInput.content,
      sessionId: '123456789',
    }

    const requestBody = {
      body: JSON.stringify(body),
    }

    const response = await api.post('/get_response', requestBody) //
    const response_text = JSON.parse(response.data['body']) // Extract the 'body' property from the response data

    console.log('Response:', response_text) // Log the response data

    return response_text
  } catch (error) {
    console.error('Error fetching data:', error)
    throw error
  }
}
