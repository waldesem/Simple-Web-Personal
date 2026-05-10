<script setup lang="ts">
import { defineAsyncComponent, PropType, ref } from "vue";
import { ofetch } from "ofetch";
import { flag } from "@/utils";
import type { Person } from "@/types";

const FormResume = defineAsyncComponent(
  () => import("@/components/forms/ResumeForm.vue"),
);

const emit = defineEmits(["update"]);

const props = defineProps({
  person: {
    type: Object as PropType<Person>,
    required: true,
  },
});

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
    <PersonDiv v-if="person" :item="person" />
    <!-- Выводим модальное окно для редактирования данных -->
    <UModal
      v-model:open="modal"
      title="Aнкета"
      description="Редактирование анкетные данные"
    >
      <template #body>
        <FormResume :resume="person" @update="submitPerson" />
      </template>
    </UModal>
  </div>
</template>
