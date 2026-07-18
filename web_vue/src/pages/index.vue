<script setup lang="ts">
import { inject, onMounted } from "vue";
import { useRouter } from "vue-router";
import { KyInstance } from "ky";
import { session } from "@/state";
import type { Session } from "@/types";

const router = useRouter();

const api = inject("api") as KyInstance;

onMounted(async () => {
  try {
    session.value = await api.get("auth/session").json<Session>();
    router.replace("/persons");
  } catch (error) {
    console.error(error);
    router.replace("/login");
  }
});
</script>

<template>
  <div>
    <UPageBody class="flex flex-col items-center justify-center h-screen">
      <UProgress color="error" animation="swing" size="xl" />
    </UPageBody>
  </div>
</template>
