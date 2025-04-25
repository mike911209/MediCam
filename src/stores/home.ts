import {
  ref,
  reactive,
  computed,
  watch,
  nextTick,
  type Component,
  defineAsyncComponent,
  shallowRef,
} from 'vue'
import { defineStore } from 'pinia'
import type { Message } from '@/models/chatModels.ts'

export const useHomeStore = defineStore('home', () => {
  const isLogin = ref<boolean>(false)
  const inputMessage = ref<string>('')

  const historyMessage = reactive<Message[]>([
    {
      role: 'assistant',
      status: 'initial',
      content:
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
    },
  ])

  const push2historyMessage = (message: Message) => {
    historyMessage.push(message)
  }

  return {
    isLogin,
    historyMessage,
    inputMessage,
    push2historyMessage,
  }
})
