// stores/credentialStore.ts
import { defineStore } from 'pinia'
import { fromCognitoIdentityPool } from '@aws-sdk/credential-providers'
import { config } from '@/models/configModel'

export const useCredentialStore = defineStore('credential', {
  state: () => ({
    credentialProvider: null as null | ReturnType<typeof fromCognitoIdentityPool>,
  }),
  actions: {
    initCredentials(idToken: string) {
      this.credentialProvider = fromCognitoIdentityPool({
        clientConfig: { region: config.value.REGION },
        identityPoolId: config.value.IDENTITY_POOL_ID,
        logins: {
          [config.value.LOGIN_URL]: idToken,
        },
      })
      console.log('Credential provider initialized')
    },
    async getCredentials() {
      if (!this.credentialProvider) {
        throw new Error('Credential provider not initialized')
      }
      return await this.credentialProvider()
    },
  },
})
