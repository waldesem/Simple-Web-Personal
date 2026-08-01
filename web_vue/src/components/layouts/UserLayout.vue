<script setup lang="ts">
import { useRouter } from 'vue-router';
import { access, refresh, session } from '@/state';
import { Roles, type Session } from '@/types';
import BrandHead from '@/components/content/BrandHead.vue';

const router = useRouter();

function logout() {
  session.value = {} as Session;
  refresh.value = '';
  access.value = '';
  router.replace('/login');
}
</script>

<template>
  <UHeader to="/persons" class="no-print">
    <template #title>
      <BrandHead />
    </template>
    <template #default>
      <UButton
        v-if="session.role === Roles.admin"
        active-class="font-bold"
        color="neutral"
        icon="i-lucide-users"
        label="Пользователи"
        to="/users"
        variant="link"
      />
    </template>
    <template #right>
      <UButton
        :disabled="!session.auth"
        :avatar="{
          alt: session.fullname ?? '?',
          size: 'lg',
          color: 'primary',
          ui: { fallback: 'text-error' },
          chip: {
            inset: true,
            color: session.fullname ? 'success' : 'error',
          },
        }"
        variant="ghost"
        title="Выход"
        size="lg"
        @click="logout"
      />
    </template>
  </UHeader>
</template>
