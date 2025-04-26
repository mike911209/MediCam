<template>
  <div class="constrol-panel-container">
    <div class="logo-container"><span class="logo-text">MediCam</span></div>
    <i
      v-if="!isStreaming"
      class="pi pi-video stream-start-btn button"
      @click="toggele2Streaming"
    ></i>
    <div v-else class="ctrl-ary">
      <i class="pi pi-stop-circle stream-end-btn" @click="toggele2Streaming"></i>
      <i
        class="pi pi-plus-circle focus-adjust-btn"
        style="font-size: 1.2rem"
        @click="plusFocus()"
      ></i>
      <i
        class="pi pi-minus-circle focus-adjust-btn"
        style="font-size: 1.2rem"
        @click="minusFocus()"
      ></i>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useHomeStore } from '@/stores/home'
import { storeToRefs } from 'pinia'
import { startStreaming, endStreaming, plusFocus, minusFocus } from '@/api/streamingApi'

const store = useHomeStore()
const { isStreaming } = storeToRefs(store)

const toggele2Streaming = async () => {
  isStreaming.value = !isStreaming.value

  if (isStreaming.value) {
    startStreaming()
      .then(() => {
        console.log('Streaming started')
      })
      .catch((error) => {
        console.error('Error starting streaming:', error)
        isStreaming.value = false
      })
  } else {
    endStreaming()
      .then(() => {
        console.log('Streaming ended')
      })
      .catch((error) => {
        console.error('Error ending streaming:', error)
        isStreaming.value = true
      })
  }
}
</script>

<style>
.constrol-panel-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  gap: 10px;
  /* background-color: #f9f9f9; */
  background-color: #f0f0f0;
}

.logo-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 10px;

  flex-grow: 1;
  .logo-text {
    font-size: 1.5rem;
    font-weight: bold;
    color: #37613c;
  }
}

.stream-start-btn {
  /* background-color: #4caf50; */
  /* color: white; */
  width: 100%;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

.ctrl-ary {
  display: flex;
  flex-direction: row;
  justify-content: start;
  align-items: center;
  gap: 15px;
  width: 100%;
}

.stream-end-btn {
  background-color: #cc5f5a;
  color: white;
  flex-grow: 1;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

.stream-end-btn:hover {
  background-color: #c09d9b;
  color: #1f2937;
}
.focus-adjust-btn {
  border-radius: 100px;
}

.focus-adjust-btn:hover {
  background-color: #cc5f5a;
  color: white;
  cursor: pointer;
}
</style>
