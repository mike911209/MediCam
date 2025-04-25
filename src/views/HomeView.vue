<template>
  <BasicLayout>
    <template v-slot:user-info>
      <div>User2</div>
    </template>
    <template v-slot:notification>
      <div>Notification2</div>
    </template>
    <template v-slot:main-content>
      <!-- <div>Content2</div> -->
       <ChatRoom/>
    </template>
  </BasicLayout>
</template>

<script setup lang="ts">
import BasicLayout from '../components/layouts/BasicLayout.vue'
import ChatRoom from '@/components/ChatRoom.vue';

</script>
