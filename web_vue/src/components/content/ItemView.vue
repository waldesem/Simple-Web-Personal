<script setup lang="ts">
import {
  defineAsyncComponent,
  onMounted,
  PropType,
  ref,
  shallowRef,
} from "vue";
import { ofetch } from "ofetch";
import { capitalize, flag } from "@/utils";
import type { Items } from "@/types";

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
});

const ItemComponent = defineAsyncComponent(
  () => import(`../items/${capitalize(props.view)}Item.vue`),
);
const FormComponent = defineAsyncComponent(
  () => import(`../forms/${capitalize(props.view)}Form.vue`),
);

onMounted(async () => await getItem());

const data = shallowRef<Items[keyof Items]>([]);
const item = shallowRef<(typeof data.value)[number] | null>(null);
const modal = ref(false); // Флаг для открытия модального окна

// Определяем функцию для получения данных из API
async function getItem() {
  data.value = await ofetch(`/routes/${props.view}/${props.candId}`);
}

// Определяем функцию для отправки данных формы на сервер
async function submitItem(form: typeof item.value) {
  modal.value = false;
  const { status } = await ofetch.raw(`/routes/${props.view}/${props.candId}`, {
    method: "POST",
    body: form,
  });
  item.value = null;
  await getItem();
  if (status !== 201) alert("Невозможно выполнить действие!");
}

// Определяем функцию для удаления данных
async function deleteItem(itemId: string) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { status } = await ofetch.raw(`/routes/${props.view}/${itemId}`, {
    method: "DELETE",
  });
  await getItem();
  if (status !== 204) alert("Невозможно выполнить действие!");
}
</script>

<template>
  <!-- Выводим сообщение если данные отсутствуют -->
  <UEmpty v-if="!data?.length" class="m-4" title="Данные отсутствуют" size="sm">
    <template #body>
      <UButton
        v-show="flag"
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
      v-show="flag"
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
      v-if="flag && data?.length"
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
