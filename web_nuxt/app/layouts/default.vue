<template>
  <UPage>
    <UHeader to="/">
      <template #title>
        <div class="inline-flex items-center text-xl font-bold space-x-1">
          <div class="text-blue-600">КАДРОВАЯ</div>
          <div class="text-red-600">БЕЗОПАСНОСТЬ</div>
        </div>
      </template>
    </UHeader>
    <UMain class="pt-16 pb-4">
      <slot />
    </UMain>
    <UFooter/>      
  </UPage>
</template>
