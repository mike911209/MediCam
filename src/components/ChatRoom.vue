<template>
  <div class="chat-room-container">
    <div class="chat-room-header">
      <h3>MediCam</h3>
    </div>
    <div class="chat-room-content">
      <div class="message-list" ref="messageListRef">
        <!-- Messages will be displayed here -->
        <div
          v-for="(message, index) in historyMessage"
          :key="index"
          class="message-item"
          :class="{ 'from-user': message.role === 'user' }"
        >
          <div class="message-sender">{{ message.role }}</div>
          <div class="message-text">{{ message.content }}</div>
        </div>
      </div>
      <div class="message-input">
        <InputText
          class="input-wrapper"
          type="text"
          v-model="inputMessage"
          placeholder="Type here..."
          @keyup.enter="sendMessage"
        />
        <div class="message-send-btn button" @click="sendMessage"><i class="pi pi-send"></i></div>

        <!-- <button class="message-send-btn">Send</button> -->
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import InputText from 'primevue/inputtext'
import { useHomeStore } from '@/stores/home'
import { storeToRefs } from 'pinia'
import { type Message } from '@/models/chatModels'
import { ref, nextTick } from 'vue'
import { getBotResponse } from '@/api/chatApi'

const store = useHomeStore()
const { push2historyMessage } = store
const { inputMessage, historyMessage } = storeToRefs(store)

const messageListRef = ref<HTMLElement | null>(null)

const scrollToEnd = () => {
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (inputMessage.value.trim() === '') return
  const newMessage: Message = {
    role: 'user',
    status: 'normal',
    content: inputMessage.value,
  }

  push2historyMessage(newMessage)
  inputMessage.value = ''

  nextTick(() => {
    scrollToEnd()
  })

  const botResponse = await getBotResponse(newMessage)
    .then((response) => {
      const botMessage: Message = {
        role: 'assistant',
        status: 'normal',
        content: response,
      }
      push2historyMessage(botMessage)
    })
    .catch((error) => {
      const botMessage: Message = {
        role: 'assistant',
        status: 'normal',
        content: 'Failed to get response',
      }
      push2historyMessage(botMessage)
      console.error('Error fetching bot response:', error)
    })
    .finally(() => {
      nextTick(() => {
        scrollToEnd()
      })
    })
}
</script>

<style scoped>
.chat-room-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  /* background-color: #f0f0f0; */
}

.chat-room-header {
  /* background-color: #4caf50; */
  /* color: white; */
  padding: 10px;
  text-align: center;
}

.chat-room-content {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  padding: 10px;
  overflow: hidden;
}

.chat-room-content .message-list {
  flex-grow: 1;
  overflow-y: auto;
  background-color: #ffffff;
  padding: 10px;
  border-radius: 10px;
}

.message-item {
  margin-bottom: 10px;
  padding: 10px;

  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 5px;

  &.from-user {
    flex-direction: row-reverse;
    justify-content: end;
    .message-text {
      background-color: #d1e7dd;
    }
  }

  .message-text {
    border-radius: 5px;
    padding: 10px;
    background-color: #f0f0f0;
    max-width: 70%;
  }
}

.chat-room-content .message-input {
  display: flex;
  flex-direction: row;
  width: 100%;
  gap: 10px;
  align-items: center;
  margin-top: 10px;
  height: 40px;

  .input-wrapper {
    flex-grow: 1;
  }
  .message-send-btn {
    /* background-color: #4caf50; */
    /* color: white; */
    border: none;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
  }
}
</style>
