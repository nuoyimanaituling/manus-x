<template>
    <svg xmlns="http://www.w3.org/2000/svg" :width="size" :height="size" viewBox="0 0 19 18" fill="none"
        :style="{ minWidth: `${size}px`, minHeight: `${size}px` }">
        <g filter="url(#filter0_ii_6414_3794)">
            <path
                d="M1.94922 4.7C1.94922 3.20883 3.15805 2 4.64922 2H13.2492C14.7404 2 15.9492 3.20883 15.9492 4.7V13.3C15.9492 14.7912 14.7404 16 13.2492 16H4.64922C3.15805 16 1.94922 14.7912 1.94922 13.3V4.7Z"
                fill="url(#paint0_linear_6414_3794)"></path>
        </g>
        <path
            d="M2.37779 4.7C2.37779 3.44552 3.39474 2.42857 4.64922 2.42857H13.2492C14.5037 2.42857 15.5206 3.44552 15.5206 4.7V13.3C15.5206 14.5545 14.5037 15.5714 13.2492 15.5714H4.64922C3.39474 15.5714 2.37779 14.5545 2.37779 13.3V4.7Z"
            stroke="#5F5F5F" stroke-width="0.857143"></path>
        <circle cx="8.57422" cy="8.625" r="3" stroke="#ACACAC" stroke-width="1.2" stroke-linecap="round"
            stroke-linejoin="round"></circle>
        <path d="M10.8242 10.875L12.3242 12.375" stroke="#ACACAC" stroke-width="1.2" stroke-linecap="round"
            stroke-linejoin="round"></path>
        <defs>
            <filter id="filter0_ii_6414_3794" x="1.44922" y="1.5" width="15" height="15" filterUnits="userSpaceOnUse"
                color-interpolation-filters="sRGB">
                <feFlood flood-opacity="0" result="BackgroundImageFix"></feFlood>
                <feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"></feBlend>
                <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                    result="hardAlpha"></feColorMatrix>
                <feOffset dx="1" dy="1"></feOffset>
                <feGaussianBlur stdDeviation="0.25"></feGaussianBlur>
                <feComposite in2="hardAlpha" operator="arithmetic" k2="-1" k3="1"></feComposite>
                <feColorMatrix type="matrix" values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.12 0"></feColorMatrix>
                <feBlend mode="normal" in2="shape" result="effect1_innerShadow_6414_3794"></feBlend>
                <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                    result="hardAlpha"></feColorMatrix>
                <feOffset dx="-1" dy="-1"></feOffset>
                <feGaussianBlur stdDeviation="0.25"></feGaussianBlur>
                <feComposite in2="hardAlpha" operator="arithmetic" k2="-1" k3="1"></feComposite>
                <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.16 0"></feColorMatrix>
                <feBlend mode="normal" in2="effect1_innerShadow_6414_3794" result="effect2_innerShadow_6414_3794">
                </feBlend>
            </filter>
            <linearGradient id="paint0_linear_6414_3794" x1="8.94922" y1="2" x2="8.94922" y2="16"
                gradientUnits="userSpaceOnUse">
                <stop stop-color="#272728" stop-opacity="0"></stop>
                <stop offset="1" stop-color="white" stop-opacity="0.16"></stop>
            </linearGradient>
        </defs>
    </svg>
</template>

<script setup lang="ts">
defineProps({
    size: {
        type: Number,
        default: 21,
    },
});
</script>