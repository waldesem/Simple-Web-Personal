<script setup lang="ts">
import { inject } from "vue";
import { useAsyncState } from "@vueuse/core";
import { useRouter } from "vue-router";
import { KyInstance } from "ky";
import { access, refresh, session } from "@/state";
import type { Session } from "@/types";

const api = inject("api") as KyInstance;

const router = useRouter();

const { state } = useAsyncState<Session>(
  async () => await api.get("/api/auth/session").json(),
  {} as Session,
  {
    onSuccess(data) {
      console.log(access.value);
      session.value = data;
    },
    onError() {
      router.replace("/login");
    },
  },
);

function logout() {
  session.value = {} as Session;
  refresh.value = "";
  access.value = "";
  router.replace("/login");
}
</script>

<template>
  <UPage>
    <UHeader to="/persons">
      <template #title>
        <div class="inline-flex items-center text-xl font-bold space-x-1">
          <div class="text-blue-600">КАДРОВАЯ</div>
          <div class="text-red-600">БЕЗОПАСНОСТЬ</div>
        </div>
      </template>
      <template #default>
        <UButton
          v-if="state.id"
          active-class="font-bold"
          inactive-class="text-muted"
          color="neutral"
          icon="i-mi-users"
          label="Пользователи"
          to="/users"
          variant="link"
        />
      </template>
      <template #right>
        <UButton
          v-if="state.id"
          active-class="font-bold"
          inactive-class="text-muted"
          icon="i-mi-log-out"
          label="Выйти"
          variant="link"
          @click="logout"
        />
      </template>
    </UHeader>
    <UMain>
      <slot />
    </UMain>
    <UFooter v-once />
  </UPage>
</template>
