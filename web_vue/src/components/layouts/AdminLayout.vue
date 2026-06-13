<script setup lang="ts">
import ky from "ky";
import { useAsyncState } from "@vueuse/core";
import { session } from "@/state";
import type { Session } from "@/types";

const { state } = useAsyncState<Session>(
  async () => await ky.get("/api/auth/session").json(),
  {} as Session,
  {
    onSuccess(data) {
      session.value = data;
    },
  },
);
</script>

<template>
  <UPage>
    <UHeader v-once to="/users">
      <template #title>
        <div class="inline-flex items-center text-xl font-bold space-x-1">
          <div class="text-slate-500">ADMIN</div>
          <div class="text-olive-500">STAFFSEC</div>
        </div>
      </template>
      <template #default>
        <ULink to="/" :replace="false" class="font-bold">Кандидаты</ULink>
      </template>
      <template #right>
        <UAvatar
          :alt="state.fullname"
          :chip="{ inset: true, color: 'warning' }"
          size="md"
        />
      </template>
    </UHeader>
    <UMain>
      <slot />
    </UMain>
    <UFooter v-once />
  </UPage>
</template>
