<script setup lang="ts">
import ky from "ky";
import { type PropType, ref } from "vue";
import { useClipboard } from "@vueuse/core";
import { itemsFields } from "@/schema/items";
import { itemsForms } from "@/schema/forms";
import type { Person } from "@/types";

const props = defineProps({
  person: {
    type: Object as PropType<Person>,
    required: true,
  },
});

const { copy, copied } = useClipboard();

const emit = defineEmits(["update"]);

const modal = ref(false); // Объявляем переменную модального окна

// Определяем функцию для отправки данных формы на сервер
async function submit(form: Person) {
  modal.value = false;
  const { status } = await ky.patch("/api/persons/" + props.person.id, {
    json: form,
  });
  if (status !== 200) alert("Невозможно выполнить действие!");
  emit("update");
}
</script>

<template>
  <ItemDiv
    :fields="itemsFields.person"
    :item="props.person"
    @update="modal = true"
    @delete="null"
  >
    <template v-if="props.person.destination" #destination>
      <NUButton
        :color="copied ? 'success' : 'info'"
        :label="copied ? 'Скопировано' : 'Копировать'"
        size="sm"
        variant="outline"
        @click="copy(props.person.destination)"
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
        :item="props.person"
        @submit="submit"
      />
    </template>
  </NUModal>
</template>
