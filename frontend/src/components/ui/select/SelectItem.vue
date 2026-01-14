<script setup lang="ts">
import type { SelectItemProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { reactiveOmit } from "@vueuse/core"
import { Check } from "lucide-vue-next"
import {
  SelectItem,
  SelectItemIndicator,

  SelectItemText,
  useForwardProps,
} from "reka-ui"
import { cn } from "@/lib/utils"

const props = defineProps<SelectItemProps & { class?: HTMLAttributes["class"] }>()

const delegatedProps = reactiveOmit(props, "class")

const forwardedProps = useForwardProps(delegatedProps)
</script>

<template>
  <SelectItem
    data-slot="select-item"
    v-bind="forwardedProps"
    :class="
      cn(
        `flex items-center gap-3 w-full px-3 py-2 rounded-[8px] hover:bg-[var(--fill-tsp-white-main)] cursor-pointer text-sm transition-colors text-[var(--text-primary)] data-[highlighted]:bg-[var(--fill-tsp-white-main)] data-[state=checked]:bg-[var(--fill-tsp-white-main)] data-[state=checked]:font-medium outline-none border-none select-none data-[disabled]:pointer-events-none data-[disabled]:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 *:[span]:last:flex *:[span]:last:items-center *:[span]:last:gap-2`,
        props.class,
      )
    "
  >
    <span class="absolute right-2 flex size-3.5 items-center justify-center">
      <SelectItemIndicator>
        <Check class="size-4" style="stroke: var(--icon-primary)" />
      </SelectItemIndicator>
    </span>

    <SelectItemText>
      <slot />
    </SelectItemText>
  </SelectItem>
</template>
