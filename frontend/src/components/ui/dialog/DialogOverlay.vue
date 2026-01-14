<script setup lang="ts">
import type { DialogOverlayProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { reactiveOmit } from "@vueuse/core"
import { DialogOverlay } from "reka-ui"
import { cn } from "@/lib/utils"

const props = defineProps<DialogOverlayProps & { class?: HTMLAttributes["class"] }>()

const delegatedProps = reactiveOmit(props, "class")
</script>

<template>
  <DialogOverlay
    data-slot="dialog-overlay"
    v-bind="delegatedProps"
    :class="cn('data-[state=open]:animate-dialog-bg-fade-in data-[state=closed]:animate-dialog-bg-fade-out fixed inset-0 z-[1000] bg-black/60 backdrop-blur-[4px] overflow-auto', props.class)"
  >
    <slot />
  </DialogOverlay>
</template>
