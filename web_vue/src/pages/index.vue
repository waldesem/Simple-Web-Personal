<script setup lang="ts">
import { inject, onMounted } from "vue";
import { useRouter } from "vue-router";
import { KyInstance } from "ky";
import { session } from "@/state";
import type { Session } from "@/types";

const router = useRouter();

const api = inject("api") as KyInstance;

onMounted(async () => {
  session.value = await api.get("auth/session").json<Session>();
  router.push("/persons");
});
</script>

<template>
  <div class="flex flex-col items-center justify-center h-screen">
    <UProgress class="w-1/2" color="error" animation="swing" />
  </div>
</template>
