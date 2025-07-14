<template>
  <div class="relative min-h-screen flex">
    <Sidebar />
    <div class="flex-1">   
      <div class="absolute top-0 left-[240px] right-0 z-20">
        <Navbar />
      </div>
      <slot />
    </div>
  </div>
</template>
