import { ref, reactive } from 'vue'
import { defineStore } from 'pinia'
import type { Message } from '@/models/chatModels.ts'
import type { notificationMessage } from '@/models/notificationModels'
import { getNotificationList } from '@/api/notificationApi.ts'

export const useHomeStore = defineStore('home', () => {
  const isLogin = ref<boolean>(false)
  const isStreaming = ref<boolean>(false)
  const showNotificationModal = ref<boolean>(false)
  const inputMessage = ref<string>('')
  const idToken = ref<string>('')
  const accessToken = ref<string>('')

  const historyMessage = reactive<Message[]>([
    {
      role: 'assistant',
      status: 'initial',
      content: 'Hello, how can I help you today?',
    },
  ])
  const notificationMessage = reactive<notificationMessage[]>([])

  const push2historyMessage = (message: Message) => {
    historyMessage.push(message)
  }

  const popHistoryMessage = () => {
    if (historyMessage.length > 0) {
      historyMessage.pop()
    }
  }
  const pullNotificationList = async () => {
    try {
      const response = await getNotificationList()

      notificationMessage.length = 0 // Clear the existing notificationMessage array

      notificationMessage.push(...response)
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }

  const checkLoginState = () => {
    return isLogin.value
  }

  pullNotificationList()

  return {
    isLogin,
    showNotificationModal,
    historyMessage,
    notificationMessage,
    inputMessage,
    idToken,
    accessToken,
    isStreaming,
    push2historyMessage,
    pullNotificationList,
    popHistoryMessage,
    checkLoginState,
  }
})
