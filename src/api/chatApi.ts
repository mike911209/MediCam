import axios from 'axios'
import type { Message } from '@/models/chatModels'

// config the baseURL in environment variables
const api = axios.create({
  baseURL: 'https://meaf3dlqs8.execute-api.us-east-1.amazonaws.com',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getBotResponse = async (userInput: Message) => {
  try {
    const body = {
      input: userInput.content,
      sessionId: '123456789',
    }

    const requestBody = {
      body: JSON.stringify(body),
    }

    const response = await api.post('/RESPONSE', requestBody) //
    const response_text = JSON.parse(response.data['body']) // Extract the 'body' property from the response data

    console.log('Response:', response_text) // Log the response data

    return response_text
  } catch (error) {
    console.error('Error fetching data:', error)
    throw error
  }
}
