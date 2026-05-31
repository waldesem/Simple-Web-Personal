<script setup lang="ts">
import ky from "ky";
import { onBeforeMount } from "vue";
import { session } from "@/state";
import type { Session } from "@/types";

onBeforeMount(
  async () =>
    (session.value = await ky.get<Session>("/api/auth/session").json()),
);
</script>

<template>
  <NUPage>
    <NUHeader to="/">
      <template #title>
        <div class="inline-flex items-center text-xl font-bold space-x-1">
          <div class="text-blue-600">КАДРОВАЯ</div>
          <div class="text-red-600">БЕЗОПАСНОСТЬ</div>
        </div>
      </template>
      <template #default>
        <NULink to="/users" :replace="false" class="font-bold">
          Пользователи
        </NULink>
      </template>
      <template #right>
        <NUAvatar :alt="session.fullname ?? '?'" size="md" />
      </template>
    </NUHeader>
    <NUMain>
      <slot />
    </NUMain>
    <NUFooter v-once />
  </NUPage>
</template>
