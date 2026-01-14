<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"

const props = defineProps<{
  class?: HTMLAttributes["class"]
}>()
</script>

<template>
  <div
    data-slot="dialog-header"
    :class="cn('pt-5 px-[24px] pb-[10px] pe-8', props.class)"
  >
    <slot />
  </div>
</template>
