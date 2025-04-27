<template>
  <div class="streaming-container">
    <div class="streaming-content">
      <video ref="videoPlayer" controls></video>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { KinesisVideoClient, GetDataEndpointCommand } from '@aws-sdk/client-kinesis-video'
import {
  KinesisVideoArchivedMediaClient,
  GetHLSStreamingSessionURLCommand,
} from '@aws-sdk/client-kinesis-video-archived-media'
import { useCredentialStore } from '@/stores/credentialStore'
import Hls from 'hls.js'
import { config } from '@/models/configModel'

const credentialStore = useCredentialStore()

const getHLSUrl = async (retryCount = 10, delay = 3000) => {
  const region = config.value.REGION
  const streamName = config.value.STREAM_NAME
  const credentials = await credentialStore.getCredentials()

  const kinesisVideoClient = new KinesisVideoClient({ region, credentials })

  const dataEndpointResponse = await kinesisVideoClient.send(
    new GetDataEndpointCommand({
      StreamName: streamName,
      APIName: 'GET_HLS_STREAMING_SESSION_URL',
    }),
  )

  const endpoint = dataEndpointResponse.DataEndpoint
  const kvamClient = new KinesisVideoArchivedMediaClient({ region, endpoint, credentials })

  let lastError = null

  for (let attempt = 1; attempt <= retryCount; attempt++) {
    try {
      const hlsStreamResponse = await kvamClient.send(
        new GetHLSStreamingSessionURLCommand({
          StreamName: streamName,
          PlaybackMode: 'LIVE',
        }),
      )
      return hlsStreamResponse.HLSStreamingSessionURL
    } catch (error) {
      lastError = error
      if (error.name === 'ResourceNotFoundException') {
        console.warn(`Attempt ${attempt}: No fragments yet, retrying after ${delay}ms...`)
        await new Promise((resolve) => setTimeout(resolve, delay))
      } else {
        throw error
      }
    }
  }

  throw lastError
}

const videoPlayer = ref<HTMLVideoElement | null>(null)

onMounted(() => {
  getHLSUrl().then((url) => {
    if (videoPlayer.value && url) {
      if (Hls.isSupported()) {
        const hls = new Hls({
          maxBufferLength: 30, // 可选，最大缓存30秒
          manifestLoadingTimeOut: 20000, // 可选，提高timeout
        })
        hls.loadSource(url)
        hls.attachMedia(videoPlayer.value)

        hls.on(Hls.Events.ERROR, (event, data) => {
          if (data.fatal) {
            switch (data.type) {
              case Hls.ErrorTypes.NETWORK_ERROR:
                console.log('network error, trying to recover...')
                hls.startLoad()
                break
              case Hls.ErrorTypes.MEDIA_ERROR:
                console.log('media error, trying to recover...')
                hls.recoverMediaError()
                break
              default:
                console.log('unrecoverable error, destroying hls')
                hls.destroy()
                break
            }
          }
        })

        onBeforeUnmount(() => {
          hls.destroy()
        })
      } else if (videoPlayer.value.canPlayType('application/vnd.apple.mpegurl')) {
        videoPlayer.value.src = url
      }
    }
  })
})
</script>

<style scoped>
.streaming-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  gap: 10px;
  /* background-color: #f0f0f0; */
}

.streaming-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 10px;
  height: 100%;
  width: 100%;
}

video {
  max-width: 100%;
  border-radius: 10px;
  object-fit: contain;
}
</style>
