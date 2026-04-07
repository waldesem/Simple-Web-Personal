<script setup lang="ts">
import { PropType, ref } from "vue";
import { useRouter } from "vue-router";
import { ofetch } from "ofetch";
import { useToast } from "@nuxt/ui/composables";
import type { Person } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  person: {
    type: Object as PropType<Person>,
    required: true,
  },
  edit: {
    type: Boolean,
    required: true,
  },
});

const toast = useToast();

const router = useRouter();

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

// Определяем функцию для удаления данных
async function deletePerson() {
  if (!confirm("Вы действительно хотите удалить профиль и связанные записи?"))
    return;
  const { status } = await ofetch.raw(`/routes/persons/${props.person.id}`, {
    method: "DELETE",
  });
  if (status === 204) {
    toast.add({
      title: "Успех",
      description: "Информация успешно удалена",
      color: "success",
    });
    return router.push({ name: "index" });
  } else {
    toast.add({
      title: "Ошибка",
      description: "Невозможно выполнить действие.",
      color: "error",
    });
  }
}
</script>

<template>
  <div class="ms-2 mt-2">
    <!-- Выводим кнопки редактирования или удаления данных -->
    <DivMenu v-if="props.edit" @update="modal = true" @delete="deletePerson" />
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
