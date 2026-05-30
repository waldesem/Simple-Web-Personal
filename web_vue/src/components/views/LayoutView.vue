<script setup lang="ts">
import ky from "ky";
import { onBeforeMount } from "vue";
import { session } from "@/state";
import type { Session } from "@/types";

onBeforeMount(
  async () => (session.value = await ky.get<Session>("/routes/session").json()),
);
</script>

<template>
  <UPage>
    <UHeader to="/">
      <template #title>
        <div class="inline-flex items-center text-xl font-bold space-x-1">
          <div class="text-blue-600">КАДРОВАЯ</div>
          <div class="text-red-600">БЕЗОПАСНОСТЬ</div>
        </div>
      </template>
      <template #default>
        <UNavigationMenu
          v-if="session.role === 'admin'"
          :items="[
            {
              label: 'Пользователи',
              icon: 'i-lucide-users',
              to: '/users',
            },
          ]"
          variant="link"
        />
      </template>
      <template #right>
        <UAvatar :alt="session?.fullname ?? '?'" size="md" />
      </template>
    </UHeader>
    <UMain>
      <slot />
    </UMain>
    <UFooter v-once />
  </UPage>
</template>
