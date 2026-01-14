<template>
    <span class="font-semibold text-[var(--text-primary)]" :style="{ fontSize: fontSize + 'px' }">manus</span>
</template>

<script setup lang="ts">
defineProps({
  fontSize: {
    type: Number,
    default: 20
  }
})
</script>
