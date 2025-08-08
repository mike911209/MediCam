<template>
  <Dialog
    v-model:visible="showNotificationModal"
    modal
    header="MediCam Notification"
    :style="{ width: '50rem' }"
    :breakpoints="{ '1199px': '75vw', '575px': '90vw' }"
  >
    <p class="mb-8">{{ message?.content }}</p>
  </Dialog>
</template>

<script setup lang="ts">
import Dialog from 'primevue/dialog'
import { useHomeStore } from '@/stores/home'
import { storeToRefs } from 'pinia'

const store = useHomeStore()
const { showNotificationModal } = storeToRefs(store)

defineProps({
  message: Object,
})
</script>

<style scoped></style>
