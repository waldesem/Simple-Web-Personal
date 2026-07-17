<script setup lang="ts">
import { useRouter } from "vue-router";
import { access, refresh, session } from "@/state";
import { Roles, type Session } from "@/types";
import { defineAsyncComponent } from "vue";

const BrandHead = defineAsyncComponent(
  () => import("@/components/content/BrandHead.vue"),
);

const router = useRouter();

function logout() {
  session.value = {} as Session;
  refresh.value = "";
  access.value = "";
  router.replace("/login");
}
</script>

<template>
  <UPage>
    <UHeader to="/">
      <template #title>
        <BrandHead />
      </template>
      <template #default>
        <UButton
          v-if="session.role === Roles.admin"
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
          v-if="session.id"
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
