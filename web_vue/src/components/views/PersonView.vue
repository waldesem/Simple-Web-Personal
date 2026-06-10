<script setup lang="ts">
import ky from "ky";
import { ref } from "vue";
import { useAsyncState, useClipboard } from "@vueuse/core";
import { itemsFields } from "@/schema/items";
import { itemsForms } from "@/schema/forms";
import type { Person } from "@/types";

const emit = defineEmits(["listnames"]);

const props = defineProps({
  personId: {
    type: String,
    required: true,
  },
});

const modal = ref(false); // Объявляем переменную модального окна

const { copy, copied } = useClipboard();

const { execute, state, isLoading } = useAsyncState(
  async () => await ky.get("/api/persons/" + props.personId).json<Person>(),
  {} as Person,
  {
    onSuccess(data) {
      emit("listnames", [data.surname, data.firstname, data.patronymic ?? '']);
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
    :fields="itemsFields.person"
    :item="state"
    @delete="null"
    @update="modal = true"
  >
    <template #destination>
      <NUButton
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
  <NUModal
    v-model:open="modal"
    title="Aнкета"
    description="Редактирование анкетные данные"
  >
    <template #body>
      <FormDiv :fields="itemsForms.person" :item="state" @submit="submit" />
    </template>
  </NUModal>
</template>
