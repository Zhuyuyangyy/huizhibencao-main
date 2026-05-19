import { ref } from 'vue'
import { sendChatMessage } from '@/api'

const quickQuestions = [
  { id: 'q1', text: '当前湿度偏高怎么办' },
  { id: 'q2', text: '今日养生建议' },
  { id: 'q3', text: '讲讲黄芪的功效' },
  { id: 'q4', text: '如何预防根腐病' },
  { id: 'q5', text: '推荐时令药膳' },
  { id: 'q6', text: '讲讲三七的功效' },
]

export function useSageAI() {
  const messages = ref([
    {
      id: 'welcome',
      role: 'sage',
      content: '年轻人，你来了。本灵在此等候多时。\n有什么关于本草种植、节气养生的问题，尽管问吧。',
      type: 'text',
      timestamp: Date.now(),
    }
  ])
  const isTyping = ref(false)
  const currentExpression = ref('happy')

  const askQuestion = async (question) => {
    if (!question.trim()) return

    const userMsg = {
      id: 'msg_' + Date.now(),
      role: 'user',
      content: question,
      type: 'text',
      timestamp: Date.now(),
    }
    messages.value.push(userMsg)
    isTyping.value = true
    currentExpression.value = 'think'

    // Call real API (DeepSeek via backend)
    const res = await sendChatMessage(question, true)

    const sageMsg = {
      id: 'reply_' + Date.now(),
      role: 'sage',
      content: res?.data?.content || '老祖的灵感通道暂时中断了，请稍后再试。',
      type: 'text',
      timestamp: Date.now(),
    }
    messages.value.push(sageMsg)
    isTyping.value = false
    currentExpression.value = 'happy'
  }

  const getHealthTip = (solarTerm) => {
    if (!solarTerm) return '养生之道，顺应天时。'
    return `时值${solarTerm.name}，${solarTerm.healthTip}`
  }

  const getHerbKnowledge = (herb) => {
    if (!herb) return ''
    return `${herb.name}：${herb.efficacy}`
  }

  return {
    messages, isTyping, currentExpression,
    askQuestion, getHealthTip, getHerbKnowledge,
    quickQuestions,
  }
}
