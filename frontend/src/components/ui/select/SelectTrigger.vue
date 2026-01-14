<script setup lang="ts">
import type { SelectTriggerProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { reactiveOmit } from "@vueuse/core"
import { ChevronDown } from "lucide-vue-next"
import { SelectIcon, SelectTrigger, useForwardProps } from "reka-ui"
import { cn } from "@/lib/utils"

const props = withDefaults(
  defineProps<SelectTriggerProps & { class?: HTMLAttributes["class"], size?: "sm" | "default" }>(),
  { size: "default" },
)

const delegatedProps = reactiveOmit(props, "class", "size")
const forwardedProps = useForwardProps(delegatedProps)
</script>

<template>
  <SelectTrigger
    data-slot="select-trigger"
    :data-size="size"
    v-bind="forwardedProps"
    :class="cn(
      `group flex items-center justify-between px-3 rounded-lg border cursor-pointer transition-colors bg-[var(--fill-tsp-gray-main)] border-[var(--border-white)] hover:bg-[var(--fill-tsp-gray-main)] hover:border-[var(--border-white)] text-[var(--text-primary)] text-sm whitespace-nowrap focus:ring-0 focus:ring-transparent focus:shadow-none focus:border-[var(--border-white)] disabled:cursor-not-allowed disabled:opacity-50 data-[size=default]:h-9 data-[size=sm]:h-8 *:data-[slot=select-value]:line-clamp-1 *:data-[slot=select-value]:flex *:data-[slot=select-value]:items-center *:data-[slot=select-value]:gap-2 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 [&:focus]:outline-[0px] [&:focus]:outline-transparent`,
      props.class,
    )"
    style="outline: none !important; box-shadow: none !important;"
  >
    <slot />
    <SelectIcon as-child>
      <ChevronDown class="size-4 transition-transform group-data-[state=open]:rotate-180" style="stroke: var(--text-primary)" />
    </SelectIcon>
  </SelectTrigger>
</template>
