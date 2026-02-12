<script setup lang="ts">
import type { Items } from "@/types";

const candId = inject("candId") as Ref<string>;

const { data } = await useAsyncData(
  "items",
  () => $fetch<Items>("/routes/items/" + candId.value),
  { default: () => ({}) as Items },
);

// Определяем массив элементов табов
const tabs = [
  {
    label: "Анкета",
    slot: "anketa" as const,
  },
  {
    label: "Проверки",
    slot: "checks" as keyof Items,
  },
  {
    label: "Полиграф",
    slot: "poligrafs" as keyof Items,
  },
  {
    label: "Расследования",
    slot: "investigations" as keyof Items,
  },
  {
    label: "Запросы",
    slot: "inquiries" as keyof Items,
  },
];

// Определяем массив элементов аккордеона
const accordion = [
  {
    label: "Должности",
    slot: "staffs" as keyof Items,
  },
  {
    label: "Образование",
    slot: "educations" as keyof Items,
  },
  {
    label: "Места работы",
    slot: "workplaces" as keyof Items,
  },
  {
    label: "Документы",
    slot: "documents" as keyof Items,
  },
  {
    label: "Адреса",
    slot: "addresses" as keyof Items,
  },
  {
    label: "Контакты",
    slot: "contacts" as keyof Items,
  },
  {
    label: "Изменения имени",
    slot: "previous" as keyof Items,
  },
  {
    label: "Аффилированность",
    slot: "affilations" as keyof Items,
  },
];
</script>

<template>
  <!-- Меню для переключения между вкладками -->
  <UTabs :items="tabs" :unmount-on-hide="false" variant="pill" class="mt-4">
    <!-- Слот вкладки для отображения анкеты -->
    <template #anketa>
      <div class="mt-4">
        <ContentPersonView />
      </div>
      <USeparator />
      <!-- Aккордеон с данными staffs, educations и т.д. -->
      <UAccordion :items="accordion" :unmount-on-hide="false">
        <template v-for="accord in accordion" #[accord.slot] :key="accord.slot">
          <ContentItemView
            :data="data[accord.slot]"
            :view="(accord.slot as keyof Items)"
            :title="accord.label"
          />
        </template>
      </UAccordion>
    </template>

    <!-- Вкладки проверки, полиграф и др. -->
    <template v-for="tab in tabs.slice(1)" #[tab.slot] :key="tab.slot">
      <div class="mt-2">
        <ContentItemView
          :data="data[tab.slot as keyof Items]"
          :view="(tab.slot as keyof Items)"
          :title="tab.label"
        />
      </div>
    </template>
  </UTabs>
</template>
