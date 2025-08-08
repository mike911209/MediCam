<template>
  <div class="login-container">
    <span class="logo-text">MediCam</span>
    <div class="username-container">
      <label for="username">Username</label>
      <InputText id="username" v-model="username" type="text" />
    </div>

    <div class="password-container">
      <label for="password">Password</label>
      <InputText id="password" v-model="password" type="password" />
    </div>

    <div class="login-button">
      <Button class="button" label="Login" icon="pi pi-user" @click="handleLogin" />
    </div>

    <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'

import { CognitoUserPool, CognitoUser, AuthenticationDetails } from 'amazon-cognito-identity-js'
import { useHomeStore } from '@/stores/home'
import { storeToRefs } from 'pinia'
import { configureChatApiClient } from '@/api/chatApi'
import { configureNotificationApiClient } from '@/api/notificationApi'
import { configureStreamingApiClient } from '@/api/streamingApi'
import { useCredentialStore } from '@/stores/credentialStore'
import { config } from '@/models/configModel'

const store = useHomeStore()
const { pullNotificationList } = store
const { idToken, accessToken, isLogin } = storeToRefs(store)

const credentialStore = useCredentialStore()
const { initCredentials } = credentialStore

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const router = useRouter()

const userPool = new CognitoUserPool({
  UserPoolId: config.value.USER_POOL_ID, // User Pool ID
  ClientId: config.value.CLIENT_ID, // App Client ID
})

const handleLogin = () => {
  errorMessage.value = ''

  const user = new CognitoUser({
    Username: username.value,
    Pool: userPool,
  })

  const authDetails = new AuthenticationDetails({
    Username: username.value,
    Password: password.value,
  })

  user.authenticateUser(authDetails, {
    // TODO: block home page if unauthenticated
    // Callback functions for authentication
    onSuccess: (session) => {
      // console.log('Login Sucessfully! Token:', session.getIdToken().getJwtToken())
      console.log('Login Sucessfully!')
      isLogin.value = true
      idToken.value = session.getIdToken().getJwtToken()
      accessToken.value = session.getAccessToken().getJwtToken()
      configureChatApiClient(idToken.value, accessToken.value)
      configureNotificationApiClient(idToken.value, accessToken.value)
      configureStreamingApiClient(idToken.value, accessToken.value)
      pullNotificationList()
      initCredentials(idToken.value)

      errorMessage.value = ''
      router.push('/') // back to home
    },
    onFailure: (err) => {
      console.error('Failed to Login:', err)
      errorMessage.value = err.message || 'Failed to Login'
    },
    newPasswordRequired: (userAttributes) => {
      delete userAttributes.email_verified
      delete userAttributes.phone_number_verified
      delete userAttributes.email
      delete userAttributes.phone_number

      const newPassword = prompt('Please enter a new password!') || ''
      if (!newPassword) {
        errorMessage.value = 'You must enter a new password!'
        return
      }

      user.completeNewPasswordChallenge(newPassword, userAttributes, {
        onSuccess: (session) => {
          console.log('Update successfully!', session)
          errorMessage.value = ''
        },
        onFailure: (err) => {
          console.error('Failed to set the new password', err)
          errorMessage.value = err.message || 'Failed to set the new password'
        },
      })
    },
  })
}
</script>

<style scoped>
.logo-text {
  font-size: 1.5rem;
  font-weight: bold;
  color: #37613c;
}
.username-container,
.password-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
  max-width: 20rem;
}

.login-button {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

.login-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding-top: 1.25rem;
  padding-bottom: 1.25rem;
}
</style>
