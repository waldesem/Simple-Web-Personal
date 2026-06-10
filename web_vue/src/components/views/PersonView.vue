<script setup lang="ts">
import ky from "ky";
import { ref } from "vue";
import { useAsyncState, useClipboard } from "@vueuse/core";
import { itemsFields } from "@/schema/items";
import { itemsForms } from "@/schema/forms";
import type { Person } from "@/types";

const person = defineModel<Person>();

const props = defineProps({
  personId: {
    type: String,
    required: true,
  },
});

const modal = ref(false); // Объявляем переменную модального окна

const { copy, copied } = useClipboard();

const { execute, isLoading } = useAsyncState(
  async () =>
    (person.value = await ky
      .get("/api/persons/" + props.personId)
      .json<Person>()),
  {} as Person,
);

// Определяем функцию для отправки данных формы на сервер
async function submit(form: Person) {
  modal.value = false;
  const { status } = await ky.patch("/api/persons/" + props.personId, {
    json: form,
  });
  if (status !== 200) alert("Невозможно выполнить действие!");
  await execute();
}
</script>

<template>
  <ItemDiv
    :class="{ 'animate-pulse': isLoading }"
    :fields="itemsFields.person"
    :item="person"
    @delete="null"
    @update="modal = true"
  >
    <template #destination>
      <NUButton
        v-if="person?.destination"
        :color="copied ? 'success' : 'info'"
        :label="copied ? 'Скопировано' : 'Копировать'"
        size="sm"
        variant="outline"
        @click="copy(person.destination)"
      />
    </template>
  </ItemDiv>

  <!-- Выводим модальное окно для редактирования данных -->
  <NUModal
    v-model:open="modal"
    title="Aнкета"
    description="Редактирование анкетные данные"
  >
    <template #body>
      <FormDiv
        :fields="itemsForms.person"
        :item="person"
        @submit="submit"
      />
    </template>
  </NUModal>
</template>
