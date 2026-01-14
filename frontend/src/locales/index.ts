import en from './en'
import zh from './zh'

export default {
  en,
  zh
}

export type Locale = 'en' | 'zh'

export const availableLocales: { label: string; value: Locale }[] = [
  { label: 'English', value: 'en' },
  { label: '中文', value: 'zh' }
] 