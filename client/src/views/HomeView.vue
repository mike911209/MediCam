<template>
  <BasicLayout>
    <template v-slot:user-info>
      <UserPanel></UserPanel>
    </template>
    <template v-slot:notification>
      <NotificationList />
      <!-- <div>Notification2</div> -->
    </template>
    <template v-slot:main-content>
      <!-- <div>Content2</div> -->
      <ChatRoom v-if="!isStreaming" />
      <Stream v-if="isStreaming" />
    </template>
  </BasicLayout>
</template>

<script setup lang="ts">
import BasicLayout from '../components/layouts/BasicLayout.vue'
import ChatRoom from '@/components/ChatRoom.vue'
import NotificationList from '@/components/NotificationList.vue'
import UserPanel from '@/components/ControlPanel.vue'
import Stream from '@/components/VideoStream.vue'

import { useHomeStore } from '@/stores/home'
import { storeToRefs } from 'pinia'

const store = useHomeStore()
const { isStreaming } = storeToRefs(store)
</script>

<style scoped></style>
