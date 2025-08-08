import axios from 'axios'
import type { Message } from '@/models/chatModels'
import { v4 as uuidv4 } from 'uuid'
import { ref } from 'vue'
import { useHomeStore } from '@/stores/home'
import { config } from '@/models/configModel'

const sessionId = ref<string>('12345678')
// config the baseURL in environment variables
const api = axios.create({
  baseURL: config.value.API_BASE_URL, // Replace with your actual base URL
  headers: {
    'Content-Type': 'application/json',
  },
})

export const configureChatApiClient = (idToken: string, accessToken: string) => {
  api.defaults.headers['Authorization'] = `Bearer ${idToken}`
  api.defaults.headers['x-api-key'] = accessToken
  sessionId.value = uuidv4() // Generate a new session ID for each user
}

export const getBotResponse = async (userInput: Message) => {
  try {
    const store = useHomeStore()
    const { checkLoginState } = store
    if (!checkLoginState) {
      return []
    }

    const body = {
      input: userInput.content,
      sessionId: sessionId.value,
    }

    const requestBody = {
      body: JSON.stringify(body),
    }

    const response = await api.post('/get_response', requestBody) //
    const response_text = JSON.parse(response.data['body']) // Extract the 'body' property from the response data

    return response_text
  } catch (error) {
    console.error('Error fetching data:', error)
    throw error
  }
}
