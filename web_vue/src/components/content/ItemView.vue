<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, PropType, ref } from "vue";
import { ofetch } from "ofetch";
import { useToast } from "@nuxt/ui/composables";
import type { Items } from "@/types";

const toast = useToast();

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  view: {
    type: String as PropType<keyof Items>,
    required: true,
  },
  candId: {
    type: String,
    required: true,
  },
  edit: {
    type: Boolean,
    required: true,
  },
});

onBeforeMount(async () => await getItem());

const data = ref<Items[keyof Items]>([]);
const item = ref<object>({}); // Данные для редактирования
const modal = ref(false); // Флаг для открытия модального окна

// Определяем функцию для получения данных из API
async function getItem() {
  data.value = await ofetch(`/routes/${props.view}/${props.candId}`);
}

function capitalize(str: string) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

const ItemComponent = defineAsyncComponent(
  () => import(`../items/${capitalize(props.view)}Item.vue`),
);
const FormComponent = defineAsyncComponent(
  () => import(`../forms/${capitalize(props.view)}Form.vue`),
);

// Определяем функцию для отправки данных формы на сервер
async function submitItem(form: typeof item.value) {
  modal.value = false;
  const { status } = await ofetch.raw(`/routes/${props.view}/${props.candId}`, {
    method: "POST",
    body: form,
  });
  item.value = {};
  await getItem();
  if (status === 201) {
    toast.add({
      title: "Успех",
      description: "Информация успешно обновлена",
      color: "success",
    });
  } else
    toast.add({
      title: "Ошибка",
      description: "Невозможно выполнить действие.",
      color: "error",
    });
}

// Определяем функцию для удаления данных
async function deleteItem(itemId: string) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { status } = await ofetch.raw(`/routes/${props.view}/${itemId}`, {
    method: "DELETE",
  });
  await getItem();
  if (status === 204) {
    toast.add({
      title: "Успех",
      description: "Информация успешно удалена",
      color: "success",
    });
  } else
    toast.add({
      title: "Ошибка",
      description: "Невозможно выполнить действие.",
      color: "error",
    });
}
</script>

<template>
  <!-- Выводим сообщение если данные отсутствуют -->
  <UEmpty v-if="!data?.length" class="m-4" title="Данные отсутствуют" size="sm">
    <template #body>
      <UButton
        v-if="props.edit"
        label="Добавить запись"
        variant="outline"
        size="sm"
        @click="modal = true"
      />
    </template>
  </UEmpty>

  <div v-for="(content, index) in data" :key="index" class="mx-2 py-2">
    <!-- Выводим кнопки редактирования/удаления данных, в режиме редактирования -->
    <DivMenu
      v-if="props.edit"
      @update="
        item = content;
        modal = true;
      "
      @delete="deleteItem(content.id)"
    />
    <!-- Выводим элемент данных -->
    <component :is="ItemComponent" :item="content" />
    <USeparator v-if="index + 1 < data.length" />
  </div>

  <!-- Модальное окно для редактирования данных -->
  <UModal
    v-model:open="modal"
    :title="props.title"
    description="Добавить/редактировать данные"
  >
    <UButton
      v-if="props.edit && data?.length"
      class="mb-2"
      label="Добавить запись"
      variant="outline"
      size="sm"
      block
    />
    <template #body>
      <component :is="FormComponent" :item="item" @update="submitItem" />
    </template>
  </UModal>
</template>
