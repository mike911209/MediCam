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

const getHLSUrl = async () => {
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

  const hlsStreamResponse = await kvamClient.send(
    new GetHLSStreamingSessionURLCommand({
      StreamName: streamName,
      PlaybackMode: 'LIVE', // LIVE 或 ON_DEMAND
    }),
  )

  return hlsStreamResponse.HLSStreamingSessionURL
}

const videoPlayer = ref<HTMLVideoElement | null>(null)

onMounted(() => {
  getHLSUrl().then((url) => {
    if (videoPlayer.value && url) {
      if (Hls.isSupported()) {
        const hls = new Hls()
        hls.loadSource(url)
        hls.attachMedia(videoPlayer.value)

        hls.on(Hls.Events.MANIFEST_PARSED, () => {
          console.log('HLS manifest parsed')
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
