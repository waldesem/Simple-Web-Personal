<script setup lang="ts">
import { defineAsyncComponent } from "vue";

const BrandHead = defineAsyncComponent(
  () => import("@/components/content/BrandHead.vue"),
);
</script>
<template>
  <UHeader v-once>
    <template #title>
      <BrandHead color1="text-grat-800" color2="text-gray-600" />
      <div class="inline-flex items-center text-xl font-bold space-x-1">
        <div>ADMIN</div>
        <div>STAFFSEC</div>
      </div>
    </template>
    <template #default>
      <UButton
        active-class="font-bold"
        inactive-class="text-muted"
        color="neutral"
        icon="i-mi-users"
        label="Кандидаты"
        to="/"
        variant="link"
      />
    </template>
    <template #right>
      <UAvatar text="A" :chip="{ inset: true, color: 'secondary' }" />
    </template>
  </UHeader>
</template>
