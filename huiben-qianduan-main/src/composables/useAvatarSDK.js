import { ref, shallowRef, onUnmounted } from 'vue'
import AvatarPlatform, {
  PlayerEvents,
  SDKEvents,
} from '@/lib/vm-sdk/avatar-sdk-web_3.1.2.1002/index.js'
import { AVATAR_CONFIG } from '@/config/avatar'

export function useAvatarSDK({ onSubtitle, onNlpResponse } = {}) {
  const instance = shallowRef(null)
  const isConnected = ref(false)
  const isLoading = ref(false)
  const playNotAllowed = ref(false)
  const subtitle = ref('')
  const error = ref(null)

  let started = false
  let pendingSubtitle = ''

  const initAndStart = async (wrapperEl) => {
    if (started) return
    started = true
    isLoading.value = true
    error.value = null

    try {
      const sdk = new AvatarPlatform({ useInlinePlayer: true })
      instance.value = sdk

      sdk.setApiInfo(AVATAR_CONFIG.apiInfo)
      sdk.setGlobalParams(AVATAR_CONFIG.globalParams)

      sdk.removeAllListeners()
      sdk
        .on(SDKEvents.connected, (resp) => {
          console.log('[AvatarSDK] connected', resp)
        })
        .on(SDKEvents.stream_start, () => {
          console.log('[AvatarSDK] stream_start')
        })
        .on(SDKEvents.disconnected, (e) => {
          isLoading.value = false
          isConnected.value = false
          started = false
          if (e) console.error('[AvatarSDK] disconnected:', e)
        })
        .on(SDKEvents.frame_start, () => {
          pendingSubtitle = ''
          subtitle.value = ''
        })
        .on(SDKEvents.frame_stop, () => {
          if (pendingSubtitle && onSubtitle) {
            onSubtitle(pendingSubtitle)
          }
          pendingSubtitle = ''
        })
        .on(SDKEvents.subtitle_info, (data) => {
          const text = data?.text || ''
          if (text) {
            subtitle.value = text
            pendingSubtitle += text
          }
        })
        .on(SDKEvents.nlp, (data) => {
          console.log('[AvatarSDK] nlp:', data)
          const nlpText = data?.text || data?.result || data?.content || ''
          if (nlpText && onNlpResponse) {
            onNlpResponse(nlpText)
          }
        })
        .on(SDKEvents.asr, (data) => {
          console.log('[AvatarSDK] asr:', data)
        })
        .on(SDKEvents.error, (e) => {
          console.error('[AvatarSDK] error:', e)
          error.value = e?.message || 'SDK error'
        })

      const player = sdk.player || sdk.createPlayer()
      player
        .on(PlayerEvents.play, () => {})
        .on(PlayerEvents.waiting, () => {})
        .on(PlayerEvents.playing, () => {})
        .on(PlayerEvents.playNotAllowed, () => {
          console.log('[AvatarSDK] play not allowed')
          playNotAllowed.value = true
        })

      await sdk.start({ wrapper: wrapperEl })
      isConnected.value = true
      playNotAllowed.value = false
    } catch (e) {
      console.error('[AvatarSDK] start failed:', e)
      error.value = e?.message || '启动失败'
      started = false
    } finally {
      isLoading.value = false
    }
  }

  const sendText = (text, opts = {}) => {
    if (!instance.value || !isConnected.value) return Promise.reject(new Error('SDK 未连接'))
    const { nlp = true, interactive_mode = 1 } = opts
    return instance.value.writeText(text, {
      nlp,
      avatar_dispatch: { interactive_mode },
    })
  }

  const interrupt = () => {
    if (!instance.value) return
    instance.value.interrupt()
  }

  const resume = () => {
    if (!instance.value?.player) return
    instance.value.player.resume()
    playNotAllowed.value = false
  }

  const stop = () => {
    if (!instance.value) return
    instance.value.stop()
    isConnected.value = false
    started = false
  }

  const destroy = () => {
    if (!instance.value) return
    instance.value.destroy()
    instance.value = null
    isConnected.value = false
    started = false
  }

  onUnmounted(() => {
    destroy()
  })

  return {
    isConnected,
    isLoading,
    playNotAllowed,
    subtitle,
    error,
    initAndStart,
    sendText,
    interrupt,
    resume,
    stop,
    destroy,
  }
}
