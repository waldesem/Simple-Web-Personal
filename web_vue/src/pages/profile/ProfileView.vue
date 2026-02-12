<script setup lang="ts">
import { useRoute } from 'vue-router'
import { ofetch } from "ofetch";
import type { Person } from "@/types";

// Получаем данные id кандидата из URL
const route = useRoute();

const candId = computed(() => route.params.id as string);
provide("candId", candId);

const edit = useEdit();

// Определяем функцию для получения данных из API
async onBeforemount(
  () => ofetch<Person>("/routes/persons/" + candId.value),
  { default: () => ({}) as Person },
);
</script>

<template>
  <LayoutsView>
  <UContainer>
    <UPageHeader
      :title="`${data.surname} ${data.firstname} ${data.patronymic ?? ''}`"
    >
      <template #links>
        <UButton
          variant="outline"
          :loading="status === 'pending'"
          :color="edit ? 'error' : 'primary'"
          :label="edit ? 'Откл.Редакт.' : 'Вкл.Редакт.'"
          :icon="edit ? 'i-lucide-pencil' : 'i-lucide-pencil-off'"
          @click="edit = !edit"
        />
      </template>
    </UPageHeader>
    <ContentTabsView />
  </UContainer>
  </LayoutsView>
</template>
