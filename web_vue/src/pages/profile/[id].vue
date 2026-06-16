<script setup lang="ts">
import ky from "ky";
import { ref } from "vue";
import { useAsyncState, useClipboard } from "@vueuse/core";
import { person as PersonItem } from "@/schema/items";
import { person as PersonForm } from "@/schema/forms";
import type { Navigations, Person } from "@/types";

definePage({ meta: { layout: "UserLayout" }, props: true });

const props = defineProps({
  id: { type: String, required: true }, // ID кандидата из index.vue
});

const { copy, copied } = useClipboard();

const modal = ref(false); // Объявляем переменную модального окна

const anketa = { label: "Анкета", icon: "i-mi-user", slot: "person" };

const tabs = [
  { label: "Проверки", icon: "i-mi-document-check", slot: "checks" },
  { label: "Полиграф", icon: "i-mi-heart", slot: "poligrafs" },
  { label: "Расследования", icon: "i-mi-archive", slot: "investigations" },
  { label: "Запросы", icon: "i-mi-comment", slot: "inquiries" },
] as Navigations[];

const accordion = [
  { label: "Должности", icon: "i-mi-laptop", slot: "staffs" },
  { label: "Образование", icon: "i-mi-book", slot: "educations" },
  { label: "Места работы", icon: "i-mi-computer", slot: "workplaces" },
  { label: "Документы", icon: "i-mi-document", slot: "documents" },
  { label: "Адреса", icon: "i-mi-home", slot: "addresses" },
  { label: "Контакты", icon: "i-mi-call", slot: "contacts" },
  { label: "Изменения имени", icon: "i-mi-edit", slot: "previous" },
  { label: "Аффилированность", icon: "i-mi-users", slot: "affilations" },
] as Navigations[];

const { execute, state, isLoading } = useAsyncState<Person>(
  async () => await ky.get("/api/persons/" + props.id).json(),
  {} as Person,
);

// Определяем функцию для отправки данных формы на сервер
async function submit(form: Person) {
  modal.value = false;
  isLoading.value = true;
  const { status } = await ky.patch("/api/persons/" + props.id, {
    json: form,
  });
  if (status !== 200) alert("Невозможно выполнить действие!");
  await execute();
}
</script>

<template>
  <UContainer>
    <UPageHeader
      :title="`${state.surname} ${state.firstname} ${state.patronymic ?? ''}`"
    />
    <UPageBody>
      <UTabs :items="[anketa, ...tabs]" :unmount-on-hide="false">
        <!-- Слот вкладки для отображения анкеты -->
        <template #person>
          <ItemDiv
            :class="{ 'animate-pulse': isLoading }"
            :fields="PersonItem"
            :item="state"
            @delete="null"
            @update="modal = true"
          >
            <template #destination>
              <UButton
                v-if="state?.destination"
                :color="copied ? 'success' : 'info'"
                :label="copied ? 'Скопировано' : 'Копировать'"
                size="sm"
                variant="outline"
                @click="copy(state.destination)"
              />
            </template>
          </ItemDiv>

          <!-- Модальное окно для редактирования данных -->
          <UModal
            v-model:open="modal"
            title="Aнкета"
            description="Редактирование анкетные данные"
          >
            <template #body>
              <FormDiv :fields="PersonForm" :item="state" @submit="submit" />
            </template>
          </UModal>

          <USeparator />

          <!-- Aккордеон с данными staffs, educations и т.д. -->
          <UAccordion :items="accordion">
            <template
              v-for="accord in accordion"
              #[accord.slot]
              :key="accord.slot"
            >
              <ItemView
                :cand-id="props.id"
                :title="accord.label"
                :view="accord.slot"
              />
            </template>
          </UAccordion>
        </template>

        <!-- Вкладки проверки, полиграф и др. -->
        <template v-for="tab in tabs" #[tab.slot] :key="tab.slot">
          <ItemView :cand-id="props.id" :title="tab.label" :view="tab.slot" />
        </template>
      </UTabs>
    </UPageBody>
  </UContainer>
</template>
