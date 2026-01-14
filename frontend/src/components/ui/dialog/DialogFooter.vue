<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"

const props = defineProps<{ class?: HTMLAttributes["class"] }>()
</script>

<template>
  <div
    data-slot="dialog-footer"
    :class="cn('mt-[12px] flex justify-end gap-[12px]', props.class)"
  >
    <slot />
  </div>
</template>
