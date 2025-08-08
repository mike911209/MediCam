// config.ts
import { ref } from 'vue'

export interface AppConfig {
  API_BASE_URL: string
  IDENTITY_POOL_ID: string
  REGION: string
  LOGIN_URL: string
  USER_POOL_ID: string
  CLIENT_ID: string
  STREAM_NAME: string
}

export const config = ref<AppConfig>({
  API_BASE_URL: 'https://meaf3dlqs8.execute-api.us-east-1.amazonaws.com/RESPONSE',
  IDENTITY_POOL_ID: 'us-east-1:a89b2316-7af4-4b53-a63a-56c849770e99',
  REGION: 'us-east-1',
  LOGIN_URL: 'cognito-idp.us-east-1.amazonaws.com/us-east-1_NaKfQ7Ulj',
  USER_POOL_ID: 'us-east-1_NaKfQ7Ulj',
  CLIENT_ID: '12eu2ndpm6sb4h1bto0kmdna0a',
  STREAM_NAME: 'icam',
})

// export async function loadConfig() {
//   const res = await fetch('/config.json')
//   const json = await res.json()
//   //   config.value = json
//   return json
// }

// export const config = loadConfig()
