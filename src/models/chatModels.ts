export interface Message {
  role: 'user' | 'assistant' | 'system'
  status: 'normal' | 'initial' | 'loading'
  content: string
}
