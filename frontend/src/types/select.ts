export interface SelectOption {
  value: any
  label: string
  disabled?: boolean
}

export interface SelectProps {
  modelValue?: any
  options: SelectOption[] | string[] | number[]
  width?: string
  height?: string
  placeholder?: string
  placement?: 'top' | 'bottom' // Currently only 'bottom' is implemented
  buttonClass?: string
  selectClass?: string
  textClass?: string
  optionClass?: string
  valueKey?: string
  labelKey?: string
}

export interface SelectEmits {
  'update:modelValue': [value: any]
  'change': [value: any]
}
