/**
 * 科大讯飞虚拟人 SDK 配置
 * 注意: appId/apiKey/apiSecret/sceneId 需替换为实际生产环境值
 */
export const AVATAR_CONFIG = {
  apiInfo: {
    serverUrl: 'wss://avatar.cn-huadong-1.xf-yun.com/v1/interact',
    appId: 'd31e0ddb',
    apiKey: '5fba054353c813fd5b5def545bd7230e',
    apiSecret: 'MDRjMDQ0Y2NmZDNjYzJlZjcyOWNlMjY1',
    sceneId: '314670014336733184',
  },
  globalParams: {
    stream: {
      protocol: 'xrtc',
      alpha: 1,
      bitrate: 1000000,
      fps: 25,
    },
    avatar: {
      avatar_id: '111001001',
      width: 720,
      height: 1280,
      scale: 0.8,
      move_h: 0,
      move_v: -0.9,
      audio_format: 1,
    },
    tts: {
      vcn: 'x4_chaoge',
      speed: 50,
      pitch: 50,
      volume: 100,
    },
    avatar_dispatch: {
      interactive_mode: 1,
      content_analysis: 0,
    },
  },
}
