<template>
    <svg 
        :width="size" 
        :height="size" 
        viewBox="0 0 16 16" 
        fill="none" 
        :style="{ minWidth: `${size}px`, minHeight: `${size}px` }"
        :color="color"
    >
        <g clip-path="url(#clearIconClipPath)">
            <path 
                fill-rule="evenodd" 
                clip-rule="evenodd"
                d="M7.99994 0.733322C3.98667 0.733322 0.733276 3.98672 0.733276 7.99999C0.733276 12.0133 3.98667 15.2667 7.99994 15.2667C12.0132 15.2667 15.2666 12.0133 15.2666 7.99999C15.2666 3.98672 12.0132 0.733322 7.99994 0.733322ZM6.42421 5.57573C6.18989 5.34141 5.80999 5.34141 5.57568 5.57573C5.34136 5.81004 5.34136 6.18994 5.57568 6.42425L7.15141 7.99999L5.57568 9.57572C5.34136 9.81004 5.34136 10.1899 5.57568 10.4243C5.80999 10.6586 6.18989 10.6586 6.42421 10.4243L7.99994 8.84852L9.57568 10.4243C9.80999 10.6586 10.1899 10.6586 10.4242 10.4243C10.6585 10.1899 10.6585 9.81004 10.4242 9.57572L8.84847 7.99999L10.4242 6.42425C10.6585 6.18994 10.6585 5.81004 10.4242 5.57573C10.1899 5.34141 9.80999 5.34141 9.57568 5.57573L7.99994 7.15146L6.42421 5.57573Z"
                fill="currentColor"
            />
        </g>
        <defs>
            <clipPath id="clearIconClipPath">
                <rect width="16" height="16" fill="white" />
            </clipPath>
        </defs>
    </svg>
</template>

<script setup lang="ts">
defineProps({
    size: {
        type: Number,
        default: 16
    },
    color: {
        type: String,
        default: 'var(--icon-tertiary)'
    }
});
</script>
