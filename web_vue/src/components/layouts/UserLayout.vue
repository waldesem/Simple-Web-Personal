<script setup lang="ts">
import { useRouter } from 'vue-router';
import { access, refresh, session } from '@/state';
import { Roles, type Session } from '@/types';
import { ref } from 'vue';

const router = useRouter();

const find = ref('');

function logout() {
  session.value = {} as Session;
  refresh.value = '';
  access.value = '';
  router.replace('/login');
}

function openDB() {
  if (find.value.length > 1)
    router.push({ path: '/persons', query: { find: find.value } });
}
</script>

<template>
  <UHeader to="/registry" class="no-print">
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
      <UFieldGroup>
        <UInput
          v-model="find"
          icon="i-lucide-search"
          variant="outline"
          placeholder="Поиск..."
        />
        <UButton icon="i-lucide-search" variant="outline" @click="openDB" />
      </UFieldGroup>
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
