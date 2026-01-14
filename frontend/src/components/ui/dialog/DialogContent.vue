<script setup lang="ts">
import type { DialogContentEmits, DialogContentProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { reactiveOmit } from "@vueuse/core"
import { X } from "lucide-vue-next"
import {
  DialogClose,
  DialogContent,

  DialogPortal,
  useForwardPropsEmits,
} from "reka-ui"
import { cn } from "@/lib/utils"
import DialogOverlay from "./DialogOverlay.vue"

const props = defineProps<DialogContentProps & { class?: HTMLAttributes["class"] }>()
const emits = defineEmits<DialogContentEmits>()

const delegatedProps = reactiveOmit(props, "class")

const forwarded = useForwardPropsEmits(delegatedProps, emits)
</script>

<template>
  <DialogPortal>
    <DialogOverlay />
    <DialogContent
      data-slot="dialog-content"
      v-bind="forwarded"
      :class="
        cn(
          'data-[state=open]:animate-dialog-slide-in-from-bottom data-[state=closed]:animate-dialog-slide-out-to-bottom fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 max-h-[95%] max-w-[98%] overflow-auto rounded-[20px] border border-[var(--border-main)] bg-[var(--background-gray-main)] p-0 z-[1000]',
          props.class,
        )"
    >
      <slot />

      <DialogClose
        class="flex h-7 w-7 items-center justify-center cursor-pointer rounded-md hover:bg-[var(--fill-tsp-gray-main)] absolute top-[18px] ltr:right-[20px] rtl:left-[20px] !right-3 !md:right-4"
      >
        <X class="size-5 text-[var(--icon-tertiary)]" />
        <span class="sr-only">Close</span>
      </DialogClose>
    </DialogContent>
  </DialogPortal>
</template>
