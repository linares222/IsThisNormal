<template>
    <div class="relative min-h-screen">
        <div class="absolute top-8 left-8 z-20">
            <NuxtLink to="/" class="text-black hover:underline font-medium flex items-center gap-2 bg-white/80 backdrop-blur-sm px-3 py-2 ">
                <Icon name="mdi:arrow-left" class="w-5 h-5" />
                Voltar
            </NuxtLink>
        </div>
        <slot />
    </div>
</template>

<script setup>

</script>