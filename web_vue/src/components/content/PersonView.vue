<script setup lang="ts">
import { inject, Ref, ref } from "vue";
import { useRouter } from "vue-router";
import { ofetch } from "ofetch";
import { useToast } from "@nuxt/ui/composables";
import type { Person } from "@/types";
import { useEdit } from "../../composables";

const emit = defineEmits(["update"]);

const person = inject("person") as Ref<Person>;

const toast = useToast();

const router = useRouter();

const edit = useEdit();

const modal = ref(false); // Объявляем переменную модального окна

// Определяем функцию для отправки данных формы на сервер
function submitPerson() {
  modal.value = false;
  emit("update");
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
  const { status } = await ofetch.raw(
    `/routes/persons/${person.value?.id}`,
    { method: "DELETE" },
  );
  if (status === 204) {
    toast.add({
      title: "Успех",
      description: "Информация успешно удалена",
      color: "success",
    });
    return router.push("/");
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
    <DivMenu
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
        <ResumeForm :resume="person" @update="submitPerson" />
      </template>
    </UModal>
  </div>
</template>
