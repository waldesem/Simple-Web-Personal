<script setup lang="ts">
import ky from "ky";
import { shallowRef } from "vue";
import { useAsyncState, useClipboard } from "@vueuse/core";
import { person as PersonItem } from "@/schema/items";
import { person as PersonForm } from "@/schema/forms";
import type { Person } from "@/types";

const emit = defineEmits(["listnames"]);

const props = defineProps({
  personId: {
    type: String,
    required: true,
  },
});

const modal = shallowRef(false); // Объявляем переменную модального окна

const { copy, copied } = useClipboard();

const { execute, state, isLoading } = useAsyncState<Person>(
  async () => await ky.get("/api/persons/" + props.personId).json(),
  {} as Person,
  {
    onSuccess(data) {
      emit("listnames", [data.surname, data.firstname, data.patronymic ?? ""]);
    },
  },
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

  <!-- Выводим модальное окно для редактирования данных -->
  <UModal
    v-model:open="modal"
    title="Aнкета"
    description="Редактирование анкетные данные"
  >
    <template #body>
      <FormDiv :fields="PersonForm" :item="state" @submit="submit" />
    </template>
  </UModal>
</template>
