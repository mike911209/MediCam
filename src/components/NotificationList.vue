<template>
  <div class="notification-container">
    <div class="notification-header">Notification</div>
    <div class="notification-content">
      <!-- iterate show the notification message -->
      <div class="notification-list" ref="notificationListRef">
        <!-- Notification messages will be displayed here -->
        <NotificationModal :message="selectedMessage" />
        <div
          v-for="(message, index) in notificationMessage"
          :key="index"
          class="notification-item"
          @click="toggle2NotificationModal(message)"
        >
          <div class="notification-text">{{ message.content }}</div>
          <div class="notification-time">{{ message.timestamp }}</div>
        </div>
      </div>
    </div>
    <div class="notification-footer">
      <p>AWS 黑肉鬆 @ NTHU</p>
      <!-- <Button label="OK" @click="handleClose" /> -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { useHomeStore } from '@/stores/home'
import { storeToRefs } from 'pinia'
import NotificationModal from './modals/NotificationModal.vue'
import { ref } from 'vue'
import { type notificationMessage } from '@/models/notificationModels'
import { defaultNotificationMessage } from '@/models/notificationModels'

const store = useHomeStore()
const { notificationMessage, showNotificationModal } = storeToRefs(store)
const selectedMessage = ref<notificationMessage>(defaultNotificationMessage)

const toggle2NotificationModal = (message: notificationMessage) => {
  showNotificationModal.value = !showNotificationModal.value
  selectedMessage.value = message
}
</script>

<style scoped>
.notification-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 10px;
  gap: 10px;
  /* background-color: #f9f9f9; */
  background-color: #f0f0f0;
}

.notification-header {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  height: 10px;
  font-size: larger;
  /* padding: 10px; */
  /* font-weight: bold; */
}

.notification-content {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow: hidden;
  justify-content: start;
  align-items: start;
  /* padding: 10px; */
  border-radius: 10px;
}

.notification-content .notification-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-y: auto;
  /* background-color: #ffffff; */
  padding: 10px;
  gap: 10px;
}

.notification-item {
  width: 100%;
  padding: 10px;
  background-color: #e0e0e0;
  border-radius: 5px;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: start;
  .notification-time {
    font-size: 0.8rem;
    color: #888;
  }
  .notification-text {
    max-width: 100%;
    overflow-x: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
}

.notification-item:hover {
  background-color: #d1e7dd;
  cursor: pointer;
}

.notification-footer {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
