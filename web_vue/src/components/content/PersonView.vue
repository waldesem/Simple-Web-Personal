<script setup lang="ts">
import type { Person } from "@/types";

const { data: person } = useNuxtData<Person>("person");

const toast = useToast();

const edit = useEdit();

const modal = ref(false); // Объявляем переменную модального окна

// Определяем функцию для отправки данных формы на сервер
function submitPerson() {
  modal.value = false;
  refreshNuxtData("person");
  toast.add({
    title: "Успех",
    description: "Информация успешно обновлена",
    color: "success",
  });
}

// Определяем функцию для удаления данных
async function deletePerson() {
  if (!confirm("Вы действительно хотите удалить профиль и связанные записи?"))
    return;
  const { status } = await $fetch.raw(
    `/routes/persons/${person.value?.id}`,
    { method: "DELETE" },
  );
  if (status === 204) {
    toast.add({
      title: "Успех",
      description: "Информация успешно удалена",
      color: "success",
    });
    refreshNuxtData("candidates");
    return navigateTo("/");
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
    <ElementDivMenu
      v-if="edit"
      @update="modal = true"
      @delete="deletePerson()"
    />
    <ItemsPersonDiv :item="person" />
    <!-- Выводим модальное окно для редактирования данных -->
    <UModal
      v-model:open="modal"
      title="Aнкета"
      description="Редактирование анкетные данные"
    >
      <template #body>
        <FormsResumeForm :resume="person" @update="submitPerson" />
      </template>
    </UModal>
  </div>
</template>
