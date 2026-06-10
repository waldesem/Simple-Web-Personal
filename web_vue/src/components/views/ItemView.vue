<script setup lang="ts">
import ky from "ky";
import { type PropType, ref, shallowRef } from "vue";
import { itemsFields } from "@/schema/items";
import { itemsForms } from "@/schema/forms";
import type { Items } from "@/types";

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
  candId: {
    type: String,
    required: true,
  },
  data: {
    type: Object as PropType<Items[keyof Items]>,
    default: []
  },
  title: {
    type: String,
    required: true,
  },
  view: {
    type: String as PropType<keyof Items>,
    required: true,
  },
});

const isLoading = ref(false);
const items = shallowRef(props.data);
const item = shallowRef({} as typeof props.data[number]);
const modal = ref(false); // Флаг для открытия модального окна
const method = ref<"POST" | "PATCH">("POST");

async function getItem() {
  items.value = await ky.get(`/api/items/${props.view}/${props.candId}`).json();
}

// Определяем функцию для отправки данных формы на сервер
async function submitItem(form: typeof item.value) {
  modal.value = false;
  isLoading.value = true;
  const url = `/api/items/${props.view}/${props.candId}`;
  const { status } = await ky(
    method.value === "POST" ? url : url + "/" + item.value.id,
    {
      method: method.value,
      json: { item: props.view, ...form },
    },
  );
  await getItem();
  item.value = {} as typeof item.value;
  if (status !== 201 && status !== 200) alert("Невозможно выполнить действие!");
  isLoading.value = false;
}

// Определяем функцию для удаления данных
async function deleteItem(itemId: string) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  isLoading.value = true;
  const { status } = await ky.delete(`/api/items/${props.view}/${itemId}`);
  if (status === 204) await getItem();
  else alert("Невозможно выполнить действие!");
  isLoading.value = false;
}
</script>

<template>
  <!-- Выводим сообщение если данные отсутствуют -->
  <NUEmpty v-if="!items.length" size="sm" title="Нет данных" variant="naked">
    <template #body>
      <NUButton
        label="Добавить запись"
        size="sm"
        variant="outline"
        @click="
          modal = true;
          method = 'POST';
        "
      />
    </template>
  </NUEmpty>

  <div
    v-for="(content, index) in items"
    :key="index"
    :class="{ 'animate-pulse': isLoading }"
  >
    <!-- Выводим элемент данных -->
    <ItemDiv
      :item="content"
      :fields="itemsFields[view]"
      @delete="deleteItem(content.id)"
      @update="
        item = content;
        modal = true;
        method = 'PATCH';
      "
    />
    <NUSeparator v-if="index + 1 < items.length" />
  </div>

  <!-- Модальное окно для редактирования данных -->
  <NUModal
    v-model:open="modal"
    :description="
      method === 'POST' ? 'Добавить данные' : 'Редактировать данные'
    "
    :title="props.title"
  >
    <NUButton
      v-if="items.length"
      block
      class="my-2"
      color="neutral"
      icon="i-mi-add"
      title="Добавить запись"
      size="sm"
      variant="outline"
      @click="method = 'POST'"
    />
    <template #body>
      <FormDiv :item="item" :fields="itemsForms[view]" @submit="submitItem" />
    </template>
  </NUModal>
</template>
