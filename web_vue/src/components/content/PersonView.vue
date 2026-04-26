<script setup lang="ts">
import { PropType, ref } from "vue";
import { ofetch } from "ofetch";
import { useToast } from "@nuxt/ui/composables";
import { flag } from "@/utils";
import type { Person } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  person: {
    type: Object as PropType<Person>,
    required: true,
  },
});

const toast = useToast();

const modal = ref(false); // Объявляем переменную модального окна

// Определяем функцию для отправки данных формы на сервер
async function submitPerson(form: Person) {
  modal.value = false;
  const { status } = await ofetch.raw("/routes/persons/" + props.person.id, {
    method: "PATCH",
    body: { ...form, created: new Date().toISOString() },
  });
  if (status === 200) {
    toast.add({
      title: "Успех",
      description: "Информация успешно обновлена",
      color: "success",
    });
  } else {
    toast.add({
      title: "Ошибка",
      description: "Невозможно выполнить действие.",
      color: "error",
    });
  }
  emit("update");
}
</script>

<template>
  <div class="ms-2 mt-2">
    <!-- Выводим кнопки редактирования или удаления данных -->
    <DivMenu v-if="flag" @update="modal = true" @delete="null" />
    <PersonDiv :item="person" />
    <!-- Выводим модальное окно для редактирования данных -->
    <UModal
      v-model:open="modal"
      title="Aнкета"
      description="Редактирование анкетные данные"
    >
      <template #body>
        <ResumeForm :resume="person" @update="submitPerson" />
      </template>
    </UModal>
  </div>
</template>
