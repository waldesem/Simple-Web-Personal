<script setup lang="ts">
import { onBeforeMount, inject, ref, Ref } from "vue";
import { ofetch } from "ofetch";
import type { Items } from "@/types";

const emit = defineEmits(["update"]);

const candId = inject("candId") as Ref<string>;

const data = ref({} as Items);

onBeforeMount(async () => await getItems());

async function getItems() {
  data.value = await ofetch<Items>("/routes/items/" + candId.value);
}

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
        <PersonView @update="emit('update')" />
      </div>
      <USeparator />
      <!-- Aккордеон с данными staffs, educations и т.д. -->
      <UAccordion :items="accordion" :unmount-on-hide="false">
        <template v-for="accord in accordion" #[accord.slot] :key="accord.slot">
          <ItemView
            :data="data[accord.slot]"
            :view="accord.slot as keyof Items"
            :title="accord.label"
          />
        </template>
      </UAccordion>
    </template>

    <!-- Вкладки проверки, полиграф и др. -->
    <template v-for="tab in tabs.slice(1)" #[tab.slot] :key="tab.slot">
      <div class="mt-2">
        <ItemView
          :data="data[tab.slot as keyof Items]"
          :view="tab.slot as keyof Items"
          :title="tab.label"
        />
      </div>
    </template>
  </UTabs>
</template>
