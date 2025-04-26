export interface notificationMessage {
  role: 'user' | 'assistant' | 'system'
  status: 'normal' | 'initial' | 'approved' | 'rejected'
  content: string
  timestamp: string
}

export const defaultNotificationMessage: notificationMessage = {
  role: 'assistant',
  status: 'initial',
  content: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
  timestamp: new Date().toLocaleString(),
}
