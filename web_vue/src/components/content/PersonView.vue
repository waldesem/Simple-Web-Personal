<script setup lang="ts">
import { defineAsyncComponent, PropType, ref } from "vue";
import { useClipboard } from "@vueuse/core";
import { ofetch } from "ofetch";
import { flag } from "@/utils";
import type { Person } from "@/types";
import { divsPerson, formPerson } from "@/schema/persona";

const ItemForm = defineAsyncComponent(
  () => import("@/components/element/FormCard.vue"),
);

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
async function submitPerson(form: Person) {
  modal.value = false;
  const { status } = await ofetch.raw("/routes/persons/" + props.person.id, {
    method: "PATCH",
    body: form,
  });
  if (status !== 200) alert("Невозможно выполнить действие!");
  emit("update");
}
</script>

<template>
  <div class="ms-2 mt-2">
    <!-- Выводим кнопки редактирования или удаления данных -->
    <DivMenu v-show="flag" @update="modal = true" @delete="null" />

    <ItemCard :fields="divsPerson" :item="props.person">
      <template v-if="props.person.destination" #destination>
        <UButton
          variant="outline"
          size="sm"
          :color="copied ? 'success' : 'info'"
          :label="copied ? 'Скопировано' : 'Копировать'"
          @click="copy(props.person.destination)"
        />
      </template>
    </ItemCard>

    <!-- Выводим модальное окно для редактирования данных -->
    <UModal
      v-model:open="modal"
      title="Aнкета"
      description="Редактирование анкетные данные"
    >
      <template #body>
        <ItemForm
          :fields="formPerson"
          :item="props.person"
          @submit="submitPerson"
        />
      </template>
    </UModal>
  </div>
</template>
