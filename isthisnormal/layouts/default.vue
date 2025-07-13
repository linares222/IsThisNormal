<template>
  <div class="relative min-h-screen">
    <!-- Navbar - Positioned absolutely to not affect centering -->
    <div class="absolute top-0 left-0 right-0 z-20">
      <Navbar />
        </div>
    
    <!-- Content Area - Can be centered -->
    <slot />
  </div>
</template>
